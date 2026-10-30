# C4 Level 4 — Code — Two Core Features

> **Status:** target code-level design for the API Application; the repository currently has no C#/.NET source code.

Level 4 zooms into the **Ticketing** and **AI Assistant** components from [C3](03-component.md): one place to request IT help, and an assistant that answers from the company's own guides and turns a chat into a ticket draft. The two features meet at one point — an assistant draft becomes a ticket only through the employee's own `POST /tickets`. The diagrams define intended responsibilities and dependency directions; they follow the three-project layout in the [folder structure](../../07-folder-structure.md).

| Feature | Use cases | Main OpenAPI operations |
|---|---|---|
| L4.1 Ticket Request & Lifecycle | UC07, UC08, UC10, UC16–UC19, UC21 (P0) | `createTicket`, `getTicket`, `listTicketQueue`, `triageTicket`, `assignTicket`, `updateTicketStatus`, `resolveTicket`, `confirmResolution`, `reopenTicket` |
| L4.2 AI Assistant | UC12, UC14 (P0); UC13, UC15 (P1) | `createAIConversation`, `askAI`, `prepareAITicketDraft`, `discardAITicketDraft` |

## L4.1 Ticket Request & Lifecycle

```mermaid
flowchart TB
    subgraph ticketing["Ticketing [Component]"]
        direction TB
        handler["TicketsController / ItTicketsController<br/><i>[ASP.NET Core Controller]</i><br/>Receives requests and maps DTOs<br/>and HTTP responses"]
        service["TicketService<br/><i>[C# class]</i><br/>Coordinates submit, triage, assign,<br/>status, resolve, confirm, and reopen"]
        policy["TicketPolicy<br/><i>[C# class]</i><br/>Requester vs IT permission,<br/>404 when not visible"]
        validator["ICatalogFormValidator<br/><i>[C# interface]</i><br/>Answers against the published<br/>form version (Service Catalog)"]
        model["Ticket + TicketWorkflow<br/><i>[Domain entity]</i><br/>Status graph per kind, resolution note,<br/>7-day reopen window"]
        repository["ITicketRepository<br/><i>[C# interface]</i><br/>AddAsync, GetForUpdateAsync,<br/>ListMineAsync, QueueAsync"]
        postgres["TicketRepository<br/><i>[C# class]</i><br/>Implements the repository with EF Core"]

        handler --> service
        service --> policy
        service --> validator
        service --> model
        service --> repository
        postgres -.->|"implements"| repository
    end

    api["HTTP API<br/><i>[Component]</i><br/>IdempotencyFilter replays POST /tickets"]
    identity["Identity & Access<br/><i>[Component]</i>"]
    approvals["Approval & Fulfilment<br/><i>[Component]</i><br/>Opens an approval when a rule applies"]
    audit["Audit & Outbox<br/><i>[Component]</i>"]
    db[("PostgreSQL<br/><i>[Container: Database]</i>")]

    api --> handler
    policy --> identity
    service --> approvals
    service -.->|"ticket events, outbox messages"| audit
    postgres --> db

    style handler fill:#1168bd,color:#fff
    style service fill:#0b4f9e,color:#fff
    style policy fill:#1168bd,color:#fff
    style validator fill:#1168bd,color:#fff
    style model fill:#1168bd,color:#fff
    style repository fill:#1168bd,color:#fff
    style postgres fill:#1168bd,color:#fff
```

Primary flow: `TicketsController → TicketService → TicketPolicy / ICatalogFormValidator / Ticket → ITicketRepository`. `IdempotencyFilter` replays a repeated `POST /tickets` before the controller runs. The Unit of Work sets `app.tenant_id` and `app.actor_id` with `SET LOCAL`, and writes the ticket, its `ticket_events`, `audit_logs`, `outbox_messages`, and `idempotency_records` in one transaction. Every command carries `expectedVersion`; a stale `row_version` returns `409 CONCURRENT_MODIFICATION`. The Background Worker closes `RESOLVED` tickets after seven days through the same `Ticket.AutoClose()` rule.

Code location:

```text
SmartDesk.Api/Controllers/            TicketsController.cs, ItTicketsController.cs
SmartDesk.Api/Contracts/Tickets/      CreateTicketRequest.cs, TriageTicketRequest.cs, TicketResponse.cs …
SmartDesk.Application/Tickets/        Ticket.cs, TicketWorkflow.cs, ITicketService.cs, TicketService.cs,
                                      TicketPolicy.cs, TicketQuery.cs, IOwnTicketReader.cs
SmartDesk.Application/Catalog/        ICatalogFormValidator.cs, CatalogFormValidator.cs
SmartDesk.Infrastructure/Persistence/ Repositories/TicketRepository.cs, Configurations/TicketConfiguration.cs
SmartDesk.Worker/Jobs/                AutoCloseResolvedTicketsJob.cs
```

## L4.2 AI Assistant

