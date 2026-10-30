# C2 — Container

> **Purpose:** zoom into SmartDesk and describe runtime and storage units in the target architecture.

```mermaid
flowchart TB
    tenantUsers(["👤 Employee / IT Staff / IT Manager / Org Admin"])
    platformAdmin(["👤 Platform Admin"])

    subgraph platform["SmartDesk [Software System Boundary]"]
        direction TB
        subgraph presentation["Presentation"]
            web["Web App<br/><i>[Container: React + TypeScript + Vite]</i><br/>Employee Portal, IT Workspace, Manager Console,<br/>Org Admin, and Platform areas"]
        end
        subgraph application["Application"]
            api["API Application<br/><i>[Container: ASP.NET Core Web API]</i><br/>Authentication, tenant context, RBAC + ownership,<br/>ticket workflows, AI orchestration"]
            worker["Background Worker<br/><i>[Container: .NET Worker Service]</i><br/>Outbox, notifications, 7-day auto-close,<br/>SLA timers, KB indexing, file scanning"]
        end
        subgraph data["Data"]
            database[("PostgreSQL + pgvector<br/><i>[Container: Database]</i><br/>40 tables with composite tenant keys,<br/>KB embeddings, outbox")]
            files[("File Storage<br/><i>[Container: S3-compatible object storage]</i><br/>Uploads, attachments, report exports")]
        end
    end

    ai["External AI Service<br/><i>[Software System]</i>"]
    mail["Email Delivery Service<br/><i>[Software System]</i>"]

    tenantUsers --> web
    platformAdmin --> web
    web -- "REST / HTTPS / JSON<br/>bearer access token;<br/>refresh via HttpOnly cookie" --> api
    api -- "SQL / PostgreSQL protocol" --> database
    api -- "objects / short-lived signed URLs" --> files
    api -- "chat completion, embeddings" --> ai
    worker -- "outbox and due timers" --> database
    worker -- "scan uploads" --> files
    worker -- "embeddings for published KB" --> ai
    worker -- "SMTP / HTTPS" --> mail

    style web fill:#1168bd,color:#fff
    style api fill:#1168bd,color:#fff
    style worker fill:#1168bd,color:#fff
    style database fill:#1168bd,color:#fff
    style files fill:#3a7bd5,color:#fff
    style ai fill:#999,color:#fff
    style mail fill:#999,color:#fff
```

## Responsibilities

| Container | Technology | Responsibility | Status |
|---|---|---|---|
| Web App | React, TypeScript, Vite; client generated from OpenAPI | Screens, route guards, forms, Problem Details by `errorCode`, `Idempotency-Key` on submit | Prototype only (`prototype/index.html`) |
| API Application | C#, ASP.NET Core Web API, REST/JSON | Trust boundary for authentication, tenant, RBAC, ownership, workflows, and AI orchestration | Not implemented; [OpenAPI 0.4.1-draft](../../api/openapi.yaml) |
| Background Worker | C#, .NET Worker Service | Outbox dispatch, email, auto-close after 7 days, SLA warnings, KB indexing, upload scanning, retention | Not implemented |
| PostgreSQL + pgvector | PostgreSQL 16+, `pgvector`, `btree_gist` | Source of truth; composite tenant FKs; KB chunk embeddings | [Design revision 2.3](../../database/README.md); verified on PGlite |
| File Storage | Private S3-compatible bucket | Binary files keyed by tenant; PostgreSQL keeps metadata only | Not chosen |

## Architecture Rules

1. The browser never accesses PostgreSQL, file storage, or the AI provider directly.
2. Hiding frontend controls is UX only; the API Application authorizes every request by permission, tenant, ownership, and state.
3. The tenant comes only from the verified session, never from a client header, path, or body.
4. One command is one transaction: business rows, `ticket_events` / `audit_logs`, and `outbox_messages` commit together; the worker reads the outbox, so no notification is sent for a rolled-back change.
5. The AI provider receives only KB excerpts already filtered by tenant, `PUBLISHED` status, and the caller's visibility; it has no tools that write.
6. The access token lives in SPA memory; the refresh token is only the `sd_refresh` HttpOnly cookie (`SameSite=Strict`), rotated on every refresh and checked with a double-submit `X-CSRF-Token`.
7. Platform Admin sessions are accepted only by `/platform/**` and never by tenant endpoints.

## Current State

```mermaid
flowchart LR
    user(["👤 User"])
    proto["UX Prototype<br/><i>prototype/index.html</i>"]
    mock["Mock data<br/><i>JavaScript in the page</i>"]
    contract["OpenAPI 0.4.1-draft<br/><i>design only</i>"]
    pg[("PostgreSQL design rev. 2.3<br/><i>not deployed</i>")]
    user --> proto --> mock
    contract -.->|"no runtime connection"| proto
    pg -.->|"data design only"| contract
    style proto fill:#1168bd,color:#fff
    style mock fill:#3a7bd5,color:#fff
    style contract fill:#999,color:#fff
    style pg fill:#999,color:#fff
```

**Previous:** [C1 — System Context](01-system-context.md) · **Next:** zoom into the API Application → [C3 — Component](03-component.md).
