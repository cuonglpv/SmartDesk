# SmartDesk — Database design (revision 2)

Target logical model for PostgreSQL. This is not the implemented database yet. It is derived from [02-use-cases.md](../02-use-cases.md) and [06-acceptance-criteria.md](../06-acceptance-criteria.md).

## Files
- `smartdesk.dbml` — full schema (42 tables, 22 enums). Import it at https://dbdiagram.io/; table groups keep the diagram readable.
- `smartdesk-constraints.sql` — partial unique indexes, exclusion constraint and vector index that DBML cannot express. Run it after the DDL exported from the DBML.
- `smartdesk-full-erd.mmd` — Mermaid ERD of all 42 tables and every column, generated from the DBML. Open it at https://mermaid.live/.
- `smartdesk-core-erd.mmd` — 23 core tables, showing only keys and state columns.

Reading the ERDs:
- Edges to `tenants` are hidden, because every table except `tenants` and `users` carries `tenant_id`.
- `||` means a required reference and `|o` an optional one (the FK column is nullable, also marked `"nullable"`). `o|` on the child side means 1:1, for example `ticket_sla` and `change_plans`.
- Each label is the role the parent plays, for example `requester`, `assigned`, or `approver`.
- The core view also leaves out bookkeeping actors such as `created by` and `published by`.

Generate the DDL with:

```bash
npx @dbml/cli dbml2sql smartdesk.dbml --postgres -o smartdesk.sql
```

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
- `invitations` and `user_tokens` — invite by email (UC04) and password reset. `users.password_hash` is nullable until the invite is accepted.
- `ticket_sla.*_warning_sent_at` — one notification per SLA threshold (UC37). `notifications.dedupe_key` is unique as a second guard.
- KB review fields (`submitted_at`, `reviewed_by`, `review_comment`), with a CHECK that the reviewer is not the author (UC34).
- `kb_chunks` — embeddings of published KB versions for AI retrieval.
- `tickets.source` (PORTAL / AI_ASSISTANT), `tenant_counters` for `ticket_no`, `tenants.suspended_reason`.
- `business_calendars` and `business_holidays` replace the per-policy `business_calendar` JSON.

**Single source of truth**
- Removed `catalog_versions.needs_approval`. Approval is decided only by `approval_rules`, which are append-only (`effective_from/to`) and support approval steps.
- `kind` is enforced along catalog item → version → ticket.
- Removed `fulfilment_tasks` (it was 1:1 with the ticket and duplicated the assignee). `fulfilment_steps` hang directly off the ticket.
- Removed `RETURNED` from the asset status: a returned device is `AVAILABLE` again.
- `approval_rules.approver_role` (varchar) became `approver_role_id → roles`.
- `sla_policies` are append-only and cannot overlap in time (exclusion constraint).

**Integrity**
- 22 enums replace free-text status and type columns. `tickets` has a CHECK that each status is valid for the ticket kind.
- 49 CHECK constraints, for example: rejection needs a reason; resolving needs a resolution note; REOPENED, CANCELLED, TRANSFERRED and ESCALATED events need a reason; a ticket cannot link to itself; a RELATED link is stored only once.
- Deletion policy is explicit: no hard deletes (NO ACTION by default), and CASCADE only for pure child rows. SET NULL is never used on composite keys.
- Case-insensitive unique email (`lower(email)`).
- The duplicate FK on `ticket_approvals.approval_rule_id` is removed.
- `audit_logs` has no FK to actors, so the log never blocks anonymising a user.
- Defaults are added: `gen_random_uuid()`, `now()`, `updated_at` columns.

**Indexes** for the hot paths: my tickets, team and assignee queues, pending approvals (by person and by role), notification inbox, conversation messages, user → tenants at login, refresh-token lookup, asset stock and history, SLA due dates, and audit by entity.

## Verified
The exported DDL, together with `smartdesk-constraints.sql`, was applied to PostgreSQL 18 (PGlite), with `vector` swapped for `real[]` because pgvector was not available in that environment. 15 invalid writes were rejected and a valid scenario was accepted. Covered: cross-tenant reference, kind mismatch, invalid status for kind, attachment on another ticket's comment, rejection without reason, draft owner mismatch, two open assignments of one asset, overlapping SLA policy, duplicate email that differs only in case, and more.

## Still open
- Triggers listed at the end of `smartdesk-constraints.sql` (updated_at, immutability, asset status sync, REVOKE on append-only tables).
- State transitions per kind are validated by the backend. The CHECK only guarantees a status is valid for the kind.
- Decide the behaviour for suspended tenants (deny login vs read-only).
- Retention periods for AI chats and audit logs. Consider PostgreSQL RLS as defense in depth.
