# C3 — Component — API Application and Background Worker

> **Status:** target architecture; no C#/.NET source exists yet. The API is a **modular monolith**: one deployable, one database, modules that talk only through each other's public interfaces.

## API Application

```mermaid
flowchart TB
    spa["Web App<br/><i>[Container: React SPA]</i>"]

    subgraph apiC["API Application [Container: ASP.NET Core 8]"]
        direction TB
        pipe["<b>HTTP Pipeline</b><br/><i>[Component: middleware]</i><br/>Session auth, TenantContext, CSRF, rate limit,<br/>Idempotency filter, ProblemDetails, audit context"]

        subgraph mods["Business modules"]
            direction TB
            idn["<b>Identity & Access</b><br/><i>[Component]</i><br/>Sign-in, sessions, memberships,<br/>roles → permissions, password"]
            orgm["<b>Organization</b><br/><i>[Component]</i><br/>Settings, departments, teams,<br/>members, invitations"]
            platm["<b>Platform</b><br/><i>[Component]</i><br/>Tenants lifecycle, platform audit"]
            cat["<b>Catalog</b><br/><i>[Component]</i><br/>Request types, form versions,<br/>approval rules, form validation"]
            tkt["<b>Ticketing</b><br/><i>[Component — C4 feature 1]</i><br/>Create, read, comment, triage, assign,<br/>status, resolve, confirm/reopen, links"]
            apr["<b>Approvals & Fulfilment</b><br/><i>[Component]</i><br/>Approval inbox/decision, fulfilment<br/>steps, change plans"]
            ast["<b>Assets</b><br/><i>[Component]</i><br/>Register, handover,<br/>recover, maintenance, history"]
            kb["<b>Knowledge Base</b><br/><i>[Component]</i><br/>Drafts, review, publish/retire,<br/>search, feedback"]
            aia["<b>AI Assistant</b><br/><i>[Component — C4 feature 2]</i><br/>Conversations, grounded answers,<br/>read-only tools, ticket drafts"]
            sla["<b>SLA & Reporting</b><br/><i>[Component]</i><br/>Policies, business calendar,<br/>alerts, KPIs, exports"]
            ntf["<b>Notifications</b><br/><i>[Component]</i><br/>In-app inbox; enqueue email"]
        end

        subgraph shared["Shared kernel"]
            direction LR
            files["<b>File Service</b><br/><i>[Component]</i><br/>Upload staging, allow-list,<br/>10 MiB limit, signed URLs"]
            aud["<b>Audit & Outbox</b><br/><i>[Component]</i><br/>audit_logs, outbox_messages<br/>in the same transaction"]
            persist["<b>Persistence</b><br/><i>[Component: EF Core]</i><br/>DbContext, tenant query filter,<br/>unit of work, row_version"]
        end
    end

    db[("Database<br/><i>[PostgreSQL + pgvector]</i>")]
    store[("File Storage<br/><i>[S3-compatible]</i>")]
    ai["External AI Service"]

    spa -- "JSON/HTTPS" --> pipe
    pipe --> mods
    idn -. "permissions" .-> pipe
    tkt -- "validate answers,<br/>resolve approval rule" --> cat
    tkt -- "open approval" --> apr
    apr -- "handover needs<br/>approved ticket" --> ast
    aia -- "retrieve published,<br/>visible chunks" --> kb
    aia -- "own-ticket status (read),<br/>draft validation" --> tkt
    aia -- "published forms" --> cat
    aia -- "chat + embeddings" --> ai
    tkt -- "SLA snapshot (P1)" --> sla
    tkt --> files
    mods --> aud
    mods --> persist
    persist --> db
    files --> store

    style tkt fill:#08427b,color:#fff,stroke:#052e56
    style aia fill:#08427b,color:#fff,stroke:#052e56
    style pipe fill:#1168bd,color:#fff,stroke:#0b4884
    style idn fill:#438dd5,color:#fff,stroke:#2e6295
    style orgm fill:#438dd5,color:#fff,stroke:#2e6295
    style platm fill:#438dd5,color:#fff,stroke:#2e6295
    style cat fill:#438dd5,color:#fff,stroke:#2e6295
    style apr fill:#438dd5,color:#fff,stroke:#2e6295
    style ast fill:#438dd5,color:#fff,stroke:#2e6295
    style kb fill:#438dd5,color:#fff,stroke:#2e6295
    style sla fill:#438dd5,color:#fff,stroke:#2e6295
    style ntf fill:#438dd5,color:#fff,stroke:#2e6295
    style files fill:#85bbf0,color:#000,stroke:#5d82a8
    style aud fill:#85bbf0,color:#000,stroke:#5d82a8
    style persist fill:#85bbf0,color:#000,stroke:#5d82a8
    style spa fill:#999,color:#fff,stroke:#666
    style db fill:#999,color:#fff,stroke:#666
    style store fill:#999,color:#fff,stroke:#666
    style ai fill:#bbb,color:#000,stroke:#888
    style apiC stroke-dasharray: 5 5
```

