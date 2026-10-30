# Sequence Diagrams — Ticketing and AI Assistant

> **Scope:** Ticket Request & Lifecycle and the AI Assistant · **Status:** Target design; no backend implemented  
> The `/v1/...` endpoints follow [OpenAPI 3.1](../../api/openapi.yaml).

The diagrams share one presentation pattern: **Actor → Page → Controller → Application Service → Repository → PostgreSQL**. Requests use solid arrows, responses use dashed arrows; `alt` describes mutually exclusive outcomes and `opt` describes optional processing.

## 1. Submit a request — `POST /v1/tickets`

```mermaid
sequenceDiagram
    actor User as Employee
    participant Page as New Request Page
    participant Filter as IdempotencyFilter
    participant API as TicketsController
    participant Service as TicketService
    participant Catalog as ICatalogFormValidator
    participant Repo as ITicketRepository
    participant DB as PostgreSQL

    User->>Page: Fill the request form and click Submit
    activate Page
    Page->>Filter: POST /v1/tickets + Idempotency-Key
    activate Filter
    Filter->>DB: SELECT idempotency_records by scope and key
    activate DB
    DB-->>Filter: Record or none
    deactivate DB

    alt Same key and same request hash
        Filter-->>Page: Replay stored 201 (Idempotent-Replayed: true)
    else Same key and different request hash
        Filter-->>Page: 409 IDEMPOTENCY_KEY_REUSED
    else New key
        Filter->>API: Continue
        activate API
        API->>Service: SubmitAsync(actor, command)
        activate Service
        Service->>Catalog: ValidateAsync(requestTypeId, version, answers)
        activate Catalog
        Catalog-->>Service: Field errors, stale version, or valid form
        deactivate Catalog

        alt Hidden or outdated request type version
            Service-->>API: CATALOG_VERSION_STALE
            API-->>Page: 409 Conflict
            Page-->>User: Reload the latest form
        else Missing or invalid fields
            Service-->>API: VALIDATION_FAILED
            API-->>Page: 400 with errors by field id
            Page-->>User: Inline errors, values kept, no ticket
        else Valid
            Service->>Service: Resolve approval rule, Ticket.Submit
            Note over Service: INCIDENT / SERVICE_REQUEST → SUBMITTED<br/>SERVICE_REQUEST with rule → PENDING_APPROVAL<br/>CHANGE → DRAFT
            Service->>Repo: AddAsync(ticket) in the unit of work
            activate Repo
            Repo->>DB: INSERT tickets, ticket_events, ticket_attachments,<br/>ticket_approvals, audit_logs, outbox_messages,<br/>idempotency_records
            activate DB
            DB-->>Repo: Commit
            deactivate DB
            Repo-->>Service: Ticket
            deactivate Repo
            Service-->>API: Ticket
            API-->>Page: 201 Ticket + Location
            Page-->>User: Request detail with ticket number
        end
        deactivate Service
        deactivate API
    end
    deactivate Filter
    deactivate Page
```

The tenant and requester come from the session. A body that carries `tenantId`, `requesterId`, or a role fails schema validation with `400` (test T16).

## 2. IT triages and resolves — `POST /v1/it/tickets/{ticketId}/triage`, `/resolve`

```mermaid
sequenceDiagram
    actor Staff as IT Staff
    participant Page as IT Ticket Detail Page
    participant API as ItTicketsController
    participant Service as TicketService
    participant Policy as TicketPolicy
    participant Repo as ITicketRepository
    participant DB as PostgreSQL

    Staff->>Page: Set category and priority, click Save
    activate Page
    Page->>API: POST /v1/it/tickets/{ticketId}/triage (expectedVersion 3)
    activate API
    API->>Service: TriageAsync(actor, command)
    activate Service
    Service->>Policy: EnsureItPermission(ticket.triage)
    Service->>Repo: GetForUpdateAsync(ticketId)
    activate Repo
    Repo->>DB: SELECT ticket (tenant filter)
    DB-->>Repo: Ticket or none
    Repo-->>Service: Ticket or null
    deactivate Repo

    alt Not found or another tenant
        Service-->>API: RESOURCE_NOT_FOUND
        API-->>Page: 404
    else Status does not allow triage
        Service-->>API: INVALID_TRANSITION
        API-->>Page: 409
    else Valid
        Service->>Service: ticket.Triage(category, priority)
        Service->>Repo: Save with row_version = 3
        activate Repo
        Repo->>DB: UPDATE tickets WHERE row_version = 3, INSERT ticket_events
        alt Another user saved first
            DB-->>Repo: 0 rows
            Repo-->>Service: Concurrency conflict
            Service-->>API: CONCURRENT_MODIFICATION
            API-->>Page: 409 — reload the ticket
        else Saved
            DB-->>Repo: Commit
            Repo-->>Service: TRIAGED, version 4
            Service-->>API: Ticket
            API-->>Page: 200 Ticket
        end
        deactivate Repo
    end
    deactivate Service
    deactivate API

    Staff->>Page: Assign, work, then Resolve with a note
    Page->>API: POST /v1/it/tickets/{ticketId}/resolve
    activate API
    API->>Service: ResolveAsync(actor, command)
    activate Service
    alt Resolution note is blank
        Service-->>API: VALIDATION_FAILED
        API-->>Page: 400, status unchanged
    else Note present and status allows it
        Service->>Repo: Save RESOLVED, resolved_at, outbox TicketResolved
        Repo->>DB: UPDATE tickets, INSERT ticket_events, outbox_messages
        Service-->>API: Ticket (reopenDeadlineAt = resolvedAt + 7 days)
        API-->>Page: 200 Ticket
    end
    deactivate Service
    deactivate API
    deactivate Page
```

