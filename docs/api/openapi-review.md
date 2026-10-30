# SmartDesk OpenAPI 0.2.0-draft — Review

> **Reviewed:** [`openapi.yaml`](openapi.yaml), [`README.md`](README.md), [`traceability.md`](traceability.md) · 2026-10-30  
> **Checked against:** [use cases](../02-use-cases.md), [acceptance criteria](../06-acceptance-criteria.md), [database design rev. 2](../database/README.md)  
> **Status of the contract:** PROPOSED. There is no backend, so every finding is about the design, not about running code.  
> **Resolution:** the findings below were found in **0.2.0-draft**. Contract **0.3.0-draft** applies the fixes, and **0.4.0-draft** applies decision D15; see [§8](#8-resolution-in-030-draft) and [§9](#9-follow-ups-done-in-040-draft-and-database-revision-22).

## 1. Verdict

The contract is well organised and safe by default: tenant comes only from the session, every request body has `additionalProperties: false`, every command carries `expectedVersion`, errors use RFC 9457 Problem Details, the AI cannot write, and 43/43 use cases are mapped. It is a good base.

It is **not ready to implement yet**. The main risk is not the OpenAPI syntax but **drift between the API and the database design** (revision 2 was written after the API draft): enums, roles, versions and idempotency storage disagree. Fix the 8 HIGH findings before generating server stubs or DTOs.

| Severity | Count | Meaning |
|---|---:|---|
| HIGH | 8 | Blocks implementation, or the API and DB cannot both be right |
| MEDIUM | 8 | Will cause bugs or rework in the first sprint that touches it |
| LOW | 7 | Style, tooling and consistency |

Finding types: **CD** = contract defect (fix the YAML), **SC** = source contradiction (API, DB, UC or AC disagree; someone must choose), **OD** = open product decision.

## 2. What was checked

| Check | Result |
|---|---|
| Counts | 85 paths, 99 operations (P0 49 · P1 43 · P2 7), 134 schemas, 17 shared examples |
| Request bodies with `additionalProperties: false` | 100% |
| Operations with `x-roles`, `x-permissions`, `x-data-scope`, `x-use-cases` | 99/99 |
| Protected operations with `401` / path-param operations with `404` | 99/99 / all |
| Protected operations with permissions but no `403` | 4 (`signOut`, `getMyProfile`, `listMyNotifications`, `markNotificationRead`) — acceptable, they are self-scoped |
| Unused schemas | `ErrorResponse` (deprecated on purpose), `TicketCommentList` |
| `201` responses with a `Location` header | 0 of 14 |
| Operations with `429` | 8 |
| Operations with `503` | 0 |
| Enum and column cross-check against `docs/database/smartdesk.dbml` | 8 mismatches (R01–R03, R05, R07, R09, R10, R12) |

The script parsed the YAML and walked every operation and schema. It is not a substitute for `npx @redocly/cli lint docs/api/openapi.yaml`, which has still not been run.

## 3. HIGH findings

### R01 — Persisted enums differ from the database · SC

| API schema | API values | DB enum | DB values |
|---|---|---|---|
| `AssetStatus` | AVAILABLE, **RESERVED**, ASSIGNED, **RETURNED**, **MAINTENANCE**, RETIRED | `asset_status` | AVAILABLE, ASSIGNED, **IN_MAINTENANCE**, RETIRED, **LOST** |
| `ArticleVisibility` | **ALL_MEMBERS**, IT_ONLY, **DEPARTMENTS** | `kb_visibility` | **ALL_EMPLOYEES**, IT_ONLY |
| `RequestType.status` | DRAFT, PUBLISHED, **HIDDEN** | `catalog_version_status` | DRAFT, PUBLISHED, **RETIRED** |
| `Approval.status` | PENDING, APPROVED, REJECTED | `approval_status` | + **CANCELLED** |

`POST /assets/{assetId}/reserve` (UC29) has no state to write in the DB, and the DB removed `RETURNED` on purpose ("a returned device is AVAILABLE again"). Department-scoped articles (`DEPARTMENTS` + `departmentIds`) have no columns in the DB, so retrieval cannot filter them.

**Fix.** Treat DB revision 2 as the source for stored states and update the API, except where the API carries a real requirement: add `RESERVED` to `asset_status` (or model a reservation as a pending `asset_assignments` row), and either add department visibility to the DB or drop `DEPARTMENTS` from the API. Add `CANCELLED` to `Approval.status`.

### R02 — `Version` minimum is 1, the DB starts at 0 · CD

`components.schemas.Version` has `minimum: 1`; `tickets.row_version` and the other versioned tables have `default: 0`. The first response after a create would violate the schema, and a client sending `expectedVersion: 0` gets `400`.

**Fix.** Pick one. Simplest: `Version.minimum: 0`, or change every `row_version` default to 1.

### R03 — One role per session, many roles per membership · SC

`TokenPair.role`, `Member.role` and `MemberPatch` carry a single `Role`. The DB has `membership_roles` (many-to-many with `role_code`), and real tenants have IT Managers who also act as IT Staff.

**Fix.**

```yaml
TokenPair:
  properties:
    roles:
      type: array
      minItems: 1
      uniqueItems: true
      items: { $ref: '#/components/schemas/Role' }
```

Do the same for `Member` and `MemberPatch`, and keep the rule "the last active ORG_ADMIN cannot lose the role" (T19).

### R04 — IT Manager cannot find articles waiting for review · CD

UC34 (P0) needs the reviewer to list `IN_REVIEW` articles and read the draft body. The only listing of non-published articles is `GET /it/kb/articles` with `x-roles: [IT_STAFF]` and `kb.draft`; `GET /kb/articles` returns only published ones. The `publish`, `return` and `retire` commands exist, but the manager has no way to discover or read what to approve.

**Fix.** Add `GET /manager/kb/articles?status=IN_REVIEW` (`listArticlesForReview`) and `GET /manager/kb/articles/{articleId}` (`getArticleForReview`), both with `kb.publish`.

### R05 — Idempotency cannot be implemented on the current schema · SC

The API promises: scope tenant + actor + method + path, key 16–128 characters, stored payload hash and original response for at least 24 h, `409 IDEMPOTENCY_KEY_REUSED` when the body differs. The DB has only `tickets.idempotency_key varchar(100)` with a unique index per requester. It cannot store the payload hash, cannot replay the original response, cannot hold a 101–128 character key, and the key lives forever instead of 24 h.

**Fix.** Add a small `idempotency_records` table (`tenant_id, membership_id, method, path, key, request_hash, response_status, response_body, created_at`, unique on the first five), cleaned up by the worker, or at minimum add `tickets.idempotency_request_hash char(64)` and set both maximum lengths to the same value.

### R06 — Three different error-code lists · CD

| Where | Codes |
|---|---|
| `x-error-codes` | `VALIDATION_ERROR`, `INVALID_CREDENTIALS`, `FORBIDDEN`, `NOT_FOUND`, `FILE_TOO_LARGE` (under **400**) |
| Shared examples | `VALIDATION_FAILED`, `AUTHENTICATION_FAILED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `UPLOAD_TOO_LARGE` (**413**), `RATE_LIMIT_EXCEEDED`, `INTERNAL_SERVER_ERROR` |
| README §7 | same as the examples |

`ProblemDetails.errorCode` is a free `string`, and the README tells the frontend to branch on `errorCode`. With three lists, the frontend and backend will disagree on day one.

**Fix.** One schema, referenced from `ProblemDetails.errorCode`, and delete `x-error-codes`:

```yaml
ErrorCode:
  type: string
  enum: [VALIDATION_FAILED, UNSUPPORTED_FILE_TYPE, AUTHENTICATION_FAILED, SESSION_EXPIRED,
         ACCESS_DENIED, TENANT_SUSPENDED, RESOURCE_NOT_FOUND, INVALID_TRANSITION,
         CONCURRENT_MODIFICATION, IDEMPOTENCY_KEY_REUSED, CATALOG_VERSION_STALE,
         APPROVAL_REQUIRED, ALREADY_DECIDED, ASSET_NOT_AVAILABLE, DUPLICATE_ASSET_TAG,
         UPLOAD_TOO_LARGE, RATE_LIMIT_EXCEEDED, AI_UNAVAILABLE, INTERNAL_SERVER_ERROR]
```

### R07 — Triage "convert type" cannot be stored · CD

UC17 allows converting a wrongly filed ticket ("a request filed as incident"). `TriageCommand` accepts a new `ticketType` and a `reason`, but the DB pins `tickets.kind` to the catalog version through a composite FK, and the three kinds have different status sets (`ck_tickets_status_per_kind`). Changing only the type breaks both. `category` is also a free string, while `RequestCategory` is an enum.

**Fix.** Replace `ticketType` with `targetRequestTypeId` + `targetRequestTypeVersion`; the server re-validates `answers` against the new form, resets the status to the initial status of the new kind, and writes a `TYPE_CHANGED` event. Make `reason` required with OAS 3.1 `if/then` when the target differs. Use `RequestCategory` for `category`.

### R08 — Session lifecycle is incomplete · CD + OD (D15)

- `TokenPair` has no refresh token although its name says "pair"; the example lifetime is 900 s and there is no refresh operation, so users must sign in again every 15 minutes.
- There is no way for a Platform Admin to obtain a session: `signIn` returns tenant sessions, the description says platform sessions are isolated, but there is no separate operation or security scheme, and `signOut` lists only tenant roles.

**Fix.** Decide the transport first (recommended for a browser SPA: HttpOnly, `SameSite=Lax` session cookie + CSRF token, which also removes token storage in JavaScript). Then add `POST /auth/refresh` (or document sliding sessions), add a `PlatformSession` security scheme used only by `/platform/**`, and add `POST /platform/auth/sign-in`.

## 4. MEDIUM findings

| # | Type | Where | Problem | Fix |
|---|---|---|---|---|
| R09 | SC | `RequestType.approvalRequired`, `slaTargetMinutes`, `RequestTypeInput` | DB rev. 2 removed `catalog_versions.needs_approval`: approval comes only from `approval_rules`, SLA only from `sla_policies`. The API keeps a second, writable copy. | Make both `readOnly` and computed ("preview" for the form, as UC07 shows them); remove them from the input schemas. |
| R10 | SC | `TicketDraft`, `CreateTicket` | DB stores `ai_ticket_drafts` with `status` and `submitted_ticket_id`, but `TicketDraft` has no `id` and `CreateTicket` only has `assistantConversationId`, so the server cannot tell which draft was submitted. UC14 also says "discard → nothing stored", which contradicts the DB. | Add `TicketDraft.id` and `CreateTicket.aiDraftId`; add `POST /ai/conversations/{conversationId}/drafts/{draftId}/discard`; change UC14 to "discard → draft marked DISCARDED". |
| R11 | CD | `askAI`, `prepareAITicketDraft` | No `503`/`504` when the LLM or embedding provider is down or slow. The client cannot show "assistant unavailable, use the catalog" and retries on `500`. | Add `Err503` with `errorCode: AI_UNAVAILABLE` and `Retry-After`; state a server time budget (for example 20 s). |
| R12 | SC | `/organization/locations`, `Member.locationId`, `Asset.locationId` | The API has a Location resource with UUIDs; the DB has only `location varchar(150)` on memberships and assets. | Add a `locations` table, or drop the resource and use a string. |
| R13 | CD | `ApprovalCommand.reason`, `TriageCommand.reason` | "Required for REJECT" is only prose. OAS 3.1 can express it, and generated validators will then enforce it. | `if: {properties: {decision: {const: REJECT}}}` → `then: {required: [reason], properties: {reason: {minLength: 1}}}`. |
| R14 | CD | `Attachment`, `downloadTicketAttachment` | No `visibility`, `commentId` or `scanStatus`. The DB has `attachment_scan_status` (PENDING/CLEAN/INFECTED), but the API does not say what a download of a PENDING or INFECTED file returns. Hiding internal files relies only on prose. | Add `scanStatus` and `visibility`; return `409 FILE_NOT_READY` for PENDING and `404` for INFECTED. |
| R15 | CD | `Ticket` | One schema serves both the requester and IT views and includes `tenantId`. Requester responses must not carry IT-only fields (team, internal counters, later SLA internals). | Split `RequesterTicket` and `ItTicket`; drop `tenantId` from both (the client already knows its tenant). |
| R16 | CD | `TicketStatus` | One 16-value enum for three kinds. The schema accepts `SCHEDULED` on an incident. | Keep one enum for the wire, but document per-kind sets with `x-allowed-by-kind`, or use `oneOf` discriminated by `ticketType`. |

## 5. LOW findings

| # | Problem | Fix |
|---|---|---|
| R17 | 14 `201` responses have no `Location` header; a replayed `POST /tickets` cannot be told apart from the first call. | Add `Location`; add `Idempotent-Replayed: true` on replay. |
| R18 | OAS 3.1 style: 5 schemas use the deprecated `example` keyword; 3 binary payloads use `format: binary`. | Use `examples: [...]`; use `contentMediaType` (and drop the schema for raw bodies). |
| R19 | Generic `{id}` path parameter for approvals, conversations, notifications, attachments and org records, next to `{ticketId}` and `{assetId}`. | Use specific names (`{approvalId}`, `{conversationId}` ...). Generated clients and logs become clearer. |
| R20 | `x-data-scope: PRE_AUTH_OR_SESSION` on `signOut`, which requires a session. | `AUTHENTICATED_USER_IN_TENANT`. |
| R21 | `429` on only 8 operations; `POST /tickets` and `POST /tickets/{ticketId}/comments` have none. | Either add `429` to all write operations or document that rate limits are global. |
| R22 | Remove `TicketCommentList` (unused) and plan the removal of the deprecated `ErrorResponse`. | — |
| R23 | Path prefixes follow UI areas (`/it`, `/manager`, `/admin`); a KB article has three base paths. | Acceptable. Authorization must never depend on the prefix; the C3 design maps all three to one KB module. |

## 6. Open product decisions — recommendation

These are already listed as D01–D16 in [review-guide.md](review-guide.md). Recommendations for the ones that block P0:

| # | Decision | Recommendation |
|---|---|---|
| D01 | Suspended tenant: deny sign-in (AC-UC01) or read-only (AC-UC41) | Deny with generic `401` for Release 1 (fail closed, simpler); revisit read-only with UC41 in P2. Update AC-UC41. |
| D03 | Reopen a SERVICE_REQUEST | Allow reopen only for INCIDENT; a service request that was not fulfilled correctly becomes a new linked request. Update AC-UC10. |
| D05 / §6 README | Oversize upload `400` (AC-UC07) or `413` | Keep `413 UPLOAD_TOO_LARGE`; change AC-UC07. |
| D04 | Delegated approvers | IT_MANAGER only in Release 1; `approval_rules.approver_membership_id` enables delegation in P1. |
| D15 | Token transport | **Decided:** refresh token only in an HttpOnly cookie, CSRF double submit (0.4.0-draft). |

## 7. Order of work

1. Align API and DB: R01, R02, R03, R05, R12, R09.
2. Close functional gaps: R04, R07, R10, R11.
3. One error catalogue: R06, then regenerate examples.
4. Decide auth transport and platform sessions: R08 / D15.
5. Run `npx @redocly/cli lint docs/api/openapi.yaml` and fix what it reports, then the LOW items.

The C4 design in [`../architecture/c4/`](../architecture/c4/README.md) already assumes these fixes; where it depends on one, it says so.

## 8. Resolution in 0.3.0-draft

Applied by a scripted patch of `openapi.yaml`, so the rest of the file is byte-for-byte unchanged. Re-checked afterwards: every `$ref` resolves, path parameters match their declarations, `operationId`s are unique, all 135 schemas pass the JSON Schema 2020-12 meta-schema, and **524 request/response examples validate against their schemas** with 0 errors (0.2 had 498). Every `errorCode` in an example or description is in `ErrorCode`. The Redocly lint has still not been run.

Result: **105 operations, 91 paths, 135 schemas** (P0 53 · P1 45 · P2 7); 43/43 use cases still mapped ([traceability.md](traceability.md) regenerated).

| # | Status | What changed in the contract | Still needed outside the contract |
|---|---|---|---|
| R01 | Fixed | `AssetStatus` = AVAILABLE, ASSIGNED, IN_MAINTENANCE, RETIRED, LOST; `ArticleVisibility` = ALL_EMPLOYEES, IT_ONLY (`departmentIds` removed); `RequestType.status` = DRAFT, PUBLISHED, RETIRED plus `visible` (= `catalog_items.is_visible`, set by `/hide`); `Approval.status` + CANCELLED. `POST /assets/{assetId}/reserve` removed: UC29 needs only an AVAILABLE asset, and a concurrent handover is already a `409` | — |
| R02 | Fixed | `Version.minimum: 0` | — |
| R03 | Fixed | `roles: Role[]` on `TokenPair`, `Member`, `Profile`, `Invitation`, `InviteMember`, `MemberPatch`; `Role` has the 4 tenant roles only; `409 LAST_ORG_ADMIN` | — |
| R04 | Fixed | `GET /manager/kb/articles` (`listArticlesForReview`), `GET /manager/kb/articles/{articleId}` (`getArticleForReview`) | — |
| R05 | Fixed (API) | `Idempotency-Key` 16–100 characters; `Idempotent-Replayed` response header | **DB:** add `idempotency_records` (request hash + stored response, 24 h) |
| R06 | Fixed | `ErrorCode` enum referenced by `ProblemDetails.errorCode`; `x-error-codes` removed | — |
| R07 | Fixed (API) | `TriageCommand`: `targetRequestTypeId` → `targetRequestTypeVersion`, `answers`, `reason` required together (`dependentRequired`); status restarts at the initial status of the new kind. `category` stays free text: it is IT's finer classification, not `RequestCategory` | **DB:** add `TYPE_CHANGED` to `ticket_event_type` |
| R08 | Fixed (D15 decided in 0.4) | `refreshToken` in `TokenPair`, `POST /auth/refresh` with rotation and re-use detection (matches `user_sessions.refresh_token_hash`); `PlatformSession` scheme on every `/platform/**` operation; `POST /platform/auth/sign-in`, `/refresh`, `/sign-out` | **D15:** refresh token in the body or only in an HttpOnly cookie |
| R09 | Fixed | `approvalRequired`, `slaTargetMinutes` are `readOnly`, computed; removed from `RequestTypeInput` and `RequestTypePatch` | — |
| R10 | Fixed (API) | `TicketDraft.id` and `status`; `CreateTicket.aiDraftId` replaces `assistantConversationId`; `POST /ai/conversations/{conversationId}/drafts/{draftId}/discard` | **Docs:** change UC14 "discard → nothing stored" to "draft marked DISCARDED" |
| R11 | Fixed | `Err503` (`AI_UNAVAILABLE`, `Retry-After`) on `askAI` and `prepareAITicketDraft` | — |
| R12 | Kept in API | `/organization/locations` stays, because UC03 and AC-UC03 manage locations as a list with duplicate-name errors | **DB:** add a `locations` table; replace `memberships.location` and `assets.location` with `location_id` |
| R13 | Fixed | `ApprovalCommand`: `if decision = REJECT then reason required, minLength 1`; triage reason via `dependentRequired` | — |
| R14 | Fixed | `Attachment.visibility`, `scanStatus`, `commentId`; download returns `409 FILE_NOT_READY` while PENDING, `404` when INFECTED | — |
| R15 | Fixed | `tenantId` removed from `Ticket` and `Asset` (and from the examples). No field of `Ticket` is IT-only today, so one schema is kept | — |
| R16 | Fixed | `TicketStatus.x-allowed-by-kind` mirrors `ck_tickets_status_per_kind` | — |
| R17 | Fixed | `Location` header on the 201s whose resource has a read endpoint (`createTicket`, `createAsset`, `createTenant`); `Idempotent-Replayed` on `createTicket` | — |
| R18 | Fixed | `examples: [...]` in schemas; `contentMediaType` for the upload; raw binary responses have no schema | — |
| R19 | Fixed | `{id}` → `{notificationId}`, `{departmentId}`, `{locationId}`, `{teamId}`, `{memberId}`, `{approvalRuleId}`, `{attachmentId}`, `{approvalId}`, `{conversationId}`, `{slaPolicyId}` | — |
| R20 | Fixed | `signOut` scope `AUTHENTICATED_USER_IN_TENANT` | — |
| R21 | Fixed | `429` on `createTicket` and `addTicketComment` | Rate-limit numbers per policy |
| R22 | Fixed | `TicketCommentList` removed; deprecated `ErrorResponse` kept for one more draft | — |
| R23 | No change | Prefixes stay; the C3 design maps all KB prefixes to one module | — |

**Database follow-ups in one list:** `idempotency_records` (R05), `TYPE_CHANGED` event type (R07), `locations` table (R12), `outbox_messages` (C4 container design). All four are done in database revision 2.2, see §9.

## 9. Follow-ups done in 0.4.0-draft and database revision 2.2

| Item | Done |
|---|---|
| D15 refresh-token transport | Refresh token only in the `sd_refresh` / `sd_platform_refresh` HttpOnly cookies (`SameSite=Strict`, path-scoped); `X-CSRF-Token` double submit on the refresh endpoints; `TokenPair` → `AccessSession` without a refresh token; `RefreshInput` removed. 105 operations, 91 paths, 134 schemas; 524 examples still validate. |
| R05 | `idempotency_records` in [smartdesk.dbml](../database/smartdesk.dbml) (scope, request hash, stored response, ≥ 24 h) |
| R07 | `TYPE_CHANGED` in `ticket_event_type` + CHECK `ck_ticket_events_type_change` (reason and old/new catalog version) |
| R12 | `locations` table; `memberships.location_id`, `assets.location_id` with composite FKs |
| Outbox | `outbox_messages` + partial index `ix_outbox_pending` |
| R10 wording | UC14 alternative and AC-UC14 now say the draft is marked `Discarded`; the contract returns `409` when a discarded draft is submitted |

The database went from 37 to 40 tables (see the [database README](../database/README.md)). A structural check of the DBML passed (every table grouped, every FK target column exists and is unique); the DDL has not been regenerated with `@dbml/cli` or re-run on PGlite.

**Later (database revision 2.3, contract 0.4.1-draft):** a second database audit regenerated the DDL, ran 38 write scenarios on PGlite and fixed eight more issues, including optimistic-locking columns for every versioned resource; see the [database audit](../database/README.md#audit-revision-23).
