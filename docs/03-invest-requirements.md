# 03 — INVEST Requirements

> Design status: TARGET V1
>
> Every user story maps 1:1 to a use case (`USxx` ↔ `UCxx`) and to at least one screen in [04 — Information architecture](04-information-architecture.md).

Cross-cutting authentication, tenant isolation, authorization, validation, audit and error handling are **acceptance constraints**, not hidden features.

## INVEST checklist

| Principle | Application in this backlog |
|---|---|
| **Independent** | Each story delivers a demonstrable outcome; unavoidable business prerequisites (e.g. approval before handover) are listed in *Dependencies*. |
| **Negotiable** | Chat vs. form layout, retrieval technique and notification channel may change as long as the outcome and the permission rules stay the same. |
| **Valuable** | Every story names the benefit for Employee, IT Staff, IT Manager or Admin. |
| **Estimable** | Role, input, output, state change and failure outcome are explicit; open values have documented defaults (reopen window 7 days, SLA warning at 80%). |
| **Small** | One primary capability per story; larger ones list their task split (API, application, persistence, UI, tests). |
| **Testable** | Each story has a positive and a negative acceptance criterion that can be checked through the UI or the API. |

## Backlog overview

```text
US01–US05   Identity and tenant
US06–US11   Employee self-service
US12–US15   AI assistant
US16–US22   Ticket management
US23–US27   Catalog, approval and fulfilment
US28–US32   IT assets
US33–US35   Knowledge base
US36–US38   SLA and reporting
```

## Product backlog

| ID | User story | Value | Priority | Dependencies |
|---|---|---|---|---|
| US01 | As a **user**, I want to sign in and sign out so that only valid members reach my organization's workspace. | Protected access | P0 | Seeded tenant and account |
| US02 | As a **user**, I want to view and edit my profile so that IT can contact and route me correctly. | Accurate contact data | P1 | US01 |
| US03 | As an **Org Admin**, I want to update organization settings (name, timezone, locations, departments) so that routing and SLA use the right context. | Correct tenant setup | P1 | US01 |
| US04 | As an **Org Admin**, I want to invite, lock and assign roles to members so that access stays controlled. | Access control | P0 | US01 |
| US05 | As a **Platform Admin**, I want to activate or suspend a tenant so that I can manage the SaaS lifecycle. | Tenant lifecycle | P2 | — |
| US06 | As an **employee**, I want to browse the IT service catalog so that I can find the right request type. | Right request first time | P0 | US23 |
| US07 | As an **employee**, I want to submit a request through a form for that service so that IT gets complete data. | Complete tickets | P0 | US06 |
| US08 | As an **employee**, I want to find and track my tickets so that I know the progress and who is handling them. | Transparency | P0 | US07 |
| US09 | As an **employee**, I want to add comments and files to my ticket so that I can give evidence without email. | Fewer back-and-forth | P0 | US08 |
| US10 | As an **employee**, I want to confirm resolution or reopen within 7 days so that tickets close only when the problem is really fixed. | Real resolution | P0 | US21 |
| US11 | As an **employee**, I want to see the devices assigned to me so that I know what I am responsible for. | Accountability | P1 | US29 |
| US12 | As an **employee**, I want to ask questions answered from internal articles with sources so that I can trust and verify the answer. | Trusted self-service | P0 | US34 |
| US13 | As an **employee**, I want step-by-step troubleshooting so that I can fix common issues myself. | Fewer tickets | P1 | US12 |
| US14 | As an **employee**, I want the assistant to prepare a ticket draft from our conversation so that I do not need to know ticket categories. | Faster intake | P0 | US07, US12 |
| US15 | As an **employee**, I want to ask about my ticket status in plain language so that I get an answer without searching. | Quick status | P1 | US08 |
| US16 | As **IT Staff**, I want to view and filter the ticket queue so that I can choose what to work on next. | Prioritized work | P0 | US07 |
| US17 | As **IT Staff**, I want to set ticket type and priority so that tickets follow the right workflow and SLA. | Correct routing | P0 | US16 |
| US18 | As **IT Staff or IT Manager**, I want to assign or pick up a ticket so that each ticket has one owner. | Clear ownership | P0 | US16 |
| US19 | As **IT Staff**, I want to update status and add public replies or internal notes so that progress is transparent and technical detail stays internal. | Transparent progress | P0 | US18 |
| US20 | As **IT Staff or IT Manager**, I want to transfer or escalate a ticket with a reason so that hard or late tickets reach the right people. | Fewer stuck tickets | P1 | US18 |
| US21 | As **IT Staff**, I want to resolve a ticket with a resolution note so that the employee knows what was done and can confirm. | Closed loop | P0 | US19 |
| US22 | As **IT Staff**, I want to link a ticket to an asset or related ticket so that I have the full context. | Context | P1 | US19, US28 |
| US23 | As an **Org Admin**, I want to manage request types (fields, routing, approval flag) and publish them so that requests arrive in a standard shape. | Standard intake | P0 | US01 |
| US24 | As an **IT Manager**, I want to configure approval rules per request type so that risky requests need sign-off. | Risk control | P1 | US23, US25 |
| US25 | As an **IT Manager**, I want to approve or reject a request with a reason so that only valid requests are fulfilled. | Governance | P0 | US07, US23 |
| US26 | As **IT Staff**, I want to follow and record fulfilment steps so that service delivery is consistent. | Consistent delivery | P1 | US25 |
| US27 | As an **IT Manager**, I want to assess and manage an ISP change so that infrastructure changes are controlled. | Controlled change | P2 | US07, US25 |
| US28 | As **IT Staff**, I want to register and update IT assets so that stock and condition are known. | Asset data | P0 | US01 |
| US29 | As **IT Staff**, I want to assign and hand over a device for an approved request so that ownership is recorded. | Ownership history | P0 | US25, US28 |
| US30 | As **IT Staff**, I want to recover a device from an employee so that stock stays accurate. | Accurate stock | P1 | US29 |
| US31 | As **IT Staff**, I want to log maintenance and repairs so that asset quality is tracked. | Asset quality | P2 | US28 |
| US32 | As an **IT Manager**, I want to view inventory and asset history so that I can plan provisioning. | Planning | P1 | US28 |
| US33 | As **IT Staff**, I want to create and edit KB drafts so that support knowledge is captured. | Reusable knowledge | P0 | US01 |
| US34 | As an **IT Manager**, I want to review, publish and retire KB articles so that employees and the AI only use approved content. | Trusted content | P0 | US33 |
| US35 | As an **employee**, I want to search and read KB articles without the AI so that I have a self-service path that does not depend on AI. | Fallback path | P0 | US34 |
| US36 | As an **IT Manager**, I want to configure SLA targets by type and priority so that support commitments are explicit. | Clear commitments | P1 | US17 |
| US37 | As an **IT Manager**, I want near-breach and breach alerts so that fewer tickets are missed. | Fewer breaches | P1 | US36 |
| US38 | As an **IT Manager**, I want to view and export operations reports so that I can measure support performance. | Measurable performance | P1 | US16, US36 |