## 3. Confirm, reopen, or auto-close — `POST /v1/tickets/{ticketId}/confirm`, `/reopen`

```mermaid
sequenceDiagram
    actor User as Employee (requester)
    participant Page as Request Detail Page
    participant API as TicketsController
    participant Service as TicketService
    participant Repo as ITicketRepository
    participant DB as PostgreSQL
    participant Job as AutoCloseResolvedTicketsJob

    alt Requester confirms
        User->>Page: Click Confirm
        Page->>API: POST /v1/tickets/{ticketId}/confirm
        API->>Service: ConfirmAsync(actor, ticketId, expectedVersion)
        Service->>Repo: GetForUpdateAsync, ticket.ConfirmResolution
        Repo->>DB: UPDATE status = CLOSED, INSERT ticket_events
        API-->>Page: 200 Ticket (CLOSED)
    else Requester reopens within 7 days (INCIDENT)
        User->>Page: Click Reopen and enter a reason
        Page->>API: POST /v1/tickets/{ticketId}/reopen
        API->>Service: ReopenAsync(actor, ticketId, expectedVersion, reason)
        alt Not the requester
            Service-->>API: RESOURCE_NOT_FOUND
            API-->>Page: 404
        else After the 7-day window
            Service-->>API: INVALID_TRANSITION
            API-->>Page: 409
        else Allowed
            Service->>Repo: ticket.Reopen(reason)
            Repo->>DB: UPDATE status = REOPENED, INSERT ticket_events (reason)
            API-->>Page: 200 Ticket (REOPENED)
        end
    else No action for 7 days
        Job->>DB: SELECT RESOLVED past deadline FOR UPDATE SKIP LOCKED
        Job->>Repo: ticket.AutoClose()
        Repo->>DB: UPDATE status = CLOSED, one CLOSED event
    end
```

The job re-checks the status under the row lock, so a retry or a second worker instance writes no second close event (test T13).

## 4. Ask the assistant — `POST /v1/ai/conversations/{conversationId}/messages`

```mermaid
sequenceDiagram
    actor User as Employee
    participant Page as AI Assistant Page
    participant API as AiConversationsController
    participant Service as AssistantService
    participant KB as IKnowledgeRetriever
    participant LLM as ILlmClient
    participant Tools as AssistantToolRegistry
    participant Repo as IAiConversationRepository
    participant DB as PostgreSQL

    User->>Page: "My VPN fails with error 809"
    activate Page
    Page->>API: POST /v1/ai/conversations/{conversationId}/messages
    activate API
    API->>Service: AskAsync(actor, conversationId, text)
    activate Service
    Service->>Repo: GetOwnedAsync(conversationId, membershipId)
    activate Repo
    Repo->>DB: SELECT ai_conversations (tenant and owner)
    DB-->>Repo: Conversation or none
    Repo-->>Service: Conversation or null
    deactivate Repo

    alt Not the owner
        Service-->>API: RESOURCE_NOT_FOUND
        API-->>Page: 404
    else Owner
        Service->>KB: SearchAsync(actor, embedding, topK 8)
        activate KB
        KB->>DB: kb_chunks JOIN PUBLISHED versions JOIN visible articles,<br/>WHERE tenant_id = caller ORDER BY distance
        DB-->>KB: Hits with scores
        KB-->>Service: Hits
        deactivate KB

        alt No source above the threshold
            Service->>Repo: Save user + assistant message (NO_SOURCE)
            Service-->>API: Reply NO_SOURCE, citations []
            API-->>Page: 200
            Page-->>User: No documented answer, catalog and draft buttons
        else Sources found
            Service->>LLM: CompleteAsync(question, sources S1..Sn, history)
            activate LLM
            opt Model calls a read-only tool (UC15, P1)
                LLM-->>Service: Tool call get_my_tickets
                Service->>Tools: ExecuteAsync(call, actor)
                Tools-->>Service: Caller's own tickets only
                Service->>LLM: CompleteAsync(with tool result)
            end
            alt Provider timeout or error
                LLM-->>Service: Failure
                Service-->>API: AI_UNAVAILABLE
                API-->>Page: 503 + Retry-After
                Page-->>User: Assistant unavailable, use the catalog
            else Answer
                LLM-->>Service: Text citing [S2]
                Service->>Service: CitationValidator drops unknown ids,<br/>none left → NO_SOURCE
                Service->>Repo: Save messages, reply kind, ai_message_sources
                Repo->>DB: INSERT ai_messages, ai_message_sources
                Service-->>API: Reply GROUNDED_ANSWER with citations
                API-->>Page: 200
                Page-->>User: Answer with source links
            end
            deactivate LLM
        end
    end
    deactivate Service
    deactivate API
    deactivate Page
```

