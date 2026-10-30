# SmartDesk — Database design (revision 2.3)

Target logical model for PostgreSQL. This is not the implemented database yet. It is derived from [02-use-cases.md](../02-use-cases.md) and [06-acceptance-criteria.md](../06-acceptance-criteria.md).

## Files
- `smartdesk.dbml` — full schema (40 tables, 23 enums). Import it at https://dbdiagram.io/; table groups keep the diagram readable.
- `smartdesk-constraints.sql` — partial and expression unique indexes, exclusion constraint and vector index that DBML cannot express. Run it after the DDL exported from the DBML.
- `smartdesk-full-erd.mmd` — Mermaid ERD of all 40 tables and every column, generated from the DBML. Open it at https://mermaid.live/.
- `smartdesk-core-erd.mmd` — 22 core tables, showing only keys and state columns.

Reading the ERDs:
- Edges to `tenants` are hidden, because every table except `tenants` and `users` carries `tenant_id`.
- `||` means a required reference and `|o` an optional one (the FK column is nullable, also marked `"nullable"`). `o|` on the child side means 1:1, for example `ticket_sla` and `change_plans`.
- Each label is the role the parent plays, for example `requester`, `assigned`, or `approver`.
- The core view also leaves out bookkeeping actors such as `created by` and `published by`.

Generate the DDL with:

```bash
npx @dbml/cli dbml2sql smartdesk.dbml --postgres -o smartdesk.sql
```

The `checks { }` blocks need `@dbml/cli` / `@dbml/core` 3.10 or newer; older versions report "A custom element can only appear in a Project". On Windows, `@dbml/cli` 10.x fails on absolute paths, so call `exporter.export(source, 'postgres')` from `@dbml/core` or run the CLI from WSL.

## How tenant isolation works
Every tenant-owned table has `tenant_id`, and every reference between tenant-owned tables is a composite foreign key `(tenant_id, x_id) → parent(tenant_id, id)`. The database therefore rejects any row that points at another tenant's data, even if the API has a bug. The same technique enforces several business rules:

| Rule | How |
|---|---|
| `tickets.kind` equals the kind of its catalog version | FK `(tenant_id, catalog_version_id, kind)` |
| An attachment's comment is on the same ticket | FK `(tenant_id, ticket_id, comment_id)` |
| Fulfilment steps only on service requests, change plans only on changes | pinned `ticket_kind` column + CHECK + FK to `tickets (tenant_id, id, kind)` |
| An AI draft belongs to the conversation owner, and its ticket is requested by that same person | FKs to `ai_conversations (tenant_id, id, membership_id)` and `tickets (tenant_id, id, requester_membership_id)` |
| A tenant session belongs to a real membership | FK `user_sessions (tenant_id, user_id) → memberships` |

## Changes from revision 1
**Requirements coverage**
- `ticket_assets` — link a ticket to the device it concerns (UC22).
- Invitations (UC04) live on the INVITED membership itself (`invite_token_hash`, `invite_expires_at`, `invited_by_membership_id`). `users.password_hash` is nullable until the invite is accepted.
- `ticket_sla.*_warning_sent_at` — one notification per SLA threshold (UC37). `notifications.dedupe_key` is unique as a second guard.
- KB review fields (`submitted_at`, `reviewed_by`, `review_comment`), with a CHECK that the reviewer is not the author (UC34).
- `kb_chunks` — embeddings of published KB versions for AI retrieval.
- `tickets.source` (PORTAL / AI_ASSISTANT), `tenant_counters` for `ticket_no`, `tenants.suspended_reason`.
- One business calendar per tenant (AC-UC36): `tenants.working_hours` + `tenants.timezone` + `tenant_holidays`. It replaces the per-policy `business_calendar` JSON; holidays are rows so that SLA timers can skip days like Tet.

