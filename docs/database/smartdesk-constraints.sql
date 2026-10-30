-- SmartDesk — physical constraints that DBML cannot express.
-- Run after the DDL exported from smartdesk.dbml (dbml2sql --postgres).

CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE EXTENSION IF NOT EXISTS vector;

-- One live version per catalog item / KB article
CREATE UNIQUE INDEX ux_catalog_versions_one_published ON catalog_versions (catalog_item_id) WHERE status = 'PUBLISHED';
CREATE UNIQUE INDEX ux_kb_versions_one_published ON kb_article_versions (article_id) WHERE status = 'PUBLISHED';

-- Location names are unique per tenant, ignoring case (tenant_id first, so per-tenant lookups use it)
CREATE UNIQUE INDEX ux_locations_name_ci ON locations (tenant_id, lower(name));

-- A device has at most one open custody record
CREATE UNIQUE INDEX ux_asset_open_assignment ON asset_assignments (asset_id) WHERE returned_at IS NULL;

-- SLA policies for the same (tenant, request type, priority) never overlap in time
ALTER TABLE sla_policies ADD CONSTRAINT ex_sla_policies_no_overlap EXCLUDE USING gist (
  tenant_id WITH =,
  coalesce(catalog_item_id, '00000000-0000-0000-0000-000000000000'::uuid) WITH =,
  priority WITH =,
  tstzrange(effective_from, effective_to) WITH &&
);

-- Vector search over published KB content
CREATE INDEX ix_kb_chunks_embedding ON kb_chunks USING hnsw (embedding vector_cosine_ops);

-- Worker queue: only pending outbox rows are scanned
CREATE INDEX ix_outbox_pending ON outbox_messages (available_at) WHERE processed_at IS NULL;

-- Still to implement as triggers (see table Notes in smartdesk.dbml):
--   * updated_at maintenance on every table that has it
--   * immutability of non-DRAFT catalog_versions and kb_article_versions, and of catalog_items.kind
--   * append-only approval_rules / sla_policies (only effective_to may change)
--   * assets.status = 'ASSIGNED' <=> an open asset_assignments row exists
--   * REVOKE UPDATE, DELETE ON ticket_events, audit_logs FROM <app_role>
--   * REVOKE UPDATE ON idempotency_records FROM <app_role> (insert once; only the worker purges expired rows)