```mermaid
flowchart TB
    subgraph assistant["AI Assistant [Component]"]
        direction TB
        handler["AiConversationsController<br/><i>[ASP.NET Core Controller]</i><br/>Receives requests and maps DTOs<br/>and HTTP responses"]
        service["AssistantService<br/><i>[C# class]</i><br/>Coordinates ask, prepare draft,<br/>and discard draft"]
        policy["ConversationPolicy<br/><i>[C# class]</i><br/>Only the conversation owner;<br/>404 otherwise"]
        grounding["GroundingPolicy + CitationValidator<br/><i>[C# class]</i><br/>Top-k and minimum score, NO_SOURCE,<br/>citations only from retrieved sources"]
        tools["AssistantToolRegistry<br/><i>[C# class]</i><br/>Read-only tools: my ticket status,<br/>suggest request type"]
        model["AiConversation<br/><i>[Domain entity]</i><br/>Messages, reply kind, sources,<br/>ticket drafts"]
        llm["ILlmClient<br/><i>[C# interface]</i><br/>CompleteAsync with timeout"]
        repository["IAiConversationRepository<br/><i>[C# interface]</i><br/>GetOwnedAsync, AddMessageAsync,<br/>SaveDraftAsync"]
        postgres["AiConversationRepository<br/><i>[C# class]</i><br/>Implements the repository with EF Core"]

        handler --> service
        service --> policy
        service --> grounding
        service --> tools
        service --> model
        service --> llm
        service --> repository
        postgres -.->|"implements"| repository
    end

    api["HTTP API<br/><i>[Component]</i><br/>Rate limit ai-ask → 429"]
    kb["Knowledge Base<br/><i>[Component]</i><br/>IKnowledgeRetriever: tenant + PUBLISHED<br/>+ visibility, checked in SQL"]
    ticketing["Ticketing<br/><i>[Component]</i><br/>IOwnTicketReader (read only)"]
    catalog["Service Catalog<br/><i>[Component]</i><br/>Published forms, answer validation"]
    provider["External AI Service<br/><i>[Software System]</i>"]
    db[("PostgreSQL + pgvector<br/><i>[Container: Database]</i>")]

    api --> handler
    service --> kb
    tools --> ticketing
    tools --> catalog
    service --> catalog
    llm -.->|"HttpLlmClient; 503 AI_UNAVAILABLE on failure"| provider
    postgres --> db
    kb --> db

    style handler fill:#1168bd,color:#fff
    style service fill:#0b4f9e,color:#fff
    style policy fill:#1168bd,color:#fff
    style grounding fill:#1168bd,color:#fff
    style tools fill:#1168bd,color:#fff
    style model fill:#1168bd,color:#fff
    style llm fill:#1168bd,color:#fff
    style repository fill:#1168bd,color:#fff
    style postgres fill:#1168bd,color:#fff
```

Primary flow: `AiConversationsController → AssistantService → ConversationPolicy → IKnowledgeRetriever → GroundingPolicy → ILlmClient → CitationValidator → IAiConversationRepository`. With no source above the score threshold the service returns `NO_SOURCE` with zero citations and does not call the LLM. Citations that are not among the retrieved sources are dropped; with none left the reply becomes `NO_SOURCE`. Tools run with the caller's principal and never write. `PrepareDraftAsync` extracts answers for the published form, validates them, and stores an `ai_ticket_drafts` row; the employee then submits `POST /tickets` with `aiDraftId`, and Ticketing marks the draft `SUBMITTED` in the same transaction.

Code location:

```text
SmartDesk.Api/Controllers/             AiConversationsController.cs
SmartDesk.Api/Contracts/AiAssistant/   AskRequest.cs, AiReplyResponse.cs, PrepareDraftRequest.cs, TicketDraftResponse.cs
SmartDesk.Application/AiAssistant/     AiConversation.cs, IAssistantService.cs, AssistantService.cs, ConversationPolicy.cs,
                                       GroundingPolicy.cs, CitationValidator.cs, PromptBuilder.cs,
                                       Tools/AssistantToolRegistry.cs, Tools/MyTicketStatusTool.cs, Tools/SuggestRequestTypeTool.cs
SmartDesk.Application/Abstractions/Ai/ ILlmClient.cs, IEmbeddingClient.cs
SmartDesk.Application/KnowledgeBase/   IKnowledgeRetriever.cs
SmartDesk.Infrastructure/Ai/           HttpLlmClient.cs, HttpEmbeddingClient.cs
SmartDesk.Infrastructure/Persistence/  Repositories/AiConversationRepository.cs, Queries/PgVectorKnowledgeRetriever.cs
SmartDesk.Worker/Jobs/                 KbIndexingHandler.cs
```

## Shared Rules for Both Features

1. Controllers contain neither SQL nor business rules.
2. Services depend on repository and provider interfaces, not directly on Npgsql, S3, or HTTP clients.
3. Policies are always enforced by the backend; frontend control visibility serves UX only. A resource that exists but is not visible returns `404`.
4. The same `ICatalogFormValidator` validates a manual form and an assistant draft.
5. One command is one transaction: business rows, events, audit, outbox, and idempotency records commit together.
6. Nothing is hard-deleted; cancellation, discard, and retirement are states.
7. P1 behaviour on P0 routes (UC13, UC15, SLA fields) stays behind a feature flag until Release 2.

**Previous:** [C3 — Component](03-component.md) · **Detailed UML:** [Ticketing and AI Assistant class and sequence diagrams](../uml/README.md) · **Folder structure:** [Frontend and three-tier backend](../../07-folder-structure.md) · **Related:** [Use cases](../../02-use-cases.md).
