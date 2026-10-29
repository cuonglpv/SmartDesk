# 06 — Acceptance Criteria

> Design status: TARGET V1
>
> Implementation status: UX prototype only — criteria marked *(prototype)* can already be seen in [`prototype/index.html`](../prototype/index.html); all others need the backend.

Each `AC-UCxx` block belongs to use case `UCxx` and user story `USxx`. The criteria describe target behavior; the API, not the UI, must enforce authorization, tenant isolation and business rules.

**HTTP conventions used below:** `400` invalid input · `401` not authenticated · `403` authenticated but not permitted in this tenant · `404` missing record **or** record of another tenant · `409` invalid state transition or concurrent update.

## Identity & Tenant

### AC-UC01 — Sign in and sign out

*Story US01 · Screens SCR-01, SCR-02*

- Valid credentials for an active member of an active tenant start a session and open the role's home page *(prototype)*.
- Wrong password, unknown email, locked member and suspended tenant all return the same `401` message; no account state is disclosed *(prototype)*.
- If the email belongs to several tenants, the user must pick one before the session starts; the session is scoped to that tenant only.
- After sign-out, protected routes redirect to Sign In and API calls with the old session return `401`.

### AC-UC02 — View and edit my profile

*Story US02 · Screen SCR-02*

- Name, phone, department, location, avatar and notification preferences can be saved; success returns the updated profile *(prototype)*.
- Role, email and tenant are read-only; a request that tries to change them returns `400` and changes nothing.

### AC-UC03 — Update organization settings

*Story US03 · Screen SCR-40*

- Org Admin can update company name, timezone, locations and departments; changes apply only to the current tenant.
- Non-admins receive `403`; invalid timezone or duplicate location name returns `400`.

### AC-UC04 — Invite, lock and assign member roles

*Story US04 · Screen SCR-41*

- An invitation creates a pending member with the chosen role; accepting it activates the account.
- A locked member cannot sign in (`401`) but keeps all history; unlocking restores access.
- Org Admin cannot remove the last Org Admin of the tenant (`409`); non-admins receive `403`.

### AC-UC05 — Activate or suspend a tenant

*Story US05 · Screen SCR-50*

- A suspended tenant can sign in read-only; every create or update returns `403` with a "tenant suspended" reason.
- Platform Admin sees tenant metadata only; ticket, comment and attachment endpoints return `403` for this role by default.

## Employee Self-service

### AC-UC06 — Browse the IT service catalog

*Story US06 · Screens SCR-10, SCR-14*

- Only published request types the employee may use are listed, grouped as *Report a problem / Request something / Propose a change* *(prototype)*.
- Each card shows whether approval is needed and the SLA target *(prototype)*.
- Draft or hidden types never appear and return `404` when opened by URL.

### AC-UC07 — Submit a request with the right form

*Story US07 · Screen SCR-15*

| Given | When | Then |
|---|---|---|
| Employee chose "Laptop provisioning" | all required fields are filled and submitted | exactly one service request is created in `PendingApproval`, linked to requester, tenant and request-type version *(prototype)* |
| Recipient or needed-by date is missing | employee submits | an error is shown next to each missing field, entered values are kept and no ticket is created *(prototype)* |
| Employee is not allowed to use this type | the API is called directly | `403`, nothing is stored |
| The same submit is sent twice (double click or retry) | backend receives both | the idempotency key returns the first ticket; no duplicate |

- Attachments larger than 10 MB or outside the allow-list (images, PDF, TXT, LOG) return `400`.

### AC-UC08 — Find and track my tickets

*Story US08 · Screens SCR-10, SCR-16, SCR-17*

- My Requests lists only tickets where I am the requester, with status, assignee and last update *(prototype)*.
- Search by ID or title and filters by status, type and date combine consistently.
- Opening another employee's ticket by URL returns `404` *(prototype)*.
- Request Detail shows the progress tracker for the ticket's own state machine *(prototype)*.

### AC-UC09 — Add comments and files to my ticket

*Story US09 · Screen SCR-17*

- A comment or file is added to the timeline with author and time and notifies the assignee *(prototype for comments)*.
- Internal IT notes are never returned to the requester.
- Comments on `Closed` or `Rejected` tickets return `409`.

### AC-UC10 — Confirm resolution or reopen a ticket

*Story US10 · Screens SCR-17, SCR-03*

- On a `Resolved` ticket the requester can Confirm (→ `Closed`) *(prototype)*.
- Reopen requires a reason and is allowed for 7 days after resolution (→ `Reopened`) *(prototype)*.
- Reopen after 7 days, or on a ticket that is not `Resolved`, returns `409`.
- With no action for 7 days the ticket auto-closes and the event is recorded.

### AC-UC11 — View assets assigned to me

*Story US11 · Screen SCR-18*