## Component catalog

| Component | OpenAPI tags / paths | Owns (DB tables) | Does not own |
|---|---|---|---|
| HTTP Pipeline | all | — | Business rules; it only builds `ICurrentPrincipal` and rejects bad requests early |
| Identity & Access | Authentication, Identity · `/auth/*`, `/me`, `/me/password` | `users`, `user_sessions`, `memberships`, `membership_roles` | Org structure, invitations UI |
| Organization | Organization, Members · `/organization/**`, `/invitations/accept` | `departments`, `locations`, `it_teams`, `it_team_members`, invite columns of `memberships` | Platform tenants |
| Platform | Platform · `/platform/**` | `tenants`, `tenant_counters` (create), `audit_logs` where scope = PLATFORM | Any tenant content |
| Catalog | Catalog, Catalog Administration · `/catalog/**`, `/admin/request-types/**`, `/approval-rules/**` | `catalog_items`, `catalog_versions`, `approval_rules` | Tickets |
| **Ticketing** | Tickets, IT Tickets, Attachments · `/tickets/**`, `/it/dashboard`, `/it/tickets/**` (except fulfilment and change) | `tickets`, `ticket_comments`, `ticket_attachments`, `ticket_events`, `ticket_links`, `ticket_assets` | Approval decisions, asset state |
| Approvals & Fulfilment | Approvals, Fulfilment, Change Management · `/approvals/**`, `/it/tickets/{ticketId}/fulfilment-steps`, `/it/tickets/{ticketId}/change-*` | `ticket_approvals`, `fulfilment_steps`, `change_plans` | Approval rules (Catalog) |
| Assets | Assets · `/assets/**` | `assets`, `asset_assignments`, `asset_maintenance` | Ticket status (asks Ticketing to resolve) |
| Knowledge Base | Knowledge Base, Knowledge Authoring, Knowledge Review · `/kb/**`, `/it/kb/**`, `/manager/kb/**` | `kb_articles`, `kb_article_versions`, `kb_chunks` (written by the worker), `kb_feedback` | Embedding calls at request time |
| **AI Assistant** | AI Assistant · `/ai/**` | `ai_conversations`, `ai_messages`, `ai_message_sources`, `ai_ticket_drafts` | Creating tickets — the employee calls `POST /tickets` |
| SLA & Reporting | SLA, Reporting · `/sla/**`, `/reports/**` | `sla_policies`, `ticket_sla`, `tenant_holidays`, calendar columns of `tenants` | Ticket transitions |
| Notifications | Notifications · `/me/notifications/**` | `notifications` | Email delivery (worker) |
| File Service | `/uploads`, attachment download | Objects in File Storage; staging metadata | Deciding who may see an attachment (Ticketing) |
| Audit & Outbox | — | `audit_logs`, `outbox_messages`, `idempotency_records` | — |

## Dependency rules

