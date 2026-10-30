# SmartDesk — API Documentation

> **Contract:** [`openapi.yaml`](openapi.yaml) · OpenAPI **3.1.0** · proposed version **0.4.1-draft** (fixes from [openapi-review.md](openapi-review.md), see §12)  
> **Implementation:** **DESIGN ONLY**. SmartDesk has requirements, diagrams and a mock-data frontend prototype, **not** an implemented backend. All base URLs and example UUIDs are illustrative.  
> **Product source:** [SmartDesk](https://github.com/cuonglpv/SmartDesk) · **Documentation approach reference:** [finance-manager/docs/api](https://github.com/PhamHiep948/finance-manager/tree/main/docs/api)

## 1. Documentation files

The contract lives in the SmartDesk repository as:

```text
SmartDesk/
└── docs/
    └── api/
        ├── openapi.yaml                 # the contract (source of truth for HTTP interfaces)
        ├── README.md                    # this guide
        ├── traceability.md              # UC01–UC43 → operations, generated from x-use-cases
        ├── review-guide.md              # review checklist and open decisions D01–D16
        └── openapi-review.md            # review findings R01–R23 and how each was resolved
```

The OpenAPI YAML is the **source of truth for proposed HTTP interfaces**, not proof of implementation. The use cases and acceptance criteria remain the source of truth for intended behavior. Design assumptions and document contradictions are explicitly tracked rather than silently treated as requirements.

## 2. API modules

| Area | Representative resources / capabilities | Priority |
|---|---|---|
| Authentication & profile | `/auth/sign-in`, `/auth/select-tenant`, `/auth/refresh`, `/auth/sign-out`, `/me` | P0 |
| Organization & members | `/organization`, `/organization/members`, `/organization/teams` | P0+ |
| Service catalog | `/catalog/request-types`, `/admin/request-types` | P0/P1 |
| Employee tickets | `/tickets`, `/tickets/my`, `/tickets/{ticketId}` | P0 |
| IT workspace | `/it/tickets`, `/it/tickets/{ticketId}/triage`, `/it/tickets/{ticketId}/resolve` | P0 |
| Approval & fulfilment | `/approvals`, `/assets/{assetId}/handover`, `/it/tickets/{ticketId}/fulfilment-steps` | P0/P1 |
| Asset management | `/assets/my`, `/assets`, `/assets/{assetId}/history` | P0/P1 |
| Knowledge base | `/kb/articles`, `/it/kb/articles` (authoring), `/manager/kb/articles` (review queue, publish) | P0/P1 |
| AI self-service | `/ai/conversations`, `/ai/conversations/{conversationId}/messages`, `.../ticket-draft`, `.../drafts/{draftId}/discard` | P0 |
| SLA & reports | `/sla/policies`, `/sla/alerts`, `/reports/operations` | P1 |
| SaaS platform | `/platform/auth/*`, `/platform/tenants`, `/platform/audit-logs` (platform session only) | P1/P2 |

**Important:** The entire contract covers 105 proposed operations over 91 paths (P0 53 · P1 45 · P2 7), supporting all 43 mapped use cases. This is *not* the same as asserting that all 105 operations are necessary to launch the P0 MVP; `x-release` records an operation's earliest intended release, and multi-use-case endpoints require feature gating.

## 3. Base URL and transport

- The YAML declares the **example** server `https://api.smartdesk.example/v1`; there is no live public endpoint.
- For local development, teams can configure an environment-specific base URL (for example, `http://localhost:5000/v1`) **after** creating a backend. These URLs are examples, not tested addresses.
- Requests and successful JSON responses use `application/json`. File uploads use `multipart/form-data`. Errors use `application/problem+json`. CSV/PDF reports return their respective media types.
- All timestamps must be ISO 8601 with an offset or `Z`; timezone calculations for SLA use the tenant's configured business calendar.

## 4. Authentication and tenant boundary

Protected endpoints use `Authorization: Bearer <access_token>`; the contract does not yet prescribe whether that token is opaque or JWT. A successful sign-in may return a tenant-selection challenge when the identity belongs to multiple organizations. The selected tenant is validated and bound to the resulting authenticated session.

**Never accept a tenant ID from a client header/body/query as an authorization authority.** Derive tenant context from the verified session. Platform Admin tokens are a separate administrative security context and must not grant access to private tenant tickets, articles, attachments, or assets.

Sessions are a short-lived **access token** in the JSON body (`AccessSession`), which the SPA keeps in memory only, plus a **rotating refresh token that is never in a body**: it is the `sd_refresh` cookie (`HttpOnly; Secure; SameSite=Strict; Path=/v1/auth`), stored server-side only as `user_sessions.refresh_token_hash`. `POST /auth/refresh` takes no body; it needs the cookie and an `X-CSRF-Token` header equal to the readable `sd_csrf` cookie (double submit, otherwise `403`). Each refresh rotates the cookie; re-use of a revoked refresh token revokes the whole session (`401`). Sign-out clears both cookies. A membership can hold several roles, so the session returns `roles: []`.

**Platform Admins** sign in with `POST /platform/auth/sign-in` and receive a `PlatformSession` (security scheme `PlatformSession`) plus the `sd_platform_refresh` cookie scoped to `/v1/platform/auth`. Only `/platform/**` accepts a platform session, and `/platform/**` accepts nothing else.

Decided (D15, 2026-10-30): the refresh token travels only in the HttpOnly cookie. CORS allows the SmartDesk web origin with credentials, and only the refresh endpoints need `credentials: 'include'`. Still open: access-token format (opaque or JWT) and the exact lifetimes. Do not copy the finance-manager single-workspace 30-minute JWT choices into SmartDesk without deciding these.

> **Document conflict requiring product decision:** `AC-UC01` says suspended tenant sign-in returns `401`; `AC-UC41` allows read-only login. Contract 0.3 preserves the fail-closed `401` choice from the earlier draft. This is a *temporary contract assumption*, not a resolved requirement.

## 5. Roles and authorization

| Capability | Employee | IT Staff | IT Manager | Org Admin | Platform Admin |
|---|:---:|:---:|:---:|:---:|:---:|
| Self-service, own tickets, visible KB, AI | ✓ | ✓ | ✓ | ✓ | — |
| Ticket queue, triage, assign, resolve | — | ✓ | ✓ | — | — |
| Fulfilment, asset write and handover | — | ✓ | Read-only asset register | — | — |
| Knowledge draft and review submission | — | ✓ | — | — | — |
| Knowledge publish/retire | — | — | ✓ | — | — |
| Approval decisions, SLA, reports | — | — | ✓ | — | — |
| Organization members, settings, catalog editor | — | — | — | ✓ | — |
| Tenant creation, tenant lifecycle and platform audit | — | — | — | — | ✓ |

Every operation contains:

- `x-roles`: **coarse informational** list of roles which could have access;
- `x-permissions`: exact capability authorization metadata (the authoritative *capability gate*);
- `x-data-scope`: identity/tenant/ownership scope classification;
- `x-use-cases`: UC identifiers used to cross-check `AC-UCxx`;
- `x-release`: earliest proposed release;
- `x-implementation-status`: always `PROPOSED`.

An allowed role is **not** enough: apply tenant checks, resource ownership, workflow state, article visibility, assignment scope, and record-level approval policies **on the server for every call**. For an unauthorized cross-tenant resource, return the same `404` as for a genuinely unknown ID. Requester ticket views must never leak IT-only notes or file metadata.

## 6. Request/response conventions

**Pagination:** `page` starts at 1 (default 1), `pageSize` defaults to 20 and is at most 100. Paginated results use `{ "items": [], "pageInfo": { "page": 1, "pageSize": 20, "total": 0, "hasNext": false } }`. Empty lists return `200` with `items: []`, not `404`. Tenant/ownership filtering happens **before** pagination and counting.

**Idempotency:** `POST /tickets` requires `Idempotency-Key` (16–100 characters, the size of the stored column). The server stores the first response and request hash for at least 24 hours in a scope including tenant, actor, HTTP method and path. Retrying the same request/key returns the original response with `Idempotent-Replayed: true`; reusing the same key for a changed payload returns `409 IDEMPOTENCY_KEY_REUSED`. The AI never submits a ticket; the employee must explicitly call the create endpoint.

**Concurrency:** Business commands use JSON `expectedVersion`. Versions start at `0` on create, like `row_version` in the database. A stale version returns `409 CONCURRENT_MODIFICATION`. This draft uses version fields rather than `ETag`/`If-Match` + `412`; do not mix mechanisms silently.

**Uploads:** `/uploads` accepts only approved images/PDF/TXT/LOG files within the configured 10 MiB limit. Upload ownership, expiration and final attachment authorization are mandatory. **Known mismatch:** AC-UC07 says oversize upload `400`, while this contract uses `413` for HTTP consistency; product/backend team should reconcile the AC before implementing.

**Export:** `/reports/operations/export` supports CSV/PDF data. Filter semantics must match `/reports/operations` to avoid showing different totals. Exports must respect tenant scoping and avoid unauthorized data.

## 7. Error contract — Problem Details

All documented error responses use `Content-Type: application/problem+json` and the `ProblemDetails` schema (RFC 9457, compatible with the RFC 7807 shape), including `errorCode` and `traceId` extensions. `errorCode` is the `ErrorCode` enum in the contract; it is the only list of codes.

```json
{
  "type": "https://api.smartdesk.example/problems/concurrent-modification",
  "title": "Conflict",
  "status": 409,
  "detail": "This record has changed. Reload it and try again.",
  "errorCode": "CONCURRENT_MODIFICATION",
  "traceId": "trace-demo-409"
}
```

Validation responses may include `errors`, an object mapping field names to arrays of messages; a frontend should use `errorCode`, not parse the human-readable `detail`. This replaces the prior custom `{ code, message, fieldErrors }` shape from contract `0.1`. The previous shape is retained as **deprecated documentation**, not as a supported response type.

| Status | Meaning | Example code |
|---|---|---|
| 400 | Invalid input / required fields | `VALIDATION_FAILED` |
| 401 | No valid tenant-bound session | `AUTHENTICATION_FAILED` |
| 403 | Missing capability, forbidden operation | `ACCESS_DENIED` |
| 404 | Missing OR not visible to the caller | `RESOURCE_NOT_FOUND` |
| 409 | Invalid business state / stale version / replay mismatch | `CONCURRENT_MODIFICATION` |
| 413 | Upload exceeds configured limit | `UPLOAD_TOO_LARGE` |
| 429 | Rate limiting | `RATE_LIMIT_EXCEEDED` |
| 500 | Unexpected server error | `INTERNAL_SERVER_ERROR` |
| 503 | AI provider unavailable or too slow (assistant endpoints only) | `AI_UNAVAILABLE` |

Other `409` codes: `INVALID_TRANSITION`, `IDEMPOTENCY_KEY_REUSED`, `CATALOG_VERSION_STALE`, `APPROVAL_REQUIRED`, `ALREADY_DECIDED`, `ASSET_NOT_AVAILABLE`, `DUPLICATE_ASSET_TAG`, `LAST_ORG_ADMIN`, `FILE_NOT_READY`.

## 8. Example API calls

These are **sample calls for future implementations**, not live commands that will succeed against the illustrative hostname. Replace the variables and UUIDs with real values after implementing a backend.

### 8.1 Sign in

```bash
API_BASE="http://localhost:5000/v1"  # illustrative only
curl -X POST "$API_BASE/auth/sign-in" \
  -H "Content-Type: application/json" \
  -d '{"email":"employee@example.com","password":"example-password"}'
```

If the identity belongs to several workspaces, sign-in yields a `TENANT_SELECTION_REQUIRED` response. Complete the login using `/auth/select-tenant` and the short-lived, single-use challenge; do not send a free-form tenant header on later calls.

Sign-in sets the `sd_refresh` and `sd_csrf` cookies. Before the access token expires, rotate it with the cookies and the CSRF header (with curl, keep the cookies in a jar):

```bash
curl -X POST "$API_BASE/auth/refresh" \
  -b cookies.txt -c cookies.txt \
  -H "X-CSRF-Token: $(awk '$6=="sd_csrf"{print $7}' cookies.txt)"
```

Add `-c cookies.txt` to the sign-in call above so the jar is filled.

### 8.2 View own tickets

```bash
ACCESS_TOKEN="REPLACE_WITH_REAL_TOKEN"
curl -X GET "$API_BASE/tickets/my?page=1&pageSize=20" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 8.3 Create an incident (human action)

```bash
curl -X POST "$API_BASE/tickets" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: sample-unique-ticket-key-00000001" \
  -d '{
    "requestTypeId": "44444444-4444-4444-8444-444444444444",
    "requestTypeVersion": 1,
    "title": "VPN fails with error 809",
    "description": "VPN connection fails after password entry.",
    "answers": {"device":"Windows laptop","errorCode":"809"},
    "uploadIds": []
  }'