## 5. Turn a chat into a ticket — `POST .../ticket-draft`, then `POST /v1/tickets`

```mermaid
sequenceDiagram
    actor User as Employee
    participant Page as AI Assistant Page
    participant API as AiConversationsController
    participant Service as AssistantService
    participant Catalog as IPublishedCatalogReader
    participant LLM as ILlmClient
    participant Tickets as TicketsController / TicketService
    participant DB as PostgreSQL

    User->>Page: "Still not working — create a ticket"
    activate Page
    Page->>API: POST /v1/ai/conversations/{conversationId}/ticket-draft
    activate API
    API->>Service: PrepareDraftAsync(actor, conversationId, requestTypeId)
    activate Service
    Service->>Catalog: GetUsableFormAsync(requestTypeId)
    Catalog-->>Service: Published form version
    Service->>LLM: Extract answers using only the form's field ids
    LLM-->>Service: Proposed answers
    Service->>Service: Validate, drop unknown fields, list missing required ones
    Service->>DB: INSERT ai_ticket_drafts (DRAFT)
    Service-->>API: TicketDraft (id, answers, missingRequiredFieldIds)
    deactivate Service
    API-->>Page: 200 TicketDraft
    deactivate API

    alt Employee discards
        User->>Page: Click Discard
        Page->>API: POST .../drafts/{draftId}/discard
        API-->>Page: 200 TicketDraft (DISCARDED), no ticket
    else Employee edits and confirms
        User->>Page: Edit fields, click Submit
        Note over Page,Tickets: The employee's own request — the assistant is not involved from here
        Page->>Tickets: POST /v1/tickets + Idempotency-Key + aiDraftId
        activate Tickets
        Tickets->>Tickets: Same validation as a manual submit, source = AI_ASSISTANT
        alt Draft is not the caller's
            Tickets-->>Page: 404
        else Draft already SUBMITTED or DISCARDED
            Tickets-->>Page: 409 INVALID_TRANSITION
        else Draft is DRAFT
            Tickets->>DB: INSERT ticket, UPDATE draft SUBMITTED + submitted_ticket_id (one transaction)
            Tickets-->>Page: 201 Ticket
        end
        deactivate Tickets
    end
    deactivate Page
```

Until the employee's `POST /tickets` succeeds, the database holds no new ticket (test T15).

## 6. Common error conventions

| Status | `errorCode` | Used in these flows when |
|---|---|---|
| 400 | `VALIDATION_FAILED` | Missing or invalid form fields, blank resolution note |
| 401 | `AUTHENTICATION_FAILED` | No valid tenant session |
| 403 | `ACCESS_DENIED` | The caller lacks the permission (for example an employee calling `/it/tickets/...`) |
| 404 | `RESOURCE_NOT_FOUND` | The ticket, conversation, or draft does not exist or is not visible to the caller |
| 409 | `INVALID_TRANSITION`, `CONCURRENT_MODIFICATION`, `IDEMPOTENCY_KEY_REUSED`, `CATALOG_VERSION_STALE` | Illegal status change, stale `expectedVersion`, reused key with a different body, outdated form |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many submissions or assistant questions |
| 503 | `AI_UNAVAILABLE` | The AI provider failed or exceeded the time budget |

All errors use `application/problem+json`. A resource that exists but belongs to another tenant or person returns the same `404` as an unknown id, so ids cannot be probed.
