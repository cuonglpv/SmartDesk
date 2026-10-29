# 04 — Information Architecture (Relume-style sitemap)

> Design status: TARGET V1
>
> 30 pages · 5 role-based areas · 38/38 use cases have an entry screen

The sitemap follows the **Relume** convention: every page is a card, and every card lists the **sections** that make up that page. Because SmartDesk is an internal application, each section is a *functional* block (what the user can see or do), not a marketing block such as "Hero" or "CTA".

## Sitemap overview

![SmartDesk sitemap overview](images/relume/sitemap-overview.png)

```text
SmartDesk
├── Shared
│   ├── SCR-01 Sign In
│   ├── SCR-02 My Profile
│   ├── SCR-03 Notification Center
│   └── SCR-04 Error Pages (403 / 404)
├── Employee Portal
│   ├── SCR-10 Employee Home
│   │   └── SCR-11 AI Assistant
│   ├── SCR-12 Knowledge Base
│   │   └── SCR-13 KB Article
│   ├── SCR-14 Service Catalog
│   │   └── SCR-15 New Request
│   ├── SCR-16 My Requests
│   │   └── SCR-17 Request Detail
│   └── SCR-18 My Assets
├── IT Workspace
│   ├── SCR-20 Agent Dashboard
│   ├── SCR-21 Ticket Queue
│   │   └── SCR-22 Ticket Detail
│   ├── SCR-23 Fulfilment Task
│   ├── SCR-24 Asset Inventory
│   │   └── SCR-25 Asset Detail
│   └── SCR-26 KB Editor
├── Manager Console
│   ├── SCR-30 Approval Inbox
│   │   └── SCR-31 Change Review (Phase 2)
│   ├── SCR-32 KB Review
│   ├── SCR-33 SLA & Reports
│   ├── SCR-34 SLA Policies
│   └── SCR-35 Approval Rules
└── Admin
    ├── SCR-40 Organization Settings
    ├── SCR-41 Members & Roles
    ├── SCR-42 Catalog Builder
    └── SCR-50 Tenants (Platform Admin)
```

## Page cards by area

### Employee Portal

![Relume sitemap — Employee Portal](images/relume/sitemap-employee-portal.png)

### IT Workspace

![Relume sitemap — IT Workspace](images/relume/sitemap-it-workspace.png)

### Manager Console

![Relume sitemap — Manager Console](images/relume/sitemap-manager-console.png)

### Admin

![Relume sitemap — Admin](images/relume/sitemap-admin.png)

### Shared pages

![Relume sitemap — Shared](images/relume/sitemap-shared.png)

## Screen inventory — what each page contains

