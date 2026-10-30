# C1 — System Context

> **Status:** target architecture; no backend exists yet. External providers are not chosen.

SmartDesk is a multi-tenant SaaS: each customer company is a **tenant** with its own employees, IT team, catalog, tickets, assets and knowledge base. A sixth actor, the **Platform Admin**, runs the SaaS itself and must never see tenant content.

```mermaid
flowchart TB
    emp["<b>Employee</b><br/><i>[Person]</i><br/>Asks the AI, submits and tracks requests,<br/>reads KB, sees own devices"]
    it["<b>IT Staff</b><br/><i>[Person]</i><br/>Triages, works and resolves tickets,<br/>hands over devices, writes KB drafts"]
    mgr["<b>IT Manager</b><br/><i>[Person]</i><br/>Approves requests, publishes KB,<br/>owns SLA and reports"]
    org["<b>Org Admin</b><br/><i>[Person]</i><br/>Members, organization settings,<br/>service catalog"]
    plat["<b>Platform Admin</b><br/><i>[Person]</i><br/>Creates, suspends and audits tenants;<br/>no access to tenant content"]

    sd["<b>SmartDesk</b><br/><i>[Software System]</i><br/>IT service desk, service catalog with approval,<br/>asset register, knowledge base and an AI assistant<br/>that answers only from published articles"]

    ai["<b>External AI Service</b><br/><i>[Software System, external]</i><br/>LLM for answers and drafts;<br/>embedding model for KB search"]
    mail["<b>Email Delivery Service</b><br/><i>[Software System, external]</i><br/>Invitations and notifications"]

    emp -- "Uses (browser, HTTPS)" --> sd
    it -- "Uses" --> sd
    mgr -- "Uses" --> sd
    org -- "Uses" --> sd
    plat -- "Uses (platform area)" --> sd
    sd -- "Sends question + permitted KB excerpts;<br/>gets answer / draft (HTTPS)" --> ai
    sd -- "Sends emails (SMTP or HTTPS API)" --> mail
    mail -. "Delivers email" .-> emp

    style sd fill:#08427b,color:#fff,stroke:#052e56
    style emp fill:#999,color:#fff,stroke:#666
    style it fill:#999,color:#fff,stroke:#666
    style mgr fill:#999,color:#fff,stroke:#666
    style org fill:#999,color:#fff,stroke:#666
    style plat fill:#999,color:#fff,stroke:#666
    style ai fill:#bbb,color:#000,stroke:#888
    style mail fill:#bbb,color:#000,stroke:#888
```

## Actors

| Actor | Main use cases | Can never |
|---|---|---|
| Employee | UC01–UC02, UC06–UC15, UC35, UC39–UC40 | See another employee's tickets or assets, internal notes, unpublished articles |
| IT Staff | UC16–UC22, UC26, UC28–UC31, UC33 | Approve requests, publish KB, force a ticket to `CLOSED` |
| IT Manager | UC18, UC20, UC24–UC25, UC27, UC32, UC34, UC36–UC38 | Write assets (read-only register) |
| Org Admin | UC03–UC04, UC23 | Work tickets, approve |
| Platform Admin | UC05, UC41–UC43 | Read tickets, attachments, articles or assets of any tenant |
| External AI Service | Secondary actor on UC12–UC15 | Write data, call SmartDesk APIs, see anything the asking user cannot see |

Every tenant user is an Employee as well (role grants inherit self-service), so IT Staff, IT Managers and Org Admins can also submit their own requests.

## External systems

| System | Data sent | Trust rule |
|---|---|---|
| External AI Service (LLM + embeddings) | The user's question, conversation turns, KB excerpts the user is allowed to read, the published form schema when drafting | Treated as untrusted output: citations are validated, the provider has no tools that write, no database credentials, no tenant IDs beyond what the request needs |
| Email Delivery Service | Recipient address, notification text, invitation link | Contains no internal notes or attachments; links require sign-in |

## Out of scope for the MVP

- Single sign-on with a company identity provider (SmartDesk uses its own email + password, UC01/UC39).
- Device management (MDM) or automatic provisioning — handover is recorded by IT staff, not executed by SmartDesk.
- Chat integrations (Teams, Slack) and inbound email-to-ticket.

---

**Next:** [C2 — Container](02-container.md) · **Up:** [C4 overview](README.md)