## Acceptance criteria (summary)

Every story has one positive (✓) and one negative (✗) criterion. Detailed Given/When/Then tables follow for the nine highest-risk stories.

| Story | ✓ Positive | ✗ Negative |
|---|---|---|
| US01 | Valid credentials open the role's home page in the selected tenant. | Wrong password, locked account or suspended tenant shows one generic error; signed-out session cannot call the API. |
| US02 | Name, phone, department, location and avatar can be saved. | Role and tenant fields are read-only; API ignores or rejects them. |
| US03 | Settings change only the current tenant. | Non-admin gets `403`. |
| US04 | Invited member receives the chosen role; locked member cannot sign in. | User without the role cannot reach the route or API (`403`). |
| US05 | Suspended tenant can sign in read-only but cannot create data. | Platform Admin cannot open ticket content by default. |
| US06 | Catalog lists only published types the employee may request. | Draft/hidden types never appear, even by URL. |
| US07 | Valid submit creates exactly one ticket in `Submitted` or `PendingApproval`. | Missing required field shows inline error and creates nothing. |
| US08 | Employee sees own tickets with status, assignee and next step. | Another employee's ticket returns `404`. |
| US09 | Comment and file appear on the timeline with author and time. | File over 10 MB or not on the allow-list is rejected. |
| US10 | Confirm moves `Resolved → Closed`; reopen within 7 days moves to `Reopened`. | Reopen after 7 days or on a non-resolved ticket is refused (`409`). |
| US11 | Only devices currently assigned to me are listed with handover date. | Other employees' assignments never appear. |
| US12 | Answer contains at least one citation that opens a published article. | No relevant source → "no documented answer" + ticket offer; no citation is invented. |
| US13 | Steps come from the cited article and are safe for an employee to perform. | Assistant never runs or asks for admin actions on the device. |
| US14 | Draft shows type, title, summary and required fields; confirm creates one ticket. | Without confirmation nothing is stored; repeated confirm does not duplicate. |
| US15 | Status answer matches the ticket record for the current user. | Asking about another person's ticket returns no data. |
| US16 | Queue filters by type, status, priority, assignee and SLA within the tenant. | Tickets of other tenants never appear. |
| US17 | Priority change is saved with actor and old/new value in the audit trail. | AI-suggested priority is never applied without IT action. |
| US18 | Ticket gets exactly one assignee from the tenant's IT team. | Assigning to a non-IT member or another tenant's user fails. |
| US19 | Allowed transition is saved; internal note is hidden from the employee. | Invalid transition (e.g. `Closed → InProgress`) returns `409`. |
| US20 | Transfer/escalation requires a reason and keeps timeline and SLA clock. | Empty reason is rejected. |
| US21 | `Resolved` requires a resolution note and notifies the requester. | Resolve without a note is rejected. |
| US22 | Linked asset/ticket is shown on both records. | Link to a record in another tenant fails. |
| US23 | Published type has required fields, routing team and approval flag; tickets keep the version they were created with. | Type without routing cannot be published. |
| US24 | New rule applies to new requests from its effective date. | Existing decisions are not changed by a rule update. |
| US25 | Approve stores approver, time and note; reject requires a reason. | Non-approver gets `403`; a second decision gets `409`. |
| US26 | Checklist steps are recorded with actor and time. | Fulfilment of a request needing approval is blocked until `Approved`. |
| US27 | Change cannot be approved without impact, rollback plan and window. | No automated network action is ever triggered. |
| US28 | Asset tag is unique per tenant; lifecycle status is required. | Duplicate tag is rejected. |
| US29 | Asset becomes `ASSIGNED`, handover record is linked to the ticket. | Concurrent assignment of the same asset: one succeeds, the other gets `409`. |
| US30 | Recovery closes the assignment and records a return event. | Recovering an unassigned asset is refused. |
| US31 | Log stores date, work done, technician, status before/after. | Log on a retired asset is refused. |
| US32 | Counts per status match the asset table without double counting. | IT Manager cannot edit assets from this view. |
| US33 | Draft is saved and visible only to IT. | Drafts never appear to employees or in AI retrieval. |
| US34 | Publish makes the article searchable and indexable for the AI. | Retired article is no longer cited in new answers. |
| US35 | Keyword and topic search return published, permitted articles. | Restricted article is hidden from unauthorized departments. |
| US36 | Targets use the business calendar, timezone and pause rules. | Overlapping or negative targets are rejected. |
| US37 | One alert at 80% and one at 100% of the target per ticket. | Job retries do not send duplicate alerts. |
| US38 | Export uses exactly the on-screen filters and totals. | Employee and IT Staff cannot open reports (`403`). |