| Screen | Page | Route | Roles | Functional sections | Use cases |
|---|---|---|---|---|---|
| `SCR-01` | **Sign In** | `/login` | All | Sign-in form; Account status message; Workspace picker; Help link | UC01 |
| `SCR-02` | **My Profile** | `/profile` | All | Profile details; Role & permissions; Notification preferences; Session | UC02, UC01 |
| `SCR-03` | **Notification Center** | `/notifications` | All | Notification list; Filters; Deep link; Mark as read | UC37, UC10, UC25 |
| `SCR-04` | **Error Pages** | `/403, /404` | All | Error message; Safe way back | — |
| `SCR-10` | **Employee Home** | `/app` | Employee | Ask SmartDesk bar; Quick actions; My open tickets; Popular guides; Pending my action | UC06, UC08, UC12, UC35 |
| `SCR-11` | **AI Assistant** | `/app/assistant` | Employee | Conversation; Cited answer; No-source fallback; Guided questions; Ticket draft panel; My ticket status | UC12, UC13, UC14, UC15 |
| `SCR-12` | **Knowledge Base** | `/app/kb` | Employee | Search; Topic filter; Results list; Featured articles | UC35 |
| `SCR-13` | **KB Article** | `/app/kb/:id` | Employee | Article header; Step-by-step content; Was this helpful?; Still need help; Related articles | UC35 |
| `SCR-14` | **Service Catalog** | `/app/catalog` | Employee | Catalog search; Category tabs; Service cards; Not sure? | UC06 |
| `SCR-15` | **New Request** | `/app/requests/new/:type` | Employee | Service summary; Dynamic form; Attachments; What happens next; Review & submit | UC07, UC14 |
| `SCR-16` | **My Requests** | `/app/requests` | Employee | Search; Filters; Ticket table; Empty state | UC08 |
| `SCR-17` | **Request Detail** | `/app/requests/:id` | Employee | Ticket header; Progress tracker; Public conversation; Assignee & approval; Resolution actions | UC08, UC09, UC10 |
| `SCR-18` | **My Assets** | `/app/assets` | Employee | Assigned devices; Handover record; Report a problem | UC11 |
| `SCR-20` | **Agent Dashboard** | `/it` | IT Staff, IT Manager | Workload counters; My priority list; Fulfilment tasks; Quick links | UC16 |
| `SCR-21` | **Ticket Queue** | `/it/tickets` | IT Staff, IT Manager | Queue views; Filters; Ticket table; Inline actions; Empty / loading | UC16, UC17, UC18 |
| `SCR-22` | **Ticket Detail** | `/it/tickets/:id` | IT Staff, IT Manager | Header & SLA; Request context; Reply & notes; Ticket actions; Resolve; Links; Audit timeline | UC17, UC18, UC19, UC20, UC21, UC22 |
| `SCR-23` | **Fulfilment Task** | `/it/fulfilment/:id` | IT Staff | Approval status; Checklist; Asset picker; Handover; Complete | UC26, UC29 |
| `SCR-24` | **Asset Inventory** | `/it/assets` | IT Staff, IT Manager (read) | Stock summary; Search & filters; Asset table; Add asset | UC28, UC32 |
| `SCR-25` | **Asset Detail** | `/it/assets/:id` | IT Staff, IT Manager (read) | Asset profile; Lifecycle status; Assign / recover; Maintenance log; History | UC28, UC29, UC30, UC31, UC32 |
| `SCR-26` | **KB Editor** | `/it/kb` | IT Staff | My drafts; Editor; Visibility; Submit for review | UC33 |
| `SCR-30` | **Approval Inbox** | `/manage/approvals` | IT Manager | Pending list; Filters; Request summary; Decision; Decision history | UC25 |
| `SCR-31` | **Change Review** | `/manage/changes/:id` | IT Manager | Change summary; Impact & rollback; Approval; Schedule & result | UC27 |
| `SCR-32` | **KB Review** | `/manage/kb` | IT Manager | Review queue; Diff & preview; Publish / retire | UC34 |
| `SCR-33` | **SLA & Reports** | `/manage/reports` | IT Manager | Filters; KPI cards; Breach watch; Charts; Export | UC37, UC38 |
| `SCR-34` | **SLA Policies** | `/manage/sla` | IT Manager | Business calendar; Targets matrix; Alert thresholds; Pause rules | UC36 |
| `SCR-35` | **Approval Rules** | `/manage/approval-rules` | IT Manager | Rule list; Approver; Conditions; Effective date | UC24 |
| `SCR-40` | **Organization Settings** | `/admin/org` | Org Admin | Company profile; Locations & departments; Regional settings | UC03 |
| `SCR-41` | **Members & Roles** | `/admin/members` | Org Admin | Member table; Invite; Role assignment; Lock / unlock | UC04 |
| `SCR-42` | **Catalog Builder** | `/admin/catalog` | Org Admin | Request types; Form fields; Routing; Preview & publish | UC23 |
| `SCR-50` | **Tenants** | `/platform/tenants` | Platform Admin | Tenant list; Activate / suspend; Tenant metadata | UC05 |

The one-line description of every section is on the page cards above; the source of truth for both is [`tools/model.py`](../tools/model.py).

## Requirement-to-screen mapping

| Use case | Name | Primary screen(s) |
|---|---|---|
| UC01 | Sign in and sign out | `SCR-01` Sign In, `SCR-02` My Profile |
| UC02 | View and edit my profile | `SCR-02` My Profile |
| UC03 | Update organization settings | `SCR-40` Organization Settings |
| UC04 | Invite, lock and assign member roles | `SCR-41` Members & Roles |
| UC05 | Activate or suspend a tenant | `SCR-50` Tenants |
| UC06 | Browse the IT service catalog | `SCR-10` Employee Home, `SCR-14` Service Catalog |
| UC07 | Submit a request through a typed form | `SCR-15` New Request |
| UC08 | Find and track my tickets | `SCR-10` Employee Home, `SCR-16` My Requests, `SCR-17` Request Detail |
| UC09 | Add comments and files to my ticket | `SCR-17` Request Detail |
| UC10 | Confirm resolution or reopen a ticket | `SCR-03` Notification Center, `SCR-17` Request Detail |
| UC11 | View assets assigned to me | `SCR-18` My Assets |
| UC12 | Ask FAQs answered from internal sources | `SCR-10` Employee Home, `SCR-11` AI Assistant |
| UC13 | Get step-by-step troubleshooting | `SCR-11` AI Assistant |
| UC14 | Draft a ticket through conversation | `SCR-11` AI Assistant, `SCR-15` New Request |
| UC15 | Ask my ticket status in natural language | `SCR-11` AI Assistant |
| UC16 | View and filter the ticket queue | `SCR-20` Agent Dashboard, `SCR-21` Ticket Queue |
| UC17 | Triage and set ticket priority | `SCR-21` Ticket Queue, `SCR-22` Ticket Detail |
| UC18 | Assign or pick up a ticket | `SCR-21` Ticket Queue, `SCR-22` Ticket Detail |
| UC19 | Update status and technical notes | `SCR-22` Ticket Detail |
| UC20 | Transfer or escalate a ticket | `SCR-22` Ticket Detail |
| UC21 | Resolve and close a ticket | `SCR-22` Ticket Detail |
| UC22 | Link a ticket to an asset or ticket | `SCR-22` Ticket Detail |
| UC23 | Manage request types and forms | `SCR-42` Catalog Builder |
| UC24 | Configure approval rules | `SCR-35` Approval Rules |
| UC25 | Approve or reject a request with reason | `SCR-03` Notification Center, `SCR-30` Approval Inbox |
| UC26 | Perform and record fulfilment work | `SCR-23` Fulfilment Task |
| UC27 | Assess and manage an ISP change | `SCR-31` Change Review |
| UC28 | Register and update IT assets | `SCR-24` Asset Inventory, `SCR-25` Asset Detail |
| UC29 | Assign and hand over a device | `SCR-23` Fulfilment Task, `SCR-25` Asset Detail |
| UC30 | Recover a device from an employee | `SCR-25` Asset Detail |
| UC31 | Log asset maintenance and repair | `SCR-25` Asset Detail |
| UC32 | View inventory and asset history | `SCR-24` Asset Inventory, `SCR-25` Asset Detail |
| UC33 | Create and edit KB article drafts | `SCR-26` KB Editor |
| UC34 | Review, publish and retire KB articles | `SCR-32` KB Review |
| UC35 | Search and read KB articles without AI | `SCR-10` Employee Home, `SCR-12` Knowledge Base, `SCR-13` KB Article |
| UC36 | Configure SLA by type and priority | `SCR-34` SLA Policies |
| UC37 | Receive near-breach and breach alerts | `SCR-03` Notification Center, `SCR-33` SLA & Reports |
| UC38 | View and export operations reports | `SCR-33` SLA & Reports |