- Only assets currently assigned to me are listed with tag, model and handover date *(prototype)*.
- Other employees' assignments are never returned.

## AI Assistant

### AC-UC12 — Ask a question and get an answer from company guides

*Story US12 · Screens SCR-10, SCR-11*

| Given | When | Then |
|---|---|---|
| A published VPN article exists and the employee may read it | the employee asks how to connect the VPN | the answer lists steps with a citation that opens that article *(prototype)* |
| No trustworthy article exists | the employee asks | the assistant says it has no documented answer and offers the catalog or a draft; no citation is invented *(prototype)* |
| The article belongs to tenant A | an employee of tenant B asks | retrieval never returns tenant A content |

- Draft, retired or restricted articles are never retrieved.

### AC-UC13 — Get step-by-step troubleshooting

*Story US13 · Screen SCR-11*

- Steps come only from cited published articles and are safe for an employee to perform *(prototype)*.
- The assistant offers "It works now" / "Still not working"; "works" ends without a ticket *(prototype)*.
- The assistant never asks for passwords or admin access and never runs actions on the device.

### AC-UC14 — Turn a chat into a ticket draft

*Story US14 · Screens SCR-11, SCR-15*

| Given | When | Then |
|---|---|---|
| The employee described a VPN error without OS and error message | the assistant prepares the request | it asks for the missing fields one by one and does not submit *(prototype)* |
| All required fields are known | the assistant creates the draft | the employee sees type, title and fields with Confirm and Discard *(prototype)* |
| The employee confirms twice or retries after a network error | the backend creates the ticket | the idempotency key prevents a duplicate *(prototype: button disabled)* |
| The assistant proposed a Change but data is incomplete | the employee has not confirmed | no ticket is created |

- The confirmed draft goes through the same validation as AC-UC07.

### AC-UC15 — Ask in chat where my ticket stands

*Story US15 · Screen SCR-11*

| Given | When | Then |
|---|---|---|
| The employee owns INC-1042 | asks "where is my ticket INC-1042?" | the assistant answers with the real status and assignee *(prototype)* |
| The employee asks about a colleague's ticket | the tool query runs | the assistant says it can only see the employee's own tickets; no data is returned *(prototype)* |

## Ticket Management

### AC-UC16 — View and filter the ticket queue

*Story US16 · Screens SCR-20, SCR-21*

- Views *Unassigned / My tickets / All permitted* and filters by type, status, priority, assignee, SLA and requester combine consistently *(prototype for views)*.
- Results contain only the current tenant's tickets; Employees receive `403`.
- An empty result shows "clear filters" *(prototype)*.

### AC-UC17 — Triage and set ticket priority

*Story US17 · Screens SCR-21, SCR-22*

- IT Staff can set type, category and priority; the change is audited with old and new value *(prototype)*.
- A priority suggested by the AI is never applied without an IT action.
- Changing priority restarts SLA targets according to the SLA policy.

### AC-UC18 — Assign or pick up a ticket

*Story US18 · Screens SCR-21, SCR-22*

- A ticket has at most one assignee, who must be an active IT member of the same tenant *(prototype)*.
- Assigning to an employee or another tenant's user returns `400`/`404`.
- Two people picking up the same ticket at once: one succeeds, the other receives `409`.

### AC-UC19 — Update status and technical notes

*Story US19 · Screen SCR-22*

| Given | When | Then |
|---|---|---|
| Ticket is `In Progress` and assigned to the technician | the technician adds an internal note | the note is visible to IT only and marked "Internal note" *(prototype)* |
| Ticket is `Closed` | the technician tries `In Progress` | `409 invalid transition`; only allowed transitions are offered in the UI *(prototype)* |

### AC-UC20 — Transfer or escalate a ticket

*Story US20 · Screen SCR-22*

- Transfer to another team or escalation to the IT Manager requires a reason; empty reason returns `400`.
- Timeline, comments and SLA clock are preserved after the transfer.

### AC-UC21 — Resolve and close a ticket

*Story US21 · Screen SCR-22*

- `Resolved` requires a resolution note; without it the UI shows an error and the API returns `400` *(prototype)*.
- Resolving notifies the requester, who can confirm or reopen (AC-UC10).
- IT cannot set `Closed` directly; closing happens through confirmation or the 7-day rule.

### AC-UC22 — Link a ticket to a device or another ticket

*Story US22 · Screen SCR-22*

- A linked asset or ticket appears on both records.
- Linking to a record of another tenant returns `404`; duplicate links are ignored.

## Catalog, Approval and Fulfilment

### AC-UC23 — Manage request types and forms

*Story US23 · Screen SCR-42*

- A request type can be published only with a name, at least one required field, a routing team and an approval flag.
- Publishing creates a new version; existing tickets keep the version they were created with.
- Hidden types disappear from the catalog immediately; non-admins receive `403`.

### AC-UC24 — Configure approval rules

