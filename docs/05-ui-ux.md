# 05 — UI/UX: Principles, Flows and Prototype

> Design status: LOW/MID-FIDELITY V1
>
> Prototype: [`prototype/index.html`](../prototype/index.html) — single HTML file, mock data, no API and no real LLM. Open it in a browser and switch role in the top bar.

## 5.1 UX principles

1. **Self-service first, never self-service only.** The assistant and the KB are on the home page, but "Browse catalog" and a plain form are always one click away.
2. **The AI is bounded.** It answers only from published internal articles and shows the source; with no source it says so. It prepares drafts but never submits, approves, assigns or changes a device.
3. **Enter once.** Information given in the chat is carried into the draft and the form; the employee does not retype it.
4. **Plain language for employees, ITSM language for IT.** Employees pick "Report a problem / Request something / Propose a change"; IT sees Incident / Service Request / Change.
5. **Always show what happens next.** Status, owner, next step and SLA are visible on the first screen of every ticket; internal notes are clearly marked and never shown to the employee.
6. **Guard irreversible actions.** Resolve needs a resolution note, reject needs a reason, handover is locked until approval.
7. **Accessible by default.** Visible labels, keyboard focus ring, errors next to the field, status never shown by colour alone.

## 5.2 Layout and design system (draft)

| Item | Decision |
|---|---|
| Canvas | Desktop 1440 × 900; sidebar 236 px; content max 1320 px; 8 px spacing scale |
| Responsive | Employee pages stack to one column below 640 px; IT and manager pages are desktop-first, tables scroll horizontally |
| Colour | Navy shell, blue primary action, green success, amber warning/waiting, red danger/high priority |
| Status chips | Text label + colour (`In Progress`, `Pending Approval`, `Resolved`…) |
| Key components | `CitedAnswer`, `TicketDraftCard`, `DynamicForm`, `ProgressTracker`, `TicketTimeline` (public vs internal), `SLAIndicator`, `AssetPicker`, `DecisionPanel` |

### Screen states

| State | Required behaviour |
|---|---|
| Loading | Keep the shell; skeleton only in the panel being loaded. |
| Empty | Explain why it is empty and show the next permitted action (e.g. "No tickets yet — New request"). |
| Validation error | Keep entered values, show the message under the field, summary banner at the top of the form. |
| API error | Short message with a retry; no technical details. |
| Forbidden / not found | `SCR-04` with a link back to the role's home; other-tenant records look like "not found". |
| Saving | Disable the submit button to prevent duplicates. |
| Success | Toast with the ticket ID and navigate to the detail page. |
| AI states | Retrieving → grounded answer with source / no-source fallback / guided questions / draft awaiting confirmation. |

## 5.3 User flows

### Flow A — VPN not working (AI → Incident)

```mermaid
flowchart TB
    A["SCR-10 Home: ask 'VPN not working'"] --> B["SCR-11 Assistant retrieves published KB"]
    B -->|source found| C["Answer with steps + KB-024 citation"]
    B -->|no source| X["Say so; offer catalog or draft"]
    C --> D{"Fixed?"}
    D -->|yes| E["End: no ticket"]
    D -->|no| F["Ask missing fields: OS, error"]
    F --> G["Draft panel: review / edit"]
    G -->|discard| E
    G -->|confirm| H["Backend validates + idempotent create"]
    H --> I["SCR-17 Request Detail: INC-xxxx Submitted"]
    I --> J["IT: SCR-21 queue → SCR-22 triage, assign, work"]
    J --> K["Resolved with note → notification"]
    K --> L{"Employee"}
    L -->|confirm| M["Closed"]
    L -->|reopen with reason ≤ 7 days| J
```

### Flow B — New laptop (Catalog → Service Request → Asset)

```mermaid
flowchart TB
    A["SCR-14 Catalog: Laptop provisioning"] --> B["SCR-15 form: recipient, needed by, configuration, reason"]
    B -->|missing field| B
    B -->|submit| C["SR-xxxx Pending Approval"]
    C --> D["Manager notified → SCR-30 Approval Inbox"]
    D -->|reject + reason| E["Employee sees reason in SCR-17 → End"]
    D -->|approve| F["IT notified → SCR-23 Fulfilment unlocked"]
    F --> G["Asset picker: AVAILABLE laptops only"]
    G --> H["Hand over: asset ASSIGNED, record linked"]
    H --> I["Resolved → employee confirms → Closed"]
```

