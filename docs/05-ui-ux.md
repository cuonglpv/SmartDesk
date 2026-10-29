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

## 5.4 Prototype screens

All screens below are captured from the prototype with [`tools/capture_ui.py`](../tools/capture_ui.py).

### Employee Home (`SCR-10`)

Ask bar, quick actions, a "pending your action" banner, open tickets and popular guides.

![Employee Home](images/ui/01-employee-home.png)

### AI Assistant — cited answer, guided questions and draft (`SCR-11`, UC12–UC14)

The draft panel stays "not submitted" until the employee confirms.

![AI Assistant with ticket draft](images/ui/02-ai-assistant-draft.png)

### AI Assistant — no source found (`SCR-11`, UC12 negative path)

The assistant refuses to guess and offers the catalog or a draft instead of inventing a citation.

![AI Assistant no-source fallback](images/ui/03-ai-assistant-no-source.png)

### Service Catalog (`SCR-14`)

![Service Catalog](images/ui/04-service-catalog.png)

### New Request — validation (`SCR-15`, UC07)

![New request validation errors](images/ui/05-new-request-validation.png)

### Request Detail — confirm or reopen (`SCR-17`, UC10)

![Request detail resolved](images/ui/06-request-detail-resolved.png)

### Ticket Queue (`SCR-21`, UC16–UC18)

![Ticket queue](images/ui/07-agent-queue.png)

### Ticket Detail — public reply vs internal note (`SCR-22`, UC19)

![Agent ticket detail](images/ui/08-agent-ticket-detail.png)

### Ticket Detail — resolution note required (`SCR-22`, UC21)

![Resolve requires a resolution note](images/ui/09-agent-resolve-validation.png)

### Fulfilment — locked until approval (`SCR-23`, UC26/UC29)

![Fulfilment locked](images/ui/10-fulfilment-locked.png)

### Approval Inbox — reject needs a reason (`SCR-30`, UC25)

![Approval inbox](images/ui/11-manager-approval-reject-reason.png)

### SLA & Reports (`SCR-33`, UC37/UC38)

![SLA and reports](images/ui/12-manager-reports.png)

### Asset Inventory (`SCR-24`, UC28/UC32)

![Asset inventory](images/ui/13-asset-inventory.png)

### Prototype coverage

| Built and interactive | Specified only (wireframe placeholder) |
|---|---|
| `SCR-10`–`SCR-18`, `SCR-20`–`SCR-24`, `SCR-30`, `SCR-33` | `SCR-02`, `SCR-26`, `SCR-32`, `SCR-34`; other pages exist only in the [IA](04-information-architecture.md) |

Demo shortcuts: `#/app/assistant?demo=vpn`, `?demo=nosource`, `#/it/tickets/INC-1042?demo=resolve`, `#/manage/approvals?demo=reject`, `#/app/requests/new/laptop?demo=invalid`.

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
