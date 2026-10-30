# 01 — Top-down Problem Analysis & Research

> Design status: PRODUCT DEFINITION V1 (29 Oct 2026)
>
> Evidence status: desk research only — no buyer interviews or usability tests have been run yet.

Product name: **SmartDesk** — a multi-tenant SaaS for IT requests, IT assets and internal knowledge, with an AI assistant on the employee side.

## 1.1 Mind map

The analysis goes top-down: business problems → users & roles → service scope → request workflows → AI assistant → business rules & security → delivery roadmap → market & positioning → success metrics. The editable source is [`mindmap/smartdesk.xmind`](mindmap/smartdesk.xmind) (open with XMind; sheet 1 = top-down analysis, sheet 2 = feature map).

![SmartDesk top-down mind map](mindmap/mindmap-top-down.png)

The second sheet decomposes the product into business modules (level 1, with their actors) and concrete user actions (level 2); items marked (V2) are outside the MVP. It is a functional map, not a UML use case diagram: some leaves group several actions and are normalised into use cases in [02 — Use cases](02-use-cases.md).

![SmartDesk feature map](mindmap/mindmap-features.png)

## 1.2 From problem to solution

**Context (who / where).** Companies with 50–500 employees, one or several offices, and an IT team of 2–15 people. Employees need VPN, Wi-Fi, email, software, laptops, printers and access rights.

**Problems (why).**

| ID | Problem | Who feels it |
|---|---|---|
| P1 | Requests arrive through chat, email and walk-ups; nothing tracks them in one place. | Employee, IT Staff |
| P2 | Employees do not know which request type to pick and must describe the issue several times. | Employee |
| P3 | The same incidents repeat while how-to guides are scattered. | Employee, IT Staff |
| P4 | Device provisioning and handover have no approval trail or ownership history. | IT Staff, IT Manager |
| P5 | Managers cannot measure backlog, SLA compliance or workload. | IT Manager |

**Jobs to be done.**

- *Employee:* "When my VPN stops working, I want to try a simple fix or send the right request in a few minutes, so I can keep working and know who is handling it."
- *IT Staff:* "When many requests arrive, I need one queue with complete information and device history, so I can work in order without asking again."
- *IT Manager:* "When I run support and devices, I need SLA, approvals, workload and stock in one view, so I can reduce risk."
- *Org Admin:* "When the company adopts a SaaS tool, I need roles and data isolation, so we can roll it out safely."

**Outcome (what).** Employee self-service + IT service desk + service catalog with approval + asset register + knowledge base + SLA and reporting. AI sits **at the employee intake** to reduce friction; it does not replace business rules.

**Solution direction (how).** Web portal + REST API + relational database; tenant isolation and role-based access; retrieval over published KB articles only; backend tools with explicit permissions; the employee confirms before any ticket is created.

## 1.3 Problem decomposition

| Stage | What happens | Owner of the decision |
|---|---|---|
| Intake | Employee searches the KB / asks the AI or picks a catalog item → a ticket of the right type is created. | Employee confirms; backend validates. |
| Triage | IT classifies Incident / Service Request / Change, sets priority and assignee. | IT Staff (never the AI). |
| Fulfilment | Clarify, update progress, get approval when required, provision device / access / change. | IT Staff; IT Manager approves. |
| Resolution | IT marks Resolved → employee confirms or reopens → closed with audit trail. | Employee + IT Staff. |
| Governance | SLA, permissions, asset data, reports. | IT Manager, Org Admin. |
| AI assistance | Cited FAQ answers, step-by-step guidance, ticket draft, my-ticket lookup. | Backend decides state, approval, permission and data. |

## 1.4 Actors and boundaries

| Actor | Goal | Must not |
|---|---|---|
| Employee | Get help, submit and track requests, confirm resolution | See other people's tickets or devices |
| IT Staff | Work the queue, update tickets, hand over devices, write KB drafts | Approve their own requests when policy forbids it |
| IT Manager | Assign, approve, set SLA, publish KB, report | Access another tenant's data |
| Org Admin | Configure tenant, members, roles, service catalog | Administer other tenants |
| Platform Admin | List, create and activate customer workspaces; suspend or reopen them (Phase 2); read the platform admin log | Read private ticket content by default |
| External AI Service | Interpret questions, compose cited answers, prepare drafts | Write to the database, approve, provision, or read beyond the user's permission |

## 1.5 Business definitions and rules

