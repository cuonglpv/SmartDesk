# C1 — System Context

> **Purpose:** show who uses SmartDesk and what the system is responsible for, without implementation technology.

```mermaid
flowchart LR
    employee(["👤 Employee"])
    itstaff(["👤 IT Staff"])
    manager(["👤 IT Manager"])
    orgadmin(["👤 Org Admin"])
    platform(["👤 Platform Admin"])

    subgraph boundary[" "]
        smartdesk["SmartDesk<br/><i>[Software System]</i><br/>IT requests, service catalog with approval,<br/>IT assets, knowledge base, SLA,<br/>and an AI assistant for employees"]
    end

    ai["External AI Service<br/><i>[Software System]</i><br/>LLM and embedding model"]
    mail["Email Delivery Service<br/><i>[Software System]</i><br/>Invitations and notifications"]

    employee -- "asks the AI, submits and tracks requests" --> smartdesk
    itstaff -- "triages, resolves, hands over devices, writes guides" --> smartdesk
    manager -- "approves, publishes guides, sets SLA, reads reports" --> smartdesk
    orgadmin -- "manages members, organization, and catalog" --> smartdesk
    platform -- "creates, suspends, and audits tenants" --> smartdesk
    smartdesk -- "question + permitted KB excerpts" --> ai
    smartdesk -- "sends email" --> mail

    style smartdesk fill:#1168bd,color:#fff
    style ai fill:#999,color:#fff
    style mail fill:#999,color:#fff
```

## System Boundary

SmartDesk is a multi-tenant SaaS: each customer company is a tenant with its own members, catalog, tickets, assets, and knowledge base. SmartDesk is responsible for sign-in and tenant selection, the service catalog and request forms, incidents, service requests and changes, approvals and fulfilment, the IT asset register and device handover, the knowledge base, the AI assistant, SLA and reports, notifications, and tenant administration.

The External AI Service only interprets questions and composes answers or drafts from excerpts SmartDesk sends; it never writes data, approves, or sees anything the asking user cannot see. The Email Delivery Service receives no internal notes or attachments.

Outside V1 scope: single sign-on with a company identity provider, device management (MDM) and automatic provisioning, chat integrations (Teams, Slack), and inbound email-to-ticket.

## Users and Primary Permissions

| Person | Primary permissions |
|---|---|
| Employee | Self-service: catalog, own requests and comments, confirm or reopen, AI assistant, knowledge base, own devices |
| IT Staff | Ticket queue, triage, assign, resolve, fulfilment, asset register and handover, KB drafts |
| IT Manager | Approval decisions and rules, KB review and publishing, SLA policies and alerts, reports, read-only asset register |
| Org Admin | Members and roles, organization settings, service catalog builder |
| Platform Admin | Tenant creation, suspension, and the platform audit log; no access to tenant content |

Every tenant role inherits Employee self-service. The API enforces role, tenant, and ownership on every request; hiding controls in the UI is only for usability.

**Next:** zoom into the Software System → [C2 — Container](02-container.md).

**Sources of truth:** `docs/01-top-down-research.md`, `docs/02-use-cases.md`, `docs/api/openapi.yaml`.
