# Detailed UML — SmartDesk

> **Status:** Code-level design for ASP.NET Core/C#; the backend has not been implemented.

This UML set expands the C3/C4 architecture using the intended class names and target folder structure:

| Document | Content |
|---|---|
| [Class diagrams](01-class-diagrams.md) | Controllers, DTOs, Services, Policies, Validators, Entities, and Repositories for Ticketing and the AI Assistant |
| [Sequence diagrams](02-sequence-diagrams.md) | Submit a request, work and resolve a ticket, confirm or reopen, ask the assistant, and turn a chat into a ticket, including error paths |
| [API traceability](../../api/traceability.md) | Every use case UC01–UC43 mapped to its OpenAPI operations |
| [Folder structure](../../07-folder-structure.md) | Target React and three-tier ASP.NET Core structure |

## Relationship to C4

- C4 Level 3 describes architectural components and their major responsibilities.
- C4 Level 4 describes code-level dependency patterns.
- UML documents classes, methods, and call order for the two core features: Ticket Request & Lifecycle and the AI Assistant.

The [OpenAPI 3.1 specification](../../api/openapi.yaml) is the source of truth for HTTP paths, requests, responses, and the security schemes. The sequence diagrams illustrate the corresponding runtime interactions. The [database design](../../database/README.md) is the source of truth for tables, constraints, and enums.

Idempotent ticket submission, per-kind ticket workflows, the seven-day reopen window, grounded answers with `NO_SOURCE`, and the rule that the assistant never writes are accepted V1 decisions. Diagrams describe TARGET code collaboration; executable tests and backend implementation remain separate evidence.
