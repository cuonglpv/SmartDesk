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
| **Testable** | Each story links to an `AC-UCxx` block with positive and negative criteria checkable through the UI or the API. |

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
US39–US43   Identity and platform administration (added after the feature map review)
```

## Product backlog

| ID | User story | Value | Priority | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|
| US01 | As a **user**, I want to sign in and sign out so that only valid members reach my organization's workspace. | Protected access | P0 | Seeded tenant and account | [AC-UC01](06-acceptance-criteria.md#ac-uc01--sign-in-and-sign-out) |
| US02 | As a **user**, I want to view and edit my profile so that IT can contact and route me correctly. | Accurate contact data | P1 | US01 | [AC-UC02](06-acceptance-criteria.md#ac-uc02--view-and-edit-my-profile) |
| US03 | As an **Org Admin**, I want to update organization settings (name, timezone, locations) and add or edit departments so that routing and SLA use the right context. | Correct tenant setup | P1 | US01 | [AC-UC03](06-acceptance-criteria.md#ac-uc03--update-organization-settings-and-departments) |
| US04 | As an **Org Admin**, I want to invite, lock and assign roles to members so that access stays controlled. | Access control | P0 | US01 | [AC-UC04](06-acceptance-criteria.md#ac-uc04--invite-lock-and-assign-member-roles) |
| US05 | As a **Platform Admin**, I want to create and activate a tenant workspace so that a new customer can start setting it up. | Customer onboarding | P1 | US01 | [AC-UC05](06-acceptance-criteria.md#ac-uc05--create-and-activate-a-tenant-workspace) |
| US06 | As an **employee**, I want to browse the IT service catalog so that I can find the right request type. | Right request first time | P0 | US23 | [AC-UC06](06-acceptance-criteria.md#ac-uc06--browse-the-it-service-catalog) |
| US07 | As an **employee**, I want to submit a request through a form for that service so that IT gets complete data. | Complete tickets | P0 | US06 | [AC-UC07](06-acceptance-criteria.md#ac-uc07--submit-a-request-with-the-right-form) |
| US08 | As an **employee**, I want to find and track my tickets so that I know the progress and who is handling them. | Transparency | P0 | US07 | [AC-UC08](06-acceptance-criteria.md#ac-uc08--find-and-track-my-tickets) |
| US09 | As an **employee**, I want to add comments and files to my ticket so that I can give evidence without email. | Fewer back-and-forth | P0 | US08 | [AC-UC09](06-acceptance-criteria.md#ac-uc09--add-comments-and-files-to-my-ticket) |
| US10 | As an **employee**, I want to confirm resolution or reopen within 7 days so that tickets close only when the problem is really fixed. | Real resolution | P0 | US21 | [AC-UC10](06-acceptance-criteria.md#ac-uc10--confirm-resolution-or-reopen-a-ticket) |
| US11 | As an **employee**, I want to see the devices assigned to me so that I know what I am responsible for. | Accountability | P1 | US29 | [AC-UC11](06-acceptance-criteria.md#ac-uc11--view-assets-assigned-to-me) |
| US12 | As an **employee**, I want to ask questions answered from internal articles with sources so that I can trust and verify the answer. | Trusted self-service | P0 | US34 | [AC-UC12](06-acceptance-criteria.md#ac-uc12--ask-a-question-and-get-an-answer-from-company-guides) |
| US13 | As an **employee**, I want step-by-step troubleshooting so that I can fix common issues myself. | Fewer tickets | P1 | US12 | [AC-UC13](06-acceptance-criteria.md#ac-uc13--get-step-by-step-troubleshooting) |
| US14 | As an **employee**, I want the assistant to prepare a ticket draft from our conversation so that I do not need to know ticket categories. | Faster intake | P0 | US07, US12 | [AC-UC14](06-acceptance-criteria.md#ac-uc14--turn-a-chat-into-a-ticket-draft) |
| US15 | As an **employee**, I want to ask about my ticket status in plain language so that I get an answer without searching. | Quick status | P1 | US08 | [AC-UC15](06-acceptance-criteria.md#ac-uc15--ask-in-chat-where-my-ticket-stands) |
| US16 | As **IT Staff**, I want to view and filter the ticket queue so that I can choose what to work on next. | Prioritized work | P0 | US07 | [AC-UC16](06-acceptance-criteria.md#ac-uc16--view-and-filter-the-ticket-queue) |
| US17 | As **IT Staff**, I want to set ticket type and priority so that tickets follow the right workflow and SLA. | Correct routing | P0 | US16 | [AC-UC17](06-acceptance-criteria.md#ac-uc17--triage-and-set-ticket-priority) |
| US18 | As **IT Staff or IT Manager**, I want to assign or pick up a ticket so that each ticket has one owner. | Clear ownership | P0 | US16 | [AC-UC18](06-acceptance-criteria.md#ac-uc18--assign-or-pick-up-a-ticket) |
| US19 | As **IT Staff**, I want to update status and add public replies or internal notes so that progress is transparent and technical detail stays internal. | Transparent progress | P0 | US18 | [AC-UC19](06-acceptance-criteria.md#ac-uc19--update-status-and-technical-notes) |
| US20 | As **IT Staff or IT Manager**, I want to transfer or escalate a ticket with a reason so that hard or late tickets reach the right people. | Fewer stuck tickets | P1 | US18 | [AC-UC20](06-acceptance-criteria.md#ac-uc20--transfer-or-escalate-a-ticket) |
| US21 | As **IT Staff**, I want to resolve a ticket with a resolution note so that the employee knows what was done and can confirm. | Closed loop | P0 | US19 | [AC-UC21](06-acceptance-criteria.md#ac-uc21--resolve-and-close-a-ticket) |
| US22 | As **IT Staff**, I want to link a ticket to an asset or related ticket so that I have the full context. | Context | P1 | US19, US28 | [AC-UC22](06-acceptance-criteria.md#ac-uc22--link-a-ticket-to-a-device-or-another-ticket) |
| US23 | As an **Org Admin**, I want to manage request types (fields, routing, approval flag) and publish them so that requests arrive in a standard shape. | Standard intake | P0 | US01 | [AC-UC23](06-acceptance-criteria.md#ac-uc23--manage-request-types-and-forms) |
| US24 | As an **IT Manager**, I want to configure approval rules per request type so that risky requests need sign-off. | Risk control | P1 | US23, US25 | [AC-UC24](06-acceptance-criteria.md#ac-uc24--configure-approval-rules) |
| US25 | As an **IT Manager**, I want to approve or reject a request with a reason so that only valid requests are fulfilled. | Governance | P0 | US07, US23 | [AC-UC25](06-acceptance-criteria.md#ac-uc25--approve-or-reject-a-request-with-reason) |
| US26 | As **IT Staff**, I want to follow and record fulfilment steps so that service delivery is consistent. | Consistent delivery | P1 | US25 | [AC-UC26](06-acceptance-criteria.md#ac-uc26--carry-out-and-record-the-delivery-work) |
| US27 | As an **IT Manager**, I want to assess and manage an ISP change so that infrastructure changes are controlled. | Controlled change | P2 | US07, US25 | [AC-UC27](06-acceptance-criteria.md#ac-uc27--review-and-plan-an-internet-provider-change-phase-2) |
| US28 | As **IT Staff**, I want to register and update IT assets so that stock and condition are known. | Asset data | P0 | US01 | [AC-UC28](06-acceptance-criteria.md#ac-uc28--add-and-update-it-devices) |
| US29 | As **IT Staff**, I want to assign and hand over a device for an approved request so that ownership is recorded. | Ownership history | P0 | US25, US28 | [AC-UC29](06-acceptance-criteria.md#ac-uc29--assign-and-hand-over-a-device) |
| US30 | As **IT Staff**, I want to recover a device from an employee so that stock stays accurate. | Accurate stock | P1 | US29 | [AC-UC30](06-acceptance-criteria.md#ac-uc30--take-a-device-back-from-an-employee) |
| US31 | As **IT Staff**, I want to log maintenance and repairs so that asset quality is tracked. | Asset quality | P2 | US28 | [AC-UC31](06-acceptance-criteria.md#ac-uc31--log-repairs-and-maintenance-phase-2) |
| US32 | As an **IT Manager**, I want to view inventory and asset history so that I can plan provisioning. | Planning | P1 | US28 | [AC-UC32](06-acceptance-criteria.md#ac-uc32--view-device-stock-and-history) |
| US33 | As **IT Staff**, I want to create and edit KB drafts so that support knowledge is captured. | Reusable knowledge | P0 | US01 | [AC-UC33](06-acceptance-criteria.md#ac-uc33--write-and-edit-guide-drafts) |
| US34 | As an **IT Manager**, I want to review, publish and retire KB articles so that employees and the AI only use approved content. | Trusted content | P0 | US33 | [AC-UC34](06-acceptance-criteria.md#ac-uc34--review-publish-and-retire-guides) |
| US35 | As an **employee**, I want to search and read KB articles without the AI so that I have a self-service path that does not depend on AI. | Fallback path | P0 | US34 | [AC-UC35](06-acceptance-criteria.md#ac-uc35--search-and-read-guides-without-the-ai) |
| US36 | As an **IT Manager**, I want to configure SLA targets by type and priority so that support commitments are explicit. | Clear commitments | P1 | US17 | [AC-UC36](06-acceptance-criteria.md#ac-uc36--set-sla-targets-by-type-and-priority) |
| US37 | As an **IT Manager**, I want near-breach and breach alerts so that fewer tickets are missed. | Fewer breaches | P1 | US36 | [AC-UC37](06-acceptance-criteria.md#ac-uc37--get-alerts-when-a-deadline-is-at-risk) |
| US38 | As an **IT Manager**, I want to view and export operations reports so that I can measure support performance. | Measurable performance | P1 | US16, US36 | [AC-UC38](06-acceptance-criteria.md#ac-uc38--view-and-export-operations-reports) |
| US39 | As a **user**, I want to change my password so that I can keep my account safe without asking IT. | Account security | P0 | US01 | [AC-UC39](06-acceptance-criteria.md#ac-uc39--change-my-password) |
| US40 | As a **user**, I want to see my notifications in one place so that I never miss an update, approval or deadline. | Nothing missed | P1 | US01 | [AC-UC40](06-acceptance-criteria.md#ac-uc40--view-my-notifications) |
| US41 | As a **Platform Admin**, I want to suspend or reopen a tenant workspace so that I can manage the SaaS lifecycle. | Tenant lifecycle | P2 | US05 | [AC-UC41](06-acceptance-criteria.md#ac-uc41--suspend-or-reopen-a-tenant-workspace-phase-2) |
| US42 | As a **Platform Admin**, I want to see the list of organizations so that I know which workspaces exist and their status. | Platform overview | P1 | US05 | [AC-UC42](06-acceptance-criteria.md#ac-uc42--view-the-organization-list) |
| US43 | As a **Platform Admin**, I want to read the platform admin log so that every admin action is traceable. | Accountability | P1 | US05 | [AC-UC43](06-acceptance-criteria.md#ac-uc43--view-the-platform-admin-log) |

## Acceptance criteria

Every story links to its `AC-UCxx` block in [06 — Acceptance criteria](06-acceptance-criteria.md). Each block contains positive and negative criteria with expected HTTP outcomes, and Given/When/Then tables for the highest-risk stories (US07, US12, US14, US15, US19, US25, US29, US34, US37).

## Per-story INVEST review

`PASS` means the design gives enough information to plan and accept the story; it does not mean it is implemented.

| Story | I | N | V | E | S | T | Notes |
|---|---|---|---|---|---|---|---|
| US01 | PASS | PASS | PASS | PASS | PASS | PASS | Email + password in V1; SSO is negotiable later. |
| US02 | PASS | PASS | PASS | PASS | PASS | PASS | Editable fields listed explicitly. |
| US03 | PASS | PASS | PASS | PASS | PASS | PASS | |
| US04 | PASS | PASS | PASS | PASS | PASS | PASS | Split tasks: invite, role change, lock/unlock. |
| US05 | PASS | PASS | PASS | PASS | PASS | PASS | Creates an empty workspace and invites the first Org Admin. |
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
| US39 | PASS | PASS | PASS | PASS | PASS | PASS | Requires the current password; other sessions are signed out. |
| US40 | PASS | PASS | PASS | PASS | PASS | PASS | Notifications are produced by other stories; this story only lists and opens them. |
| US41 | PASS | PASS | PASS | PASS | PASS | PASS | Suspended = read-only. |
| US42 | PASS | PASS | PASS | PASS | PASS | PASS | Metadata only, never ticket content. |
| US43 | PASS | PASS | PASS | PASS | PASS | PASS | Read-only log. |

## Release plan

Releases follow priority, and every dependency points to the same or an earlier release.

| Release | Stories | Demo journey |
|---|---|---|
| **Release 1 — MVP** (22 × P0) | US01, 04, 06, 07, 08, 09, 10, 12, 14, 16, 17, 18, 19, 21, 23, 25, 28, 29, 33, 34, 35, 39 | S1 VPN incident through AI; S2 laptop request with approval and handover |
| **Release 2 — V1 complete** (18 × P1) | US02, 03, 05, 11, 13, 15, 20, 22, 24, 26, 30, 32, 36, 37, 38, 40, 42, 43 | SLA alerts and reports; troubleshooting guidance; device recovery; workspace onboarding |
| **Phase 2** (3 × P2) | US27, 31, 41 | S3 ISP change; maintenance log; tenant lifecycle |

## Cross-cutting acceptance constraints

- Only the five roles above exist; the API, not the client, enforces role, tenant and ownership.
- Every list, detail, search, file and AI retrieval is filtered by tenant on the server.
- Records of another tenant return `404`; missing permission in the same tenant returns `403`.
- Ticket and asset updates use optimistic concurrency; conflicting writes return `409`.
- Ticket creation is idempotent; the AI has no write tools.
- Uploaded files are type- and size-checked before storage.
- Every state change writes an audit event with actor, time, old and new value.

**Related:** [Use cases](02-use-cases.md) · [Acceptance criteria](06-acceptance-criteria.md) · [Information architecture](04-information-architecture.md)
