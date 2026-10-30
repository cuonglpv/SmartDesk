# SmartDesk — API ↔ Use Case Traceability

> **Design only.** Automatically derived from `x-use-cases`/`x-release` in [`openapi.yaml`](openapi.yaml) (0.3.0-draft).

Source: [SmartDesk use cases](https://github.com/cuonglpv/SmartDesk/blob/main/docs/02-use-cases.md) · [Acceptance criteria](https://github.com/cuonglpv/SmartDesk/blob/main/docs/06-acceptance-criteria.md).

Coverage: **43/43 UC**, 105 operations. Operations by earliest release: P0: 53, P1: 45, P2: 7.

| Use case | Target API operations |
|---|---|
| `UC01` | `POST /auth/sign-in` (`signIn`, P0)<br>`POST /auth/select-tenant` (`selectTenant`, P0)<br>`POST /auth/refresh` (`refreshSession`, P0)<br>`POST /auth/sign-out` (`signOut`, P0)<br>`POST /platform/auth/sign-in` (`platformSignIn`, P1)<br>`POST /platform/auth/refresh` (`platformRefreshSession`, P1)<br>`POST /platform/auth/sign-out` (`platformSignOut`, P1) |
| `UC02` | `GET /me` (`getMyProfile`, P1)<br>`PATCH /me` (`updateMyProfile`, P1) |
| `UC03` | `GET /organization` (`getOrganization`, P1)<br>`PATCH /organization` (`updateOrganization`, P1)<br>`GET /organization/departments` (`listOrgDepartments`, P1)<br>`POST /organization/departments` (`createOrgDepartment`, P1)<br>`PATCH /organization/departments/{departmentId}` (`updateOrgDepartment`, P1)<br>`GET /organization/locations` (`listOrgLocations`, P1)<br>`POST /organization/locations` (`createOrgLocation`, P1)<br>`PATCH /organization/locations/{locationId}` (`updateOrgLocation`, P1)<br>`GET /organization/teams` (`listOrgTeams`, P1)<br>`POST /organization/teams` (`createOrgTeam`, P1)<br>`PATCH /organization/teams/{teamId}` (`updateOrgTeam`, P1) |
| `UC04` | `GET /organization/members` (`listMembers`, P0)<br>`POST /organization/members/invitations` (`inviteMember`, P0)<br>`POST /invitations/accept` (`acceptInvitation`, P0)<br>`PATCH /organization/members/{memberId}` (`changeMember`, P0) |
| `UC05` | `POST /platform/tenants` (`createTenant`, P1) |
| `UC06` | `GET /catalog/request-types` (`browseCatalog`, P0)<br>`GET /catalog/request-types/{requestTypeId}` (`getPublishedRequestType`, P0) |
| `UC07` | `POST /uploads` (`uploadTemporaryFile`, P0)<br>`POST /tickets` (`createTicket`, P0)<br>`POST /tickets/{ticketId}/cancel` (`cancelTicket`, P1) |
| `UC08` | `GET /tickets/my` (`listMyTickets`, P0)<br>`GET /tickets/{ticketId}` (`getTicket`, P0)<br>`GET /tickets/{ticketId}/timeline` (`listTicketTimeline`, P0) |
| `UC09` | `POST /uploads` (`uploadTemporaryFile`, P0)<br>`GET /tickets/{ticketId}/timeline` (`listTicketTimeline`, P0)<br>`POST /tickets/{ticketId}/comments` (`addTicketComment`, P0)<br>`GET /tickets/{ticketId}/attachments` (`listTicketAttachments`, P0)<br>`GET /tickets/{ticketId}/attachments/{attachmentId}/content` (`downloadTicketAttachment`, P0) |
| `UC10` | `POST /tickets/{ticketId}/confirm` (`confirmResolution`, P0)<br>`POST /tickets/{ticketId}/reopen` (`reopenTicket`, P0) |
| `UC11` | `GET /assets/my` (`listMyAssets`, P1) |
| `UC12` | `POST /ai/conversations` (`createAIConversation`, P0)<br>`POST /ai/conversations/{conversationId}/messages` (`askAI`, P0) |
| `UC13` | `POST /ai/conversations/{conversationId}/messages` (`askAI`, P0) |
| `UC14` | `POST /tickets` (`createTicket`, P0)<br>`POST /ai/conversations/{conversationId}/ticket-draft` (`prepareAITicketDraft`, P0)<br>`POST /ai/conversations/{conversationId}/drafts/{draftId}/discard` (`discardAITicketDraft`, P0) |
| `UC15` | `POST /ai/conversations/{conversationId}/messages` (`askAI`, P0) |
| `UC16` | `GET /tickets/{ticketId}` (`getTicket`, P0)<br>`GET /it/dashboard` (`getITDashboard`, P0)<br>`GET /it/tickets` (`listTicketQueue`, P0) |
| `UC17` | `POST /it/tickets/{ticketId}/triage` (`triageTicket`, P0) |
| `UC18` | `POST /it/tickets/{ticketId}/assign` (`assignTicket`, P0) |
| `UC19` | `GET /tickets/{ticketId}/timeline` (`listTicketTimeline`, P0)<br>`POST /tickets/{ticketId}/comments` (`addTicketComment`, P0)<br>`POST /it/tickets/{ticketId}/status` (`updateTicketStatus`, P0) |
| `UC20` | `POST /it/tickets/{ticketId}/transfer` (`transferTicket`, P1) |
| `UC21` | `POST /tickets/{ticketId}/cancel` (`cancelTicket`, P1)<br>`POST /it/tickets/{ticketId}/resolve` (`resolveTicket`, P0) |
| `UC22` | `POST /it/tickets/{ticketId}/links` (`linkTicketRecord`, P1)<br>`GET /it/tickets/{ticketId}/links` (`getTicketLinks`, P1)<br>`GET /assets/{assetId}/links` (`getAssetLinks`, P1) |
| `UC23` | `GET /organization/teams` (`listOrgTeams`, P1)<br>`POST /organization/teams` (`createOrgTeam`, P1)<br>`PATCH /organization/teams/{teamId}` (`updateOrgTeam`, P1)<br>`GET /admin/request-types` (`listAdminRequestTypes`, P0)<br>`POST /admin/request-types` (`createRequestType`, P0)<br>`PATCH /admin/request-types/{requestTypeId}` (`editRequestType`, P0)<br>`POST /admin/request-types/{requestTypeId}/publish` (`publishRequestType`, P0)<br>`POST /admin/request-types/{requestTypeId}/hide` (`hideRequestType`, P0) |
| `UC24` | `GET /approval-rules` (`listApprovalRules`, P1)<br>`POST /approval-rules` (`createApprovalRule`, P1)<br>`PATCH /approval-rules/{approvalRuleId}` (`updateApprovalRule`, P1) |
| `UC25` | `GET /approvals/inbox` (`getApprovalInbox`, P0)<br>`POST /approvals/{approvalId}/decision` (`decideApproval`, P0) |
| `UC26` | `GET /it/tickets/{ticketId}/fulfilment-steps` (`listFulfilmentSteps`, P1)<br>`POST /it/tickets/{ticketId}/fulfilment-steps` (`recordFulfilmentStep`, P1) |
| `UC27` | `POST /it/tickets/{ticketId}/change-assessment` (`recordChangeAssessment`, P2)<br>`POST /it/tickets/{ticketId}/change-result` (`recordChangeResult`, P2)<br>`POST /it/tickets/{ticketId}/change-schedule` (`scheduleChange`, P2)<br>`POST /it/tickets/{ticketId}/change-close` (`closeCompletedChange`, P2) |
| `UC28` | `POST /assets` (`createAsset`, P0)<br>`PATCH /assets/{assetId}` (`updateAsset`, P0)<br>`POST /assets/{assetId}/transition` (`transitionAssetStatus`, P1) |
| `UC29` | `POST /assets/{assetId}/handover` (`handOverAsset`, P0) |
| `UC30` | `POST /assets/{assetId}/recover` (`recoverAsset`, P1)<br>`POST /assets/{assetId}/transition` (`transitionAssetStatus`, P1) |
| `UC31` | `POST /assets/{assetId}/maintenance` (`recordAssetMaintenance`, P2) |
| `UC32` | `GET /assets/summary` (`getAssetStockSummary`, P1)<br>`GET /assets` (`listAssets`, P1)<br>`GET /assets/{assetId}` (`getAsset`, P1)<br>`GET /assets/{assetId}/links` (`getAssetLinks`, P1)<br>`GET /assets/{assetId}/history` (`listAssetHistory`, P1) |
| `UC33` | `GET /it/kb/articles` (`listDraftArticles`, P0)<br>`POST /it/kb/articles` (`createArticleDraft`, P0)<br>`PATCH /it/kb/articles/{articleId}` (`editArticleDraft`, P0)<br>`POST /it/kb/articles/{articleId}/submit-review` (`submitArticleForReview`, P0) |
| `UC34` | `GET /manager/kb/articles` (`listArticlesForReview`, P0)<br>`GET /manager/kb/articles/{articleId}` (`getArticleForReview`, P0)<br>`POST /manager/kb/articles/{articleId}/publish` (`publishArticle`, P0)<br>`POST /manager/kb/articles/{articleId}/return` (`returnArticle`, P0)<br>`POST /manager/kb/articles/{articleId}/retire` (`retireArticle`, P0) |
| `UC35` | `GET /kb/articles` (`searchPublishedArticles`, P0)<br>`GET /kb/articles/{articleId}` (`getPublishedArticle`, P0)<br>`POST /kb/articles/{articleId}/feedback` (`rateArticle`, P0) |
| `UC36` | `GET /sla/policies` (`listSlaPolicies`, P1)<br>`POST /sla/policies` (`createSlaPolicy`, P1)<br>`PATCH /sla/policies/{slaPolicyId}` (`editSlaPolicy`, P1) |
| `UC37` | `GET /sla/alerts` (`listSlaAlerts`, P1) |
| `UC38` | `GET /reports/operations` (`getOperationsReport`, P1)<br>`GET /reports/operations/export` (`exportOperationsReport`, P1) |
| `UC39` | `POST /me/password` (`changeMyPassword`, P0) |
| `UC40` | `GET /me/notifications` (`listMyNotifications`, P1)<br>`POST /me/notifications/{notificationId}/read` (`markNotificationRead`, P1) |
| `UC41` | `POST /platform/tenants/{tenantId}/suspend` (`suspendTenant`, P2)<br>`POST /platform/tenants/{tenantId}/reopen` (`reopenTenant`, P2) |
| `UC42` | `GET /platform/tenants` (`listTenants`, P1)<br>`GET /platform/tenants/{tenantId}` (`getTenant`, P1) |
| `UC43` | `GET /platform/audit-logs` (`listPlatformAudits`, P1) |

## How to use the table

- Use the UC/AC documents to verify allowed actors, preconditions, negative cases, and state transitions. A mapped operation is not proof of full acceptance-criteria coverage.
- A multi-UC operation may be introduced in P0 but support a later-use-case feature only behind a release flag.
- Every operation is proposed (`x-implementation-status: PROPOSED`), not evidence that any HTTP handler exists.

## Review gates

1. For every `UCxx`, test at least one happy path, authorization failure, tenant-crossing attempt and relevant business-state rejection.
2. Check request/response examples against the exact schema, and ensure error media type is `application/problem+json`.
3. Ensure resource-level ownership is checked even when `x-roles` allows the acting role.
4. Confirm suspended-tenant and SERVICE_REQUEST reopen decisions with product owner before production implementation.