### Flow C — Switch office ISP (Change, Phase 2)

```text
Catalog "Propose a change" → site, current ISP, reason, proposed window
 → Assessing: IT records impact, affected users, downtime, rollback plan
 → SCR-31 Change Review: manager approves / rejects / asks for more info
 → Scheduled maintenance window → IT implements manually → result recorded → Closed
```

SmartDesk never runs network changes itself.

### Screen transitions

| # | Actor | From | Trigger | To | Feedback |
|---|---|---|---|---|---|
| 1 | Employee | `SCR-10` Home | Ask a question | `SCR-11` Assistant | Answer with source or no-source message |
| 2 | Employee | `SCR-11` | Issue not fixed | same page | Guided questions, then draft panel |
| 3 | Employee | Draft panel | Confirm | `SCR-17` Request Detail | Toast with ticket ID |
| 4 | Employee | `SCR-14` Catalog | Choose service | `SCR-15` New Request | Approval need and SLA shown before typing |
| 5 | Employee | `SCR-15` | Submit | `SCR-17` | "Waiting for approval" step highlighted |
| 6 | IT Manager | Notification | Open | `SCR-30` Approval Inbox | Request summary with stock |
| 7 | IT Manager → IT Staff | `SCR-30` | Approve | **notification to IT** → `SCR-23` Fulfilment | Lock removed, asset picker enabled |
| 8 | IT Staff | `SCR-23` | Hand over | `SCR-25` Asset Detail / ticket resolved | Asset `ASSIGNED`, requester notified |
| 9 | IT Staff → Employee | `SCR-22` | Resolve with note | **notification** → `SCR-17` | Confirm / reopen banner |

## 5.4 Prototype screens by role

All screenshots come from the prototype and are grouped by role, like the reference project. Regenerate them with [`tools/capture_ui.py`](../tools/capture_ui.py).

```text
docs/images/ui/
├── common/       Sign in, company picker, not found          (4)
├── employee/     Home, assistant, guides, requests, devices  (17)
├── it-staff/     Dashboard, queue, ticket, delivery, devices  (10)
└── it-manager/   Approvals, reports, read-only devices        (9)
```

### Common

#### Sign In (`SCR-01`, UC01)

![Sign in](images/ui/common/01-sign-in.png)

#### Sign In — one message for every failed attempt

![Sign in error](images/ui/common/02-sign-in-error.png)

#### Sign In — email belongs to more than one company

![Choose company](images/ui/common/03-sign-in-choose-company.png)

#### Not found — another employee's ticket (`SCR-04`)

![Not found](images/ui/common/04-not-found.png)

### Employee

#### Home (`SCR-10`)

![Employee home](images/ui/employee/01-home.png)

#### AI Assistant — answer with a source (`SCR-11`, UC12–UC13)

![AI answer with source](images/ui/employee/02-ai-answer-with-source.png)

#### AI Assistant — follow-up questions and ticket draft (UC14)

![AI ticket draft](images/ui/employee/03-ai-ticket-draft.png)

#### AI Assistant — when it doesn't know (UC12)

![AI no source](images/ui/employee/04-ai-no-source.png)

#### AI Assistant — "where's my ticket?" (UC15)

![AI ticket status](images/ui/employee/05-ai-ticket-status.png)

#### Knowledge Base and guide (`SCR-12`, `SCR-13`, UC35)

![Knowledge base](images/ui/employee/06-knowledge-base.png)

![KB article](images/ui/employee/07-kb-article.png)

#### Service Catalog (`SCR-14`, UC06)

![Service catalog](images/ui/employee/08-service-catalog.png)

#### New Request — form and errors (`SCR-15`, UC07)

![New request](images/ui/employee/09-new-request.png)

![New request errors](images/ui/employee/10-new-request-errors.png)

#### My Requests (`SCR-16`, UC08)

![My requests](images/ui/employee/11-my-requests.png)

#### Request Detail — in progress, waiting for approval, resolved (`SCR-17`, UC08–UC10)

![Request in progress](images/ui/employee/12-request-in-progress.png)

![Request waiting for approval](images/ui/employee/13-request-waiting-approval.png)

![Request resolved](images/ui/employee/14-request-resolved.png)

#### My Assets (`SCR-18`, UC11)

