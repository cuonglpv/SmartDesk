# C3 — Component — API Application

> **Status:** target architecture. The components below do not yet have C#/.NET source code in the repository.

```mermaid
flowchart TB
    subgraph rt["API Application [Container]"]
        direction TB
        api["HTTP API<br/><i>[Component: ASP.NET Core]</i><br/>REST endpoints, session and CSRF checks,<br/>Idempotency-Key, Problem Details"]
        identity["Identity & Access<br/><i>[Component]</i><br/>Sign-in, sessions, tenant context,<br/>roles → permissions, ownership"]
        org["Organization & Platform<br/><i>[Component]</i><br/>Members, departments, locations, teams,<br/>tenant lifecycle, platform audit"]
        catalog["Service Catalog<br/><i>[Component]</i><br/>Request types, form versions,<br/>approval rules, form validation"]
        tickets["Ticketing<br/><i>[Component]</i><br/>Submit, comment, triage, assign,<br/>resolve, confirm / reopen"]
        approvals["Approval & Fulfilment<br/><i>[Component]</i><br/>Approval decisions, fulfilment steps,<br/>change plans"]
        assets["IT Assets<br/><i>[Component]</i><br/>Register, handover, recovery,<br/>maintenance, history"]
        kb["Knowledge Base<br/><i>[Component]</i><br/>Drafts, review, publish / retire,<br/>search, retrieval for the AI"]
        assistant["AI Assistant<br/><i>[Component]</i><br/>Grounded answers, read-only tools,<br/>ticket drafts"]
        sla["SLA & Reporting<br/><i>[Component]</i><br/>Policies, business calendar,<br/>alerts, KPIs, exports"]
        audit["Audit & Outbox<br/><i>[Component]</i><br/>Audit log and outbox messages<br/>in the business transaction"]
        fileStore["File Storage Adapter<br/><i>[Component]</i><br/>Upload staging, allow-list,<br/>10 MiB limit, signed URLs"]
        persistence["Persistence<br/><i>[Component]</i><br/>Repositories, tenant query filter,<br/>unit of work, row_version"]
    end

    web["Web App<br/><i>[Container: React]</i>"]
    db[("PostgreSQL + pgvector<br/><i>[Container: Database]</i>")]
    store[("File Storage<br/><i>[Container]</i>")]
    llm["External AI Service<br/><i>[Software System]</i>"]

    web --> api
    api --> identity
    api --> org
    api --> catalog
    api --> tickets
    api --> approvals
    api --> assets
    api --> kb
    api --> assistant
    api --> sla
    tickets --> catalog
    tickets --> approvals
    tickets --> fileStore
    approvals --> assets
    assistant -->|"published, visible chunks"| kb
    assistant -->|"own tickets (read only)"| tickets
    assistant -->|"published forms"| catalog
    assistant --> llm
    identity --> persistence
    org --> persistence
    catalog --> persistence
    tickets --> persistence
    approvals --> persistence
    assets --> persistence
    kb --> persistence
    assistant --> persistence
    sla --> persistence
    tickets -.->|"ticket events"| audit
    approvals -.->|"decisions"| audit
    assets -.->|"custody events"| audit
    kb -.->|"publish / retire"| audit
    audit --> persistence
    persistence --> db
    fileStore --> store

    style api fill:#1168bd,color:#fff
    style identity fill:#1168bd,color:#fff
    style org fill:#1168bd,color:#fff
    style catalog fill:#1168bd,color:#fff
    style tickets fill:#0b4f9e,color:#fff
    style approvals fill:#1168bd,color:#fff
    style assets fill:#1168bd,color:#fff
    style kb fill:#1168bd,color:#fff
    style assistant fill:#0b4f9e,color:#fff
    style sla fill:#1168bd,color:#fff
    style audit fill:#1168bd,color:#fff
    style fileStore fill:#1168bd,color:#fff
    style persistence fill:#1168bd,color:#fff
```

The two darker components, **Ticketing** and **AI Assistant**, are the core features zoomed into at [C4 — Code](04-code.md).

## Component catalog

| Component | Owns | Does not own |
|---|---|---|
| HTTP API | Transport, session and CSRF checks, idempotency replay, error contract | SQL and business decisions |
| Identity & Access | Sign-in, sessions and refresh rotation, tenant context, permissions, ownership rule | UI visibility |
| Organization & Platform | Members and invitations, departments, locations, teams, tenant lifecycle, platform audit | Tenant content (tickets, articles, files) |
| Service Catalog | Request types, immutable form versions, approval rules, answer validation | Tickets |
| Ticketing | Ticket lifecycle per kind, comments, attachments, timeline, links | Approval decisions and asset state |
| Approval & Fulfilment | Approval inbox and decisions, fulfilment steps, change plans | Approval rules (Service Catalog) |
| IT Assets | Asset register, single active assignment, handover and recovery, maintenance | Ticket status (asks Ticketing to resolve) |
| Knowledge Base | Article versions, independent review, publishing, search, retrieval of published chunks | Embedding at request time (worker) |
| AI Assistant | Conversations, grounding and citation checks, read-only tools, ticket drafts | Creating tickets — the employee calls `POST /tickets` |
| SLA & Reporting | SLA policies, business calendar, alerts, KPIs, exports | Ticket transitions |
| Audit & Outbox | `audit_logs`, `outbox_messages`, `idempotency_records` | Primary operational data |
| File Storage Adapter | File validation, generated keys, binary persistence | Who may see an attachment (Ticketing) |
| Persistence | Repositories, SQL, transactions, optimistic locking | HTTP and UI authorization |

## Dependency Flow

`HTTP API → Identity & Access → business component → Persistence → PostgreSQL`.

Ticketing calls the Service Catalog to validate answers and resolve the approval rule. The AI Assistant reads through Knowledge Base, Ticketing, and Service Catalog interfaces only. No business component opens its own PostgreSQL connection or reads another component's tables.

The **Background Worker** reuses Application and Persistence: an Outbox Dispatcher sends email and triggers KB indexing; scheduled jobs auto-close resolved tickets after seven days, raise SLA warnings, scan uploads, and purge expired idempotency records and uploads. Every job is idempotent and claims rows with `FOR UPDATE SKIP LOCKED`.

## AI Assistant Write Boundary

**Status:** ACCEPTED

### Confirmed requirement

The assistant never submits a ticket, approves a request, or changes an asset (UC12–UC15, `docs/01-top-down-research.md` §5).

The AI Assistant depends only on read interfaces: `IKnowledgeRetriever`, `IOwnTicketReader`, and `IPublishedCatalogReader`. A draft becomes a ticket only through the employee's own `POST /tickets`, which runs the same Ticketing validation as a manual submission. Architecture tests fail the build if the AI Assistant references a write service; integration test T15 checks that no ticket exists before the employee submits.

**Previous:** [C2 — Container](02-container.md) · **Next:** [C4 — Code for Ticketing and the AI Assistant](04-code.md) · **Related:** [Folder structure](../../07-folder-structure.md).

**Sources of truth:** `docs/02-use-cases.md`, `docs/api/openapi.yaml`, `docs/database/smartdesk.dbml`.