**Single source of truth**
- Removed `catalog_versions.needs_approval`. Approval is decided only by `approval_rules`, which are append-only (`effective_from/to`) and support approval steps.
- `kind` is enforced along catalog item → version → ticket.
- Removed `fulfilment_tasks` (it was 1:1 with the ticket and duplicated the assignee). `fulfilment_steps` hang directly off the ticket.
- Removed `RETURNED` from the asset status: a returned device is `AVAILABLE` again.
- Roles are a fixed enum `role_code` (EMPLOYEE, IT_STAFF, IT_MANAGER, ORG_ADMIN) used by `membership_roles`, `approval_rules` and `ticket_approvals`; there is no `roles` table. Platform admins are `users.is_platform_admin`.
- `sla_policies` are append-only and cannot overlap in time (exclusion constraint).

**Integrity**
- 22 enums replace free-text status and type columns. `tickets` has a CHECK that each status is valid for the ticket kind.
- 50 CHECK constraints, for example: rejection needs a reason; resolving needs a resolution note; REOPENED, CANCELLED, TRANSFERRED and ESCALATED events need a reason; a ticket cannot link to itself; a RELATED link is stored only once.
- Deletion policy is explicit: no hard deletes (NO ACTION by default), and CASCADE only for pure child rows. SET NULL is never used on composite keys.
- Case-insensitive unique email (`lower(email)`).
- The duplicate FK on `ticket_approvals.approval_rule_id` is removed.
- `audit_logs` has no FK to actors, so the log never blocks anonymising a user.
- Defaults are added: `gen_random_uuid()`, `now()`, `updated_at` columns.

**Indexes** for the hot paths: my tickets, team and assignee queues, pending approvals (by person and by role), notification inbox, conversation messages, user → tenants at login, refresh-token lookup, asset stock and history, SLA due dates, and audit by entity.