![My assets](images/ui/employee/15-my-assets.png)

#### My Profile — details and validation (`SCR-02`, UC02)

![Profile](images/ui/employee/16-profile.png)

![Profile error](images/ui/employee/17-profile-error.png)

### IT Staff

#### Dashboard (`SCR-20`, UC16)

![IT dashboard](images/ui/it-staff/01-dashboard.png)

#### Ticket Queue (`SCR-21`, UC16–UC18)

![Ticket queue](images/ui/it-staff/02-ticket-queue.png)

#### Ticket Detail — reply, IT-only note, resolve (`SCR-22`, UC17–UC21)

![Ticket detail](images/ui/it-staff/03-ticket-detail.png)

![Internal note](images/ui/it-staff/04-internal-note.png)

![Resolve needs a note](images/ui/it-staff/05-resolve-needs-note.png)

#### Fulfilment — locked, then ready after approval (`SCR-23`, UC26, UC29)

![Fulfilment locked](images/ui/it-staff/06-fulfilment-locked.png)

![Fulfilment ready](images/ui/it-staff/07-fulfilment-ready.png)

#### Asset Inventory (`SCR-24`, UC28)

![Asset inventory](images/ui/it-staff/08-asset-inventory.png)

#### KB Editor — specified only (`SCR-26`, UC33)

![KB editor](images/ui/it-staff/09-kb-editor-spec.png)

#### My Profile (`SCR-02`)

![IT staff profile](images/ui/it-staff/10-profile.png)

### IT Manager

#### Approval Inbox — review, reject needs a reason, approve (`SCR-30`, UC25)

![Approval inbox](images/ui/it-manager/01-approval-inbox.png)

![Reject needs a reason](images/ui/it-manager/02-reject-needs-reason.png)

![Approved](images/ui/it-manager/03-approved.png)

#### SLA & Reports (`SCR-33`, UC37–UC38)

![SLA and reports](images/ui/it-manager/04-sla-reports.png)

#### Ticket Queue (`SCR-21`, UC18, UC20)

![Manager ticket queue](images/ui/it-manager/05-ticket-queue.png)

#### Asset Inventory — read only (`SCR-24`, UC32)

![Read-only inventory](images/ui/it-manager/06-asset-inventory-read-only.png)

#### SLA Policies and KB Review — specified only (`SCR-34`, `SCR-32`)

![SLA policies](images/ui/it-manager/07-sla-policies-spec.png)

![KB review](images/ui/it-manager/08-kb-review-spec.png)

#### My Profile (`SCR-02`)

![Manager profile](images/ui/it-manager/09-profile.png)

### Prototype coverage

| Built and interactive | Specified only (section placeholders) | Not in the prototype |
|---|---|---|
| `SCR-01`, `SCR-02`, `SCR-04`, `SCR-10`–`SCR-18`, `SCR-20`–`SCR-24`, `SCR-30`, `SCR-33` | `SCR-26`, `SCR-32`, `SCR-34`; the Password section of `SCR-02` (UC39) | `SCR-03`, `SCR-25`, `SCR-31`, `SCR-35`, `SCR-40`–`SCR-42`, `SCR-50` (see the [IA](04-information-architecture.md)) |

Demo accounts on the Sign In page: `an@`, `minh@`, `quang@acme.example`, password `demo1234` (mock data only). The `?demo=` shortcuts used for the screenshots are listed in [`tools/capture_ui.py`](../tools/capture_ui.py).

## 5.5 Usability acceptance criteria

- An employee starts a VPN incident from Home in **≤ 2 interactions**.
- An employee can start without knowing the words Incident / Service Request.
- Flows A and B can be completed with the keyboard only (except the OS file picker).
- The user is warned before irreversible actions (approve, reject, resolve, hand over).
- Every AI how-to answer shows a source; with no source, the fallback is shown instead.
- Ticket detail shows status, owner and next step in the first desktop viewport.

## 5.6 Validation plan

Quick test with 5–8 participants across four tasks: (a) employee unfamiliar with ITSM reports a VPN issue, (b) employee requests a laptop, (c) technician resolves a ticket, (d) manager approves a request. Measure completion rate, time on task, hesitations, wrong request type and trust in the AI answer. **No test has been run yet.**

**Related:** [Information architecture](04-information-architecture.md) · [Use cases](02-use-cases.md)