- **Incident** = a service is broken (e.g. VPN cannot connect). **Service Request** = ask for something new (e.g. VPN access, a laptop). **Change** = a planned modification with impact assessment (e.g. switching the office ISP).
- Approval applies to request types configured to need it; incidents do not need approval.
- SLA is defined per tenant + ticket type + priority with an explicit business calendar; the AI never calculates SLA.
- After IT marks a ticket `Resolved`, the employee can `Confirm` (→ `Closed`) or `Reopen` within **7 days** (configurable); with no answer the ticket auto-closes after the window.
- Asset lifecycle: `AVAILABLE → RESERVED → ASSIGNED → RETURNED / MAINTENANCE → AVAILABLE / RETIRED`; an asset cannot be assigned to two people at the same time.
- Every query, file and embedding is isolated by tenant and by KB visibility.

## 1.6 Market evidence

| Source | What the product shows | Takeaway for SmartDesk |
|---|---|---|
| Atlassian Jira Service Management | Help center, request types, dynamic forms, approvals, queues, SLA, knowledge, assets | The ITSM capability set is proven; SmartDesk keeps an SME-sized subset rather than full ITIL. |
| Freshservice Freddy AI | AI self-service portal, knowledge search, multi-turn intent capture, grounded answers | Putting AI on the employee side is an established pattern, not an arbitrary feature. |

**Positioning hypothesis (to validate).** Existing tools are configured for mid/large IT teams. SmartDesk targets a 2–15 person IT team that wants a ready-made catalog (VPN, laptop, ISP), a simple asset register and an assistant that only answers from its own KB.

**Research limits.** The sources prove that the features exist and are marketed; they do **not** prove that SMEs will pay or at what price. Interviews and a pricing survey are still required.

**Method references (not market evidence).** Relume sitemap and wireframe docs (how to express pages as functional sections) and the [finance-manager](https://github.com/PhamHiep948/finance-manager) repository (documentation structure: mind map → use cases → INVEST → IA).

Sources:

1. Atlassian ITSM guide — https://www.atlassian.com/collections/service/guides/it-service-management
2. Jira Service Management docs — https://support.atlassian.com/jira-service-management-cloud/docs/discover-it-service-management-itsm/
3. Freshservice Freddy AI overview — https://support.freshservice.com/support/solutions/articles/50000011728-freddy-ai-feature-overview
4. Relume sitemap — https://www.relume.ai/resources/docs/building-a-sitemap-with-ai
5. Relume wireframes — https://www.relume.ai/resources/docs/how-to-create-and-edit-wireframes-in-the-relume-site-builder

## 1.7 Scope

| Release | Contents | Use cases |
|---|---|---|
| **Release 1 — MVP** (all P0) | Sign-in, change password, members/roles, catalog with 3 templates (VPN Incident, VPN Access, Laptop Provisioning), request forms, my tickets, AI FAQ + ticket draft, queue/triage/assign/resolve, approval decision, asset register + handover, KB draft/publish/search | 22 |
| **Release 2 — V1 complete** (all P1) | Profile, notification center, org settings and departments, my assets, troubleshooting guidance, my-ticket status via AI, transfer/escalate, links, approval rules, fulfilment checklist, device recovery, inventory view, SLA policies, alerts, reports, organization list, workspace creation, platform admin log | 18 |
| **Phase 2** (P2) | ISP Change template and review, maintenance log, workspace suspend/reopen | 3 |

**Out of scope:** automatic control of VPN/AD/ISP or network configuration, logs/metrics/tracing, on-call paging, multi-agent chatbots, ERP/accounting, real subscription billing, native mobile app.

## 1.8 Hypotheses and success metrics

These are **targets for a pilot**, not market data.

| Hypothesis | Metric | Initial target |
|---|---|---|
| Employees solve more issues themselves | Self-service resolution rate (A/B: AI on/off) | 20–30% |
| Fewer follow-up questions | Tickets complete on first submit | ≥ 75% |
| Faster ticket submission | Time from opening chat/form to submit | −25% vs. plain form |
| AI does not invent answers | Grounded answer rate, citation precision, abstention rate | Prefer abstaining when no source |
| IT works accountably | SLA compliance, reopen rate, queue backlog | Baseline measured in pilot |

**Next research step:** 6–8 employees from two departments, 3–5 technicians and 2 IT managers; test the three journeys below; interviews separate from usability tests.

## 1.9 Key business scenarios

- **S1 — VPN not working (Incident):** employee asks the AI → AI answers from the KB with a citation → employee tries the steps → still broken → AI drafts an Incident with OS, error and screenshot → employee confirms → IT triages and fixes → employee confirms resolution.
- **S2 — New laptop (Service Request):** employee uses the catalog or the AI → recipient, need, needed-by date → manager approval → IT checks available stock → reserve/assign → handover record and audit.
- **S3 — Switch office ISP (Change, Phase 2):** employee proposes the change → site, problem, maintenance window → IT assesses impact and rollback → manager approves → implementation scheduled → result recorded.

**Related:** [Use cases](02-use-cases.md) · [INVEST requirements](03-invest-requirements.md) · [Information architecture](04-information-architecture.md) · [UI/UX](05-ui-ux.md)