```

The `answers` keys are **catalog-version dependent**, not a global hard-coded form. The backend must reject missing required fields, unknown fields, stale published form versions, and unauthorized request types. The request body must not accept `tenantId`, `requesterId` or role claims.

### 8.4 Approve a request (IT Manager only)

```bash
APPROVAL_ID="REPLACE_WITH_REAL_APPROVAL_UUID"
curl -X POST "$API_BASE/approvals/$APPROVAL_ID/decision" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"expectedVersion":2,"decision":"APPROVE"}'
```

For `REJECT`, the contract requires a nonempty `reason` (`if`/`then` in `ApprovalCommand`); the server must also and update the approval state atomically so that two approvers cannot make conflicting decisions. Approval eligibility is a **person-level authorization check**, not merely role membership.

### 8.5 Ask the assistant (read-only KB)

```bash
CONVERSATION_ID="REPLACE_WITH_REAL_CONVERSATION_UUID"
curl -X POST "$API_BASE/ai/conversations/$CONVERSATION_ID/messages" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"My VPN fails with error 809. What should I check?"}'
```

Responses with `kind=NO_SOURCE` must have **zero citations**, not fabricated article references. `POST .../ticket-draft` stores a draft (`id`, `status: DRAFT`), never a ticket. The employee reviews it and submits `POST /tickets` with `aiDraftId`; the draft becomes `SUBMITTED` in the same transaction. `POST .../drafts/{draftId}/discard` marks it `DISCARDED`. If the AI provider is down, both assistant calls return `503 AI_UNAVAILABLE`.

### 8.6 Upload and asset handover

```bash
curl -X POST "$API_BASE/uploads" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "file=@./evidence.pdf"
```

Asset handover: `POST /assets/{assetId}/handover` with `expectedVersion`, approved `ticketId`, `recipientMemberId`, `handedOverAt`, and `condition`. The backend must atomically enforce single active assignment, validated approval, authorized recipient and audit history.

## 9. Business sequences to enforce on the server

### Incident

1. Employee browses the published catalog and submits an incident, using the current form version and idempotency key.
2. IT performs triage, assignment, progress and resolution with `expectedVersion`.
3. The employee confirms or reopens within seven days; otherwise an idempotent server job automatically closes it.
4. Public comments are visible to requester; internal IT notes and their attachments never appear in requester views.

### Laptop Service Request

1. Employee submits catalog form → `PENDING_APPROVAL`.
2. Authorized manager decides; rejected requests never proceed to fulfillment.
3. IT picks an AVAILABLE asset and hands it over, logs the assignment and updates fulfillment/ticket state in a transaction.
4. Ensure no double handover, double resolution, or separate asset assignment bypasses approval.

### Knowledge-backed AI

1. Employee opens conversation, asks a question.
2. Retrieval filters by **tenant**, **article PUBLISHED state** and **user visibility**.
3. No trustworthy source → `NO_SOURCE` with `citations: []`.
4. AI suggests a draft; only an explicit employee action may create the ticket.

## 10. Verify the contract

Validate:

```bash
# From the repository root, if Node.js and network access are available:
npx @redocly/cli lint docs/api/openapi.yaml
npx @redocly/cli bundle docs/api/openapi.yaml
```

Use **Swagger Editor**, ReDoc or Swagger UI to visually review path grouping, schemas and examples. At the time of authoring, local checks covered YAML parsing, reference resolution, path parameters, unique `operationId`, JSON Schema syntax and representative request/response examples. **A full OpenAPI metaschema/Spectral/Redocly lint, live contract tests and penetration tests have not been run.**

## 11. Traceability and unresolved decisions

[`traceability.md`](traceability.md) maps every UC01–UC43 to API method/path, `operationId` and planned release. Mapping is necessary but not sufficient to prove individual acceptance criteria are met.

Before implementing the MVP, product and engineering owners must resolve at least: (1) suspended-tenant sign-in conflict, (2) whether Service Requests can reopen, (3) delegated approvers after Release 1 (Release 1: IT_MANAGER only), (4) SLA re-calculation after priority updates, (5) whether upload oversize returns `400` as the AC says or standards-oriented `413` as proposed, (6) access-token format and lifetimes (refresh transport is decided: HttpOnly cookie), (7) catalog schema evolution and old ticket snapshot reads.

**Most important test boundaries:** tenant A may not read tenant B; Platform Admin may not read tenant content; employee never sees internal comments; AI never writes; approval precedes handover; two concurrent handovers cannot both succeed; duplicate create request cannot create duplicate tickets.

## 12. Changes

### 0.4.1-draft — aligned with database revision 2.3

| Area | Change |
|---|---|
| Links | `LinkCommand.linkType` / `TicketLink.linkType` (RELATED, DUPLICATE_OF, CAUSED_BY), required for ticket targets and forbidden for asset targets |
| Fulfilment | `FulfilmentStep.status` and `FulfilmentStepCommand.status` (PENDING, DONE, SKIPPED) replace the `done` flag |
| Change | `ChangeAssessment.riskLevel` (LOW, MEDIUM, HIGH) is required |

Every resource with a `version` field now has a `row_version` column in the database ([audit A2](../database/README.md#audit-revision-23)).

### 0.4.0-draft — D15 decided

| Area | Change |
|---|---|
| Sessions | Refresh tokens leave the JSON bodies: `TokenPair` is renamed `AccessSession` (access token only); `RefreshInput` removed |
| Refresh | `POST /auth/refresh` and `POST /platform/auth/refresh` take no body; security schemes `RefreshCookie` (`sd_refresh`) and `PlatformRefreshCookie` (`sd_platform_refresh`); required `X-CSRF-Token` header; `403` on CSRF mismatch |
| Cookies | `Set-Cookie` documented on sign-in, tenant selection, refresh (sets) and sign-out (clears) through `components.headers` |
| AI drafts | Submitting a DISCARDED or SUBMITTED draft returns `409 INVALID_TRANSITION` (AC-UC14) |

### 0.3.0-draft

All findings of [openapi-review.md](openapi-review.md) that the contract can fix are applied; §8 of the review lists each one. This is a **breaking** revision of a design-only contract (no client or server exists yet).

| Area | Change |
|---|---|
| Enums | `AssetStatus`, `ArticleVisibility`, `RequestType.status`, `Approval.status` now match the database enums; `departmentIds` removed from articles; `RequestType.visible` added |
| Assets | `POST /assets/{assetId}/reserve` removed (UC29 needs no reservation; concurrent handover is a `409`); recover returns the asset to `AVAILABLE` |
| Identity | `role` → `roles[]` on session, member, profile, invitation; `Role` lists tenant roles only; `POST /auth/refresh`; platform sign-in, refresh, sign-out and the `PlatformSession` scheme |
| Versions, idempotency | `Version` minimum `0`; `Idempotency-Key` max 100; `Idempotent-Replayed` and `Location` headers |
| Errors | `ErrorCode` enum referenced by `ProblemDetails`; `x-error-codes` removed; `503 AI_UNAVAILABLE` on assistant calls; `429` on ticket create and comments |
| Tickets | Triage converts by `targetRequestTypeId` (+ version, answers, reason); `tenantId` removed from `Ticket` and `Asset`; per-kind status sets in `x-allowed-by-kind`; attachments expose `visibility`, `scanStatus`, `commentId` |
| Catalog | `approvalRequired`, `slaTargetMinutes` are read-only, computed from approval rules and SLA policies; removed from inputs |
| AI | `TicketDraft.id` + `status`; `CreateTicket.aiDraftId` replaces `assistantConversationId`; discard endpoint |
| KB | `GET /manager/kb/articles` and `GET /manager/kb/articles/{articleId}` for the IT Manager review queue |
| Style | `{id}` path parameters renamed (`{approvalId}`, `{conversationId}` …); `examples` instead of `example` in schemas; `contentMediaType` instead of `format: binary`; unused `TicketCommentList` removed |

Database follow-ups that the contract now assumes are listed in the review (§8).

---

*Reference approach borrowed from finance-manager: separate OpenAPI contract, API README, stable examples, documented roles/ownership and Problem Details. SmartDesk's domain model, multi-tenant rules, ITSM workflows and AI security are specified independently.*