## Detailed acceptance criteria (Given / When / Then)

### US07 — Submit a typed request

| Given | When | Then |
|---|---|---|
| Employee chose "Laptop Provisioning" | all required fields are filled and submitted | exactly one service request is created in `PendingApproval`, linked to requester and tenant |
| Recipient or needed-by date is missing | employee submits | error is shown next to the field; no ticket is created |
| Employee is not allowed to use this type | API is called directly | `403`, nothing stored |

### US12 — FAQ answer with sources

| Given | When | Then |
|---|---|---|
| A published VPN article exists and the employee may read it | employee asks how to connect the VPN | answer lists steps with a link to that article |
| No trustworthy article exists | employee asks | assistant says it has no documented answer and offers a ticket; nothing is invented |
| Article belongs to tenant A | employee of tenant B asks | retrieval never returns tenant A content |

### US14 — Ticket draft from conversation

| Given | When | Then |
|---|---|---|
| Employee described a VPN error without OS and error message | assistant prepares the request | it asks for the missing fields one by one and does not submit |
| All required fields are known | assistant creates the draft | employee sees type, category, summary, description and attachments with Edit and Confirm |
| Employee clicks Confirm twice or retries after a network error | backend creates the ticket | idempotency key prevents a duplicate |
| Assistant proposed a Change but data is incomplete | employee has not confirmed | no ticket is created |

### US15 — My ticket status

| Given | When | Then |
|---|---|---|
| Employee owns ticket INC-1042 | asks "where is my VPN ticket?" | assistant queries by the server-side identity and returns the real status |
| Employee asks about a colleague's ticket | tool query runs | no data is returned |

### US19 — Status and notes

| Given | When | Then |
|---|---|---|
| Ticket is `InProgress` and assigned to the technician | technician sets `Resolved` with a resolution note | timeline event is created and the requester is notified |
| Ticket is `Closed` | technician tries `InProgress` | API returns `409 invalid transition` |

### US25 — Approval decision

| Given | When | Then |
|---|---|---|
| Request is `PendingApproval` | IT Manager approves | request becomes `Approved` with approver, time and note |
| IT Staff without approval right | calls the approve endpoint | `403`, state unchanged |
| Request was already rejected | approve is called | `409`, no second decision |

### US29 — Device handover

