# C4 Model — SmartDesk

> **Status:** Architecture baseline · **Audience:** developers, reviewers, and maintainers

The documentation proceeds from the outside in. Every node has a **name**, **type** (`Person`, `Software System`, `Container`, `Component`), technology where relevant, and a short description.

```mermaid
flowchart LR
    C1["C1 · System Context<br/><small>Who uses the system?</small>"]
    C2["C2 · Container<br/><small>What runtime units make up the system?</small>"]
    C3["C3 · Component<br/><small>How is the API Application decomposed?</small>"]
    C4["C4 · Code<br/><small>How are the two core features organized?</small>"]
    C1 -->|"zoom into SmartDesk"| C2
    C2 -->|"zoom into API Application"| C3
    C3 -->|"zoom into Ticketing & AI Assistant"| C4
    style C1 fill:#1168bd,color:#fff,stroke:#0b4884
    style C2 fill:#1168bd,color:#fff,stroke:#0b4884
    style C3 fill:#1168bd,color:#fff,stroke:#0b4884
    style C4 fill:#1168bd,color:#fff,stroke:#0b4884
```

| Level | Document | Scope |
|---|---|---|
| C1 | [System Context](01-system-context.md) | Five roles, the SmartDesk boundary, the External AI Service and email delivery |
| C2 | [Container](02-container.md) | Web App, API Application, Background Worker, PostgreSQL + pgvector, file storage |
| C3 | [Component](03-component.md) | Components inside the API Application and the Background Worker |
| C4 | [Code — two core features](04-code.md) | C# classes/interfaces for Ticket Request & Lifecycle and the AI Assistant |

## Implementation Status

| Unit | Actual status |
|---|---|
| UX prototype | Single file `prototype/index.html` with mock data |
| Web App (React) | Not started |
| API Application / Background Worker | Not started; [OpenAPI 0.4.1-draft](../../api/openapi.yaml) defines 105 proposed operations |
| PostgreSQL | [Database design revision 2.3](../../database/README.md): DBML + constraints, applied to PGlite (38/38 scenarios), not deployed |
| File storage, AI provider, email | Not chosen |

The diagrams describe the **target architecture**. Technologies (React, ASP.NET Core, PostgreSQL) are the working assumption for the first implementation and can change without changing C1–C3.

## Color Conventions

- Dark blue: the primary unit being described.
- Light blue: a neighboring element in the same system.
- Gray: a user or element outside the boundary being zoomed.
- Dashed line: a Software System or Container boundary.

See also: [Use cases](../../02-use-cases.md#use-case-catalog) · [Detailed UML](../uml/README.md) · [Folder structure](../../07-folder-structure.md).