## Navigation model

```mermaid
flowchart TB
    Login["SCR-01 Sign In"] --> Shell{"Role-aware shell"}
    Shell -->|Employee| EH["SCR-10 Employee Home"]
    Shell -->|IT Staff / IT Manager| AD["SCR-20 Agent Dashboard"]
    Shell -->|IT Manager| AI["SCR-30 Approval Inbox"]
    Shell -->|Org Admin| OS["SCR-40 Organization Settings"]
    Shell -->|Platform Admin| TN["SCR-50 Tenants"]

    EH --> AS["SCR-11 AI Assistant"] -->|confirm draft| RD["SCR-17 Request Detail"]
    EH --> CT["SCR-14 Service Catalog"] --> NR["SCR-15 New Request"] -->|submit| RD
    EH --> KB["SCR-12 Knowledge Base"] --> KA["SCR-13 KB Article"] -->|still need help| NR
    EH --> MR["SCR-16 My Requests"] --> RD

    AD --> Q["SCR-21 Ticket Queue"] --> TD["SCR-22 Ticket Detail"]
    AD --> FT["SCR-23 Fulfilment Task"] --> ADT["SCR-25 Asset Detail"]
    AI -->|approve, notification to IT| FT

    Shell -.->|no permission| ERR["SCR-04 Error Pages"]
```

**Global shell (every authenticated page):** logo and tenant name, role-aware sidebar, scoped search, notification bell (→ `SCR-03`), avatar menu (→ `SCR-02`, sign out), breadcrumbs.

## Navigation rules and deep links

1. **One detail per record.** A ticket opened from AI, catalog, notification or search always lands on the same detail page for that role (`SCR-17` for the requester, `SCR-22` for IT).
2. **Detail pages are not menu items.** Sidebars contain list/home pages only; details open from a list, a notification or a link.
3. **AI draft lives inside the assistant.** It is a panel on `SCR-11`, not a separate page; confirming it reuses the `SCR-15` validation.
4. **Destructive or irreversible actions use a confirm dialog,** not a page (approve, reject, resolve, recover device, publish).
5. **Hand-offs between roles go through notifications.** Approval in `SCR-30` notifies IT, which opens `SCR-23`; resolve in `SCR-22` notifies the employee, who confirms in `SCR-17`.
6. **Errors:** `403` for a missing permission, `404` for missing records **and** for records in another tenant; both offer a link back to the role's home page.

## Page permissions

| Area | Employee | IT Staff | IT Manager | Org Admin | Platform Admin |
|---|---|---|---|---|---|
| Shared (`SCR-01`–`SCR-04`) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Employee Portal (`SCR-10`–`SCR-18`) | ✓ | ✓ | ✓ | ✓ | |
| IT Workspace (`SCR-20`–`SCR-23`, `SCR-26`) | | ✓ | ✓ | | |
| Asset Inventory / Detail (`SCR-24`, `SCR-25`) | | ✓ (write) | ✓ (read) | | |
| Manager Console (`SCR-30`–`SCR-35`) | | | ✓ | | |
| Admin (`SCR-40`–`SCR-42`) | | | | ✓ | |
| Tenants (`SCR-50`) | | | | | ✓ |

Unauthorized items are not rendered in the sidebar, and direct URL access is refused by the API.

## Reusable components

`AppShell`, `RoleAwareSidebar`, `GlobalSearch`, `NotificationBell`, `DataTable`, `FilterBar`, `StatusBadge`, `PriorityBadge`, `SLAIndicator`, `TicketTimeline`, `AttachmentList`, `CitedAnswer`, `TicketDraftCard`, `DynamicForm`, `AssetPicker`, `ConfirmDialog`, `EmptyState`, `ErrorState`, `Skeleton`.

**Related:** [Use cases](02-use-cases.md) · [INVEST requirements](03-invest-requirements.md) · [UI/UX](05-ui-ux.md)