| Given | When | Then |
|---|---|---|
| Asset A is `AVAILABLE` and the request is `Approved` | technician assigns A | asset is `ASSIGNED`, handover record is linked to the ticket |
| Asset A is being assigned by two technicians at the same time | both submit | one succeeds, the other gets `409 conflict` |

### US34 — KB publishing

| Given | When | Then |
|---|---|---|
| Article is a draft | IT Manager publishes | status is `Published` and only now is it indexed for the AI |
| Article is retired | employee asks the assistant | the article is not cited in new answers |

### US37 — SLA alerts

| Given | When | Then |
|---|---|---|
| Ticket reaches 80% of its resolve target | the SLA job runs | exactly one near-breach alert is sent |
| The job retries after a failure | it runs again | no duplicate alert for the same ticket and threshold |

## Per-story INVEST review

`PASS` means the design gives enough information to plan and accept the story; it does not mean it is implemented.

| Story | I | N | V | E | S | T | Notes |
|---|---|---|---|---|---|---|---|
| US01 | PASS | PASS | PASS | PASS | PASS | PASS | Email + password in V1; SSO is negotiable later. |
| US02 | PASS | PASS | PASS | PASS | PASS | PASS | Editable fields listed explicitly. |
| US03 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US04 | PASS | PASS | PASS | PASS | PASS | PASS | Split tasks: invite, role change, lock/unlock. |
| US05 | PASS | PASS | PASS | PASS | PASS | PASS | Suspended = read-only. |
| US06 | PASS | PASS | PASS | PASS | PASS | PASS | Needs at least one published type (seed data). |
| US07 | PASS | PASS | PASS | PASS | PASS | PASS | Field schema comes from US23. |
| US08 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US09 | PASS | PASS | PASS | PASS | PASS | PASS | File limit 10 MB, allow-list defined. |
| US10 | PASS | PASS | PASS | PASS | PASS | PASS | Reopen window 7 days, auto-close after the window. |
| US11 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US12 | PASS | PASS | PASS | PASS | PASS | PASS | Abstention when no source is part of the story. |
| US13 | PASS | PASS | PASS | PASS | PASS | PASS | Uses only steps from cited articles. |
| US14 | PASS | PASS | PASS | PASS | PASS | PASS | Submission reuses US07 validation. |
| US15 | PASS | PASS | PASS | PASS | PASS | PASS | Read-only tool scoped to the current user. |
| US16 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US17 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US18 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US19 | PASS | PASS | PASS | PASS | PASS | PASS | Transition table in [02](02-use-cases.md#ticket-lifecycles). |
| US20 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US21 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US22 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US23 | PASS | PASS | PASS | PASS | SPLIT | PASS | Largest story — split into: type CRUD, field schema, routing + approval flag, preview/publish with versioning. |
| US24 | PASS | PASS | PASS | PASS | PASS | PASS | MVP uses the approval flag from US23; rules add conditions. |
| US25 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US26 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US27 | PASS | PASS | PASS | PASS | PASS | PASS | Phase 2; manual implementation only. |
| US28 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US29 | PASS | PASS | PASS | PASS | PASS | PASS | Depends on US25 by business rule. |
| US30 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US31 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US32 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US33 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US34 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US35 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US36 | PASS | PASS | PASS | PASS | PASS | PASS | Default thresholds 80% / 100%. |
| US37 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US38 | PASS | PASS | PASS | PASS | PASS | PASS | CSV and PDF only. |

## Release plan

Releases follow priority, and every dependency points to the same or an earlier release.

| Release | Stories | Demo journey |
|---|---|---|
| **Release 1 — MVP** (21 × P0) | US01, 04, 06, 07, 08, 09, 10, 12, 14, 16, 17, 18, 19, 21, 23, 25, 28, 29, 33, 34, 35 | S1 VPN incident through AI; S2 laptop request with approval and handover |
| **Release 2 — V1 complete** (14 × P1) | US02, 03, 11, 13, 15, 20, 22, 24, 26, 30, 32, 36, 37, 38 | SLA alerts and reports; troubleshooting guidance; device recovery |
| **Phase 2** (3 × P2) | US05, 27, 31 | S3 ISP change; maintenance log; tenant lifecycle |

## Cross-cutting acceptance constraints

- Only the five roles above exist; the API, not the client, enforces role, tenant and ownership.
- Every list, detail, search, file and AI retrieval is filtered by tenant on the server.
- Records of another tenant return `404`; missing permission in the same tenant returns `403`.
- Ticket and asset updates use optimistic concurrency; conflicting writes return `409`.
- Ticket creation is idempotent; the AI has no write tools.
- Uploaded files are type- and size-checked before storage.
- Every state change writes an audit event with actor, time, old and new value.

**Related:** [Use cases](02-use-cases.md) · [Information architecture](04-information-architecture.md)