## Verified
**Revision 2.3 (2026-10-30):** the DDL exported by `@dbml/core` 10.3.1, together with `smartdesk-constraints.sql`, was applied to PGlite 0.3.14 with the real `vector` and `btree_gist` extensions: 40 tables, 57 CHECK constraints, 107 foreign keys. 38 of 38 scenarios behaved as expected, see [Audit (revision 2.3)](#audit-revision-23).

**Revision 2 (earlier run):** the exported DDL, together with `smartdesk-constraints.sql`, was applied to PostgreSQL 18 (PGlite), with `vector` swapped for `real[]` because pgvector was not available in that environment. 17 invalid writes were rejected and a valid scenario was accepted. Covered: cross-tenant reference, kind mismatch, invalid status for kind, attachment on another ticket's comment, rejection without reason, draft owner mismatch, two open assignments of one asset, overlapping SLA policy, duplicate email that differs only in case, invited membership without a token, approval rule naming both a role and a person, and more.

## Still open
- Triggers listed at the end of `smartdesk-constraints.sql` (updated_at, immutability, asset status sync, REVOKE on append-only tables).
- State transitions per kind are validated by the backend. The CHECK only guarantees a status is valid for the kind.
- Decide the behaviour for suspended tenants (deny login vs read-only).
- Retention periods for AI chats and audit logs. Consider PostgreSQL RLS as defense in depth.

## Simplifications (revision 2.1)
Tables that the use cases do not need were removed or folded in, so the schema went from 42 to 37 tables:

| Removed | Why | Replaced by |
|---|---|---|
| `user_tokens` | No use case for password reset or email verification (UC39 is changing a password while signed in) | Add it back together with a "forgot password" use case |
| `business_calendars` | AC-UC36 needs one calendar per tenant, not several | `tenants.working_hours` |
| `business_holidays` | Same, renamed and no longer per calendar | `tenant_holidays` |
| `invitations` | At most one live invitation per membership | Invite columns on `memberships` |
| `roles` | The four roles are fixed; there are no custom roles | Enum `role_code` |
| `platform_admins` | Only a flag was needed; grants are already audited | `users.is_platform_admin` |

## Alignment with API contract 0.3 (revision 2.2)
The [OpenAPI review](../api/openapi-review.md) found places where the API needs data the schema did not have. The schema went from 37 to 40 tables:

| Change | Why | API |
|---|---|---|
| New `locations` table; `memberships.location` and `assets.location` (free text) become `location_id` with composite FKs | UC03 manages locations as a list with duplicate-name errors (AC-UC03) | `/organization/locations`, `Member.locationId`, `Asset.locationId` (R12) |
| New `idempotency_records` table (scope tenant + member + method + path + key, request hash, stored response, at least 24 h) | Replaying the first response and detecting a changed body need more than `tickets.idempotency_key` | `Idempotency-Key` on `POST /tickets`, `409 IDEMPOTENCY_KEY_REUSED` (R05) |
| `TYPE_CHANGED` added to `ticket_event_type`, with a CHECK that it carries a reason and the old/new catalog versions | Triage converts a wrongly filed ticket to another request type (UC17) | `TriageCommand.targetRequestTypeId` (R07) |
| New `outbox_messages` table + partial index on pending rows | API and worker exchange notifications and KB indexing through a transactional outbox | [C4 container](../architecture/c4/02-container.md) |

Both new infrastructure tables are in the table group `api_infrastructure`. `user_sessions.refresh_token_hash` already fits the decision to send the refresh token only in an HttpOnly cookie (D15); no change was needed there.

## Audit (revision 2.3)
A second audit generated the DDL with the real DBML parser, ran it on PostgreSQL (PGlite) and compared every API enum and versioned resource with the schema.

| # | Severity | Finding | Fix |
|---|---|---|---|
| A1 | HIGH | `ck_ticket_events_type_change` accepted a `TYPE_CHANGED` event with `details` NULL: `NULL ? 'key'` is NULL, and a CHECK only rejects false | Also require `details IS NOT NULL` |
| A2 | HIGH | The API sends `expectedVersion` for 14 resources, but only `tickets` had `row_version`; two concurrent edits of an asset, approval, article, member or policy could both win | `row_version int not null default 0` on `tenants`, `users`, `memberships`, `departments`, `locations`, `it_teams`, `catalog_items`, `approval_rules`, `ticket_approvals`, `assets`, `kb_articles`, `sla_policies` |
| A3 | MEDIUM | Reason and note checks used `IS NOT NULL`, so `''` or spaces passed (only the approval reject check trimmed) | Resolution note, reopen / reject / cancel reasons, transfer / escalate reasons, type-change reason and tenant suspension reason now require `length(btrim(...)) > 0` |
| A4 | MEDIUM | `TriageCommand.category` and `Ticket.category` had no column | `tickets.category varchar(100)` |
| A5 | MEDIUM | `AIReply.kind` (grounded, no source, follow-up, ticket status) was not stored, so grounded-answer and abstention rates could not be measured | Enum `ai_reply_kind` + `ai_messages.reply_kind`, required exactly on ASSISTANT messages (`ck_ai_messages_reply_kind`) |
| A6 | LOW | UC02 profile fields `avatarUrl` and `notificationPreferences` had no columns | `users.avatar_url`, `memberships.notification_preferences jsonb` |
| A7 | LOW | API and DB disagreed on ticket link types, fulfilment step status (no SKIPPED in the API) and the change assessment (risk level vs. affected users and downtime) | API 0.4.1-draft adds `linkType`, `status` and `riskLevel`; `change_plans` adds `affected_user_count`, `estimated_downtime_minutes` |
| A8 | LOW | The DBML exporter writes `(lower(name), tenant_id)` for a mixed expression index, so per-tenant lookups cannot use the leading column | `ux_locations_name_ci` moved to `smartdesk-constraints.sql` as `(tenant_id, lower(name))` |

Scenarios run (all as expected): cross-tenant location on a member and an asset; duplicate location name ignoring case; `TYPE_CHANGED` without reason, without details, with NULL details; blank reopen, transfer, resolution and suspension text; converting a ticket with a status invalid for the new kind, with a kind that disagrees with its catalog version, and after fulfilment work started; idempotency scope duplicate, other-tenant member, short key, retention under 24 h, invalid status; outbox negative attempts and unknown tenant; assistant message without reply kind and user message with one; plus regressions from revision 2 (cross-tenant requester, two open assignments of one asset, platform session without tenant, case-insensitive duplicate e-mail).

Every API enum that maps to a stored state now has the same values as its DB enum (17 pairs compared). The full ERD lists every DBML column of all 40 tables, in DBML order.