1. **Modules call each other only through a public interface** in their `*.Contracts` namespace (for example Ticketing calls `ICatalogFormValidator`, never `CatalogDbContext`).
2. **No module reads another module's tables.** Reporting is the one exception and does so through read-only SQL views.
3. **The AI Assistant has no write path into other modules.** Its tools are the read-only interfaces `IOwnTicketReader`, `IKnowledgeRetriever` and `IPublishedCatalogReader`; a ticket is created only by the employee's own `POST /tickets` (UC14, test T15).
4. **Every module command runs inside the unit of work** that sets `app.tenant_id` / `app.actor_id` for the connection and commits audit + outbox rows together.
5. **Authorization is three checks, always in this order:** permission from `x-permissions` → tenant (implicit in every query) → ownership and state in the module. A resource that fails the tenant or ownership check returns `404`, never `403` (tests T01, T03, T20).

## Background Worker

```mermaid
flowchart LR
    subgraph wk["Background Worker [Container: .NET Worker Service]"]
        direction TB
        disp["<b>Outbox Dispatcher</b><br/><i>[Component]</i><br/>Claims outbox rows (SKIP LOCKED),<br/>routes by message type"]
        mailer["<b>Email Sender</b><br/><i>[Component]</i><br/>Invitations, ticket updates,<br/>approval requests"]
        idx["<b>KB Indexer</b><br/><i>[Component]</i><br/>On publish: chunk + embed → kb_chunks;<br/>on retire: delete chunks"]
        close["<b>Auto-close Job</b><br/><i>[Component]</i><br/>RESOLVED older than 7 days → CLOSED,<br/>one event per ticket"]
        slaj["<b>SLA Monitor (P1)</b><br/><i>[Component]</i><br/>80% warning, 100% breach,<br/>dedupe per threshold"]
        scan["<b>Upload Scanner</b><br/><i>[Component]</i><br/>Malware scan → CLEAN / INFECTED"]
        ret["<b>Retention Job</b><br/><i>[Component]</i><br/>Expired uploads, idempotency records,<br/>old AI conversations"]
    end
    db[("Database")]
    store[("File Storage")]
    ai["External AI Service"]
    mail["Email Delivery Service"]

    disp --> mailer
    disp --> idx
    mailer --> mail
    idx --> ai
    idx --> db
    disp --> db
    close --> db
    slaj --> db
    scan --> store
    scan --> db
    ret --> db
    ret --> store

    style wk stroke-dasharray: 5 5
    style disp fill:#08427b,color:#fff,stroke:#052e56
    style mailer fill:#438dd5,color:#fff,stroke:#2e6295
    style idx fill:#438dd5,color:#fff,stroke:#2e6295
    style close fill:#438dd5,color:#fff,stroke:#2e6295
    style slaj fill:#438dd5,color:#fff,stroke:#2e6295
    style scan fill:#438dd5,color:#fff,stroke:#2e6295
    style ret fill:#438dd5,color:#fff,stroke:#2e6295
    style db fill:#999,color:#fff,stroke:#666
    style store fill:#999,color:#fff,stroke:#666
    style ai fill:#bbb,color:#000,stroke:#888
    style mail fill:#bbb,color:#000,stroke:#888
```

Every job is **idempotent**: it re-reads state under a row lock and does nothing if the change already happened, so a retry or a second worker instance cannot send a duplicate alert or write a second close event (tests T13, T24).

## Cross-cutting decisions

| Concern | Decision |
|---|---|
| Tenant isolation | `ICurrentPrincipal.TenantId` from the session; EF Core global query filter on `tenant_id`; composite FKs in the DB as the last line of defence. PostgreSQL RLS can be added later as defence in depth. |
| Concurrency | Every command takes `expectedVersion`; EF Core concurrency token on `row_version`; stale → `409 CONCURRENT_MODIFICATION` (tests T06, T07, T18). |
| Idempotency | `IdempotencyFilter` on `POST /tickets`; `idempotency_records` keyed by tenant + member + method + path + key with a request hash (review R05). |
| Errors | One `ProblemDetailsFactory`; `errorCode` from a single enum (review R06); `traceId` = `Activity.TraceId`. |
| Feature gating | `IFeatureGate` per use case and release (P0 / P1 / P2), because several P0 routes also serve P1 use cases (README §2, review guide D14). |
| Observability | OpenTelemetry traces and metrics; AI calls record model, token counts and latency in `ai_messages`. Prompts and KB excerpts are never written to logs. |

---

**Previous:** [C2 — Container](02-container.md) · **Next:** [C4 — Code](04-code.md)