*Story US24 · Screen SCR-35*

- A rule defines request type, approver and optional conditions (department, cost, asset type) and an effective date.
- New rules apply only to requests submitted after the effective date; recorded decisions never change.

### AC-UC25 — Approve or reject a request with reason

*Story US25 · Screens SCR-30, SCR-03*

| Given | When | Then |
|---|---|---|
| Request is `PendingApproval` | the IT Manager approves | request becomes `Approved` with approver, time and optional note; IT is notified *(prototype)* |
| The manager rejects without a reason | clicks Reject | the error "A reason is required to reject" is shown and nothing changes *(prototype)* |
| IT Staff without approval right | calls the approve endpoint | `403`, state unchanged |
| The request was already decided | approve or reject is called again | `409`, no second decision |

### AC-UC26 — Carry out and record the delivery work

*Story US26 · Screen SCR-23*

- A request that needs approval cannot be fulfilled before `Approved`; the page is locked *(prototype)*.
- Each checklist step is recorded with actor and time; completing all steps resolves the request.

### AC-UC27 — Review and plan an internet provider change *(Phase 2)*

*Story US27 · Screen SCR-31*

- Approval is blocked until impact, affected users, downtime, rollback plan and maintenance window are filled.
- The implementation result must be recorded before `Closed`.
- SmartDesk never triggers a network change automatically.

## IT Assets

### AC-UC28 — Add and update IT devices

*Story US28 · Screens SCR-24, SCR-25*

- Asset tag is unique within the tenant; a duplicate returns `409`.
- Every asset has a lifecycle status; status changes are audited.

### AC-UC29 — Assign and hand over a device

*Story US29 · Screens SCR-23, SCR-25*

| Given | When | Then |
|---|---|---|
| Asset A is `AVAILABLE` and the request is `Approved` | the technician hands over A | A becomes `ASSIGNED`, a handover record is linked to the ticket and the request is resolved *(prototype)* |
| Two technicians assign asset A at the same time | both submit | one succeeds, the other receives `409 conflict` |
| The request is still `PendingApproval` | handover is attempted | `409`; the UI keeps the action disabled *(prototype)* |

### AC-UC30 — Take a device back from an employee

*Story US30 · Screen SCR-25*

- Recovery closes the active assignment, records condition and date, and sets the asset to `RETURNED`.
- Recovering an asset that is not assigned returns `409`.

### AC-UC31 — Log repairs and maintenance *(Phase 2)*

*Story US31 · Screen SCR-25*

- A log entry stores date, work done, technician and status before/after.
- Logging on a `RETIRED` asset returns `409`.

### AC-UC32 — View device stock and history

*Story US32 · Screens SCR-24, SCR-25*

- Counts per status equal the rows in the asset table with no double counting *(prototype)*.
- The IT Manager view is read-only: no add or edit controls are shown *(prototype)*, and write endpoints return `403`.

## Knowledge Base

### AC-UC33 — Write and edit guide drafts

*Story US33 · Screen SCR-26*

- Drafts are visible to IT only and are never returned by employee search or AI retrieval.
- Submitting for review moves the draft to `In review` and notifies IT Managers.

### AC-UC34 — Review, publish and retire guides

*Story US34 · Screen SCR-32*

| Given | When | Then |
|---|---|---|
| The article is a draft | the IT Manager publishes | status is `Published` and only now is it indexed for the AI |
| The article is retired | an employee asks the assistant | the article is not cited in new answers |

### AC-UC35 — Search and read guides without the AI

*Story US35 · Screens SCR-12, SCR-13*

- Keyword and topic search return only published articles the user may read *(prototype)*.
- An article page offers "Still need help?" which opens a request with the article linked *(prototype)*.
- A restricted article opened by URL returns `404` for unauthorized users.

## SLA and Reporting

### AC-UC36 — Set SLA targets by type and priority

*Story US36 · Screen SCR-34*

- Response and resolve targets are set per ticket type and priority using the tenant's business calendar and timezone.
- The clock pauses in `Waiting for Employee`; negative or missing targets return `400`.

### AC-UC37 — Get alerts when a deadline is at risk

*Story US37 · Screens SCR-33, SCR-03*

| Given | When | Then |
|---|---|---|
| A ticket reaches 80% of its resolve target | the SLA job runs | exactly one near-breach alert is sent to the assignee and IT Manager |
| The job retries after a failure | it runs again | no duplicate alert for the same ticket and threshold |

### AC-UC38 — View and export operations reports

*Story US38 · Screen SCR-33*

- KPI cards and charts use the selected date range, team, type and priority *(prototype)*.
- CSV/PDF export contains exactly the on-screen filters and totals.
- Employees and IT Staff receive `403` for reports.

**Related:** [Use cases](02-use-cases.md) · [INVEST requirements](03-invest-requirements.md) · [Information architecture](04-information-architecture.md)
