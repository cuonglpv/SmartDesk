"""Single source of truth for the SmartDesk diagrams.

Every generated artefact (XMind file, mind map PNG, use case diagrams, Relume
sitemap) reads from this module so that the documents and images never drift.
"""

# ---------------------------------------------------------------------------
# 1. Mind maps (XMind sheets)
# ---------------------------------------------------------------------------

TOP_DOWN_ROOT = "SmartDesk\nAI-assisted IT Helpdesk SaaS"

TOP_DOWN = [
    ("Problem — Why", [
        "Requests get lost in chat, email and walk-ups",
        "Employees cannot pick the right request type",
        "Incidents repeat; how-to guides are scattered",
        "Device handover lacks approval and audit trail",
        "Managers cannot see backlog, SLA or workload",
    ]),
    ("Users — Who", [
        "Employee: asks, requests, tracks",
        "IT Staff: triages, fixes, fulfils",
        "IT Manager: approves, sets SLA, reports",
        "Org Admin: members, roles, service catalog",
        "Platform Admin: tenant lifecycle only",
        "AI provider: external, read-only scope",
    ]),
    ("Services — What", [
        "Incident: VPN, Wi-Fi, printer failures",
        "Service request: VPN access, laptop, software",
        "Change request: office ISP switch",
        "IT asset register and handover",
        "Knowledge base articles",
    ]),
    ("End-to-end flow — How", [
        "Self-service, then draft and submit a ticket",
        "Triage, assign, work, resolve",
        "Approve, fulfil, hand over the device",
        "Confirm or reopen, close, audit",
    ]),
    ("Market evidence", [
        "Jira Service Management: request types, queues, SLA, assets",
        "Freshservice Freddy AI: AI self-service with cited answers",
        "Gap: SME-sized setup, AI only at employee intake",
        "Not yet validated: willingness to pay, pricing",
    ]),
    ("AI Employee Assistant", [
        "Answer FAQs with cited internal sources",
        "Guide troubleshooting step by step",
        "Turn a conversation into a ticket draft",
        "Look up only my own tickets",
        "No source found: say so and offer a ticket",
    ]),
    ("Business rules", [
        "Tenant isolation on every query and file",
        "RBAC and ownership enforced by the API",
        "Separate state machines per ticket type",
        "AI never approves, provisions or writes",
        "Audit log, idempotent create, no double-assign",
    ]),
    ("Scope", [
        "Release 1 (MVP): incident, laptop request, KB, AI",
        "Release 2: approval rules, SLA, alerts, reports",
        "Phase 2: ISP change, maintenance log, tenants",
        "Out: network automation, monitoring, ERP, mobile app",
    ]),
    ("Success metrics", [
        "Self-service resolution rate",
        "Tickets complete on first submit",
        "Time to submit a ticket",
        "SLA compliance and reopen rate",
        "Citation precision and abstention rate",
    ]),
]

FEATURE_ROOT = "SmartDesk\nFeature map"

FEATURES = [
    ("Access & Identity", [
        "Sign in / sign out", "Edit my profile", "Organization settings",
        "Invite, lock, assign roles", "Activate / suspend tenant",
    ]),
    ("Employee Self-service", [
        "Browse service catalog", "Submit typed request form", "Track my tickets",
        "Comment and attach files", "Confirm or reopen", "View my assets",
    ]),
    ("AI Assistant", [
        "Cited FAQ answers", "Step-by-step troubleshooting",
        "Conversational ticket draft", "Ask my ticket status",
    ]),
    ("Ticket Management", [
        "Queue and filters", "Triage and priority", "Assign / pick up",
        "Status and internal notes", "Transfer / escalate", "Resolve and close",
        "Link asset or ticket",
    ]),
    ("Catalog & Approval", [
        "Request types and forms", "Approval rules", "Approve / reject with reason",
        "Fulfilment tasks", "ISP change review",
    ]),
    ("IT Assets", [
        "Register and update", "Assign and hand over", "Recover device",
        "Maintenance log", "Inventory and history",
    ]),
    ("Knowledge Base", [
        "Draft articles", "Review, publish, retire", "Search and read",
    ]),
    ("SLA & Reporting", [
        "SLA policies", "Breach alerts", "Reports and export",
    ]),
]

# ---------------------------------------------------------------------------
# 2. Use cases
# ---------------------------------------------------------------------------

# id: (name, package, priority, primary actors)
USE_CASES = {
    "UC01": ("Sign in and sign out", "Identity & Tenant", "P0", ["User"]),
    "UC02": ("View and edit my profile", "Identity & Tenant", "P1", ["User"]),
    "UC03": ("Update organization settings", "Identity & Tenant", "P1", ["Org Admin"]),
    "UC04": ("Invite, lock and assign member roles", "Identity & Tenant", "P0", ["Org Admin"]),
    "UC05": ("Activate or suspend a tenant", "Identity & Tenant", "P2", ["Platform Admin"]),
    "UC06": ("Browse the IT service catalog", "Employee Self-service", "P0", ["Employee"]),
    "UC07": ("Submit a request through a typed form", "Employee Self-service", "P0", ["Employee"]),
    "UC08": ("Find and track my tickets", "Employee Self-service", "P0", ["Employee"]),
    "UC09": ("Add comments and files to my ticket", "Employee Self-service", "P0", ["Employee"]),
    "UC10": ("Confirm resolution or reopen a ticket", "Employee Self-service", "P0", ["Employee"]),
    "UC11": ("View assets assigned to me", "Employee Self-service", "P1", ["Employee"]),
    "UC12": ("Ask FAQs answered from internal sources", "AI Assistant", "P0", ["Employee"]),
    "UC13": ("Get step-by-step troubleshooting", "AI Assistant", "P1", ["Employee"]),
    "UC14": ("Draft a ticket through conversation", "AI Assistant", "P0", ["Employee"]),
    "UC15": ("Ask my ticket status in natural language", "AI Assistant", "P1", ["Employee"]),
    "UC16": ("View and filter the ticket queue", "Ticket Management", "P0", ["IT Staff"]),
    "UC17": ("Triage and set ticket priority", "Ticket Management", "P0", ["IT Staff"]),
    "UC18": ("Assign or pick up a ticket", "Ticket Management", "P0", ["IT Staff", "IT Manager"]),
    "UC19": ("Update status and technical notes", "Ticket Management", "P0", ["IT Staff"]),
    "UC20": ("Transfer or escalate a ticket", "Ticket Management", "P1", ["IT Staff", "IT Manager"]),
    "UC21": ("Resolve and close a ticket", "Ticket Management", "P0", ["IT Staff"]),
    "UC22": ("Link a ticket to an asset or ticket", "Ticket Management", "P1", ["IT Staff"]),
    "UC23": ("Manage request types and forms", "Catalog & Approval", "P0", ["Org Admin"]),
    "UC24": ("Configure approval rules", "Catalog & Approval", "P1", ["IT Manager"]),
    "UC25": ("Approve or reject a request with reason", "Catalog & Approval", "P0", ["IT Manager"]),
    "UC26": ("Perform and record fulfilment work", "Catalog & Approval", "P1", ["IT Staff"]),
    "UC27": ("Assess and manage an ISP change", "Catalog & Approval", "P2", ["IT Manager"]),
    "UC28": ("Register and update IT assets", "IT Assets", "P0", ["IT Staff"]),
    "UC29": ("Assign and hand over a device", "IT Assets", "P0", ["IT Staff"]),
    "UC30": ("Recover a device from an employee", "IT Assets", "P1", ["IT Staff"]),
    "UC31": ("Log asset maintenance and repair", "IT Assets", "P2", ["IT Staff"]),
    "UC32": ("View inventory and asset history", "IT Assets", "P1", ["IT Manager"]),
    "UC33": ("Create and edit KB article drafts", "Knowledge Base", "P0", ["IT Staff"]),
    "UC34": ("Review, publish and retire KB articles", "Knowledge Base", "P0", ["IT Manager"]),
    "UC35": ("Search and read KB articles without AI", "Knowledge Base", "P0", ["Employee"]),
    "UC36": ("Configure SLA by type and priority", "SLA & Reporting", "P1", ["IT Manager"]),
    "UC37": ("Receive near-breach and breach alerts", "SLA & Reporting", "P1", ["IT Manager"]),
    "UC38": ("View and export operations reports", "SLA & Reporting", "P1", ["IT Manager"]),
}

AI_SUPPORTED = ["UC12", "UC13", "UC14", "UC15"]

# Three diagrams keep every view readable; together they cover all 38 use cases.
UC_DIAGRAMS = [
    {
        "file": "uc-1-employee",
        "title": "SmartDesk — Use cases: Employee & AI Assistant",
        "left": ["User", "Employee"],
        "right": ["AI Provider"],
        "packages": [
            ("Identity", ["UC01", "UC02"]),
            ("Employee Self-service", ["UC06", "UC07", "UC08", "UC09", "UC10", "UC11"]),
            ("Knowledge Base", ["UC35"]),
            ("AI Assistant", ["UC12", "UC13", "UC14", "UC15"]),
        ],
        "links": {"User": ["UC01", "UC02"],
                  "Employee": ["UC06", "UC07", "UC08", "UC09", "UC10", "UC11",
                               "UC35", "UC12", "UC13", "UC14", "UC15"],
                  "AI Provider": AI_SUPPORTED},
        "generalization": [("Employee", "User")],
        "extends": [("UC13", "UC12"), ("UC14", "UC13")],
    },
    {
        "file": "uc-2-it-staff",
        "title": "SmartDesk — Use cases: IT Staff",
        "left": ["IT Staff"],
        "right": [],
        "packages": [
            ("Ticket Management", ["UC16", "UC17", "UC18", "UC19", "UC20", "UC21", "UC22"]),
            ("Fulfilment", ["UC26"]),
            ("IT Assets", ["UC28", "UC29", "UC30", "UC31"]),
            ("Knowledge Base", ["UC33"]),
        ],
        "links": {"IT Staff": ["UC16", "UC17", "UC18", "UC19", "UC20", "UC21", "UC22",
                               "UC26", "UC28", "UC29", "UC30", "UC31", "UC33"]},
        "generalization": [],
        "extends": [],
    },
    {
        "file": "uc-3-management",
        "title": "SmartDesk — Use cases: IT Manager, Org Admin, Platform Admin",
        "left": ["IT Manager"],
        "right": ["Org Admin", "Platform Admin"],
        "packages": [
            ("Tickets & Approval", ["UC18", "UC20", "UC24", "UC25", "UC27"]),
            ("Assets & Knowledge", ["UC32", "UC34"]),
            ("SLA & Reporting", ["UC36", "UC37", "UC38"]),
            ("Tenant Administration", ["UC03", "UC04", "UC23", "UC05"]),
        ],
        "links": {"IT Manager": ["UC18", "UC20", "UC24", "UC25", "UC27", "UC32", "UC34",
                                 "UC36", "UC37", "UC38"],
                  "Org Admin": ["UC03", "UC04", "UC23"],
                  "Platform Admin": ["UC05"]},
        "generalization": [],
        "extends": [],
    },
]

# ---------------------------------------------------------------------------
# 3. Relume-style sitemap: page -> sections (name, what the section does)
# ---------------------------------------------------------------------------

SITEMAP_GROUPS = [
    ("Shared", "#64748b"),
    ("Employee Portal", "#2563eb"),
    ("IT Workspace", "#0d9488"),
    ("Manager Console", "#d97706"),
    ("Admin", "#7c3aed"),
]

SCREENS = [
    # ---- Shared ----------------------------------------------------------
    {"id": "SCR-01", "name": "Sign In", "group": "Shared", "route": "/login",
     "roles": "All", "ucs": ["UC01"], "sections": [
        ("Sign-in form", "Work email, password, show/hide password, submit"),
        ("Account status message", "Locked user, suspended tenant or wrong credentials, no detail leak"),
        ("Workspace picker", "Choose a tenant when the email belongs to several organizations"),
        ("Help link", "Forgot password and contact IT instructions"),
    ]},
    {"id": "SCR-02", "name": "My Profile", "group": "Shared", "route": "/profile",
     "roles": "All", "ucs": ["UC02", "UC01"], "sections": [
        ("Profile details", "Edit name, phone, department, location, avatar"),
        ("Role & permissions", "Read-only role and tenant, cannot self-promote"),
        ("Notification preferences", "Email or in-app for ticket updates and approvals"),
        ("Session", "Sign out of this device"),
    ]},
    {"id": "SCR-03", "name": "Notification Center", "group": "Shared", "route": "/notifications",
     "roles": "All", "ucs": ["UC37", "UC10", "UC25"], "sections": [
        ("Notification list", "Ticket updates, approvals, SLA warnings, newest first"),
        ("Filters", "Unread, type, date"),
        ("Deep link", "Open the related ticket, approval or asset"),
        ("Mark as read", "Single item or all"),
    ]},
    {"id": "SCR-04", "name": "Error Pages", "group": "Shared", "route": "/403, /404",
     "roles": "All", "ucs": [], "sections": [
        ("Error message", "Same 404 for missing and other-tenant records"),
        ("Safe way back", "Button to the role's home page"),
    ]},

    # ---- Employee Portal ---------------------------------------------------
    {"id": "SCR-10", "name": "Employee Home", "group": "Employee Portal", "route": "/app",
     "roles": "Employee", "ucs": ["UC06", "UC08", "UC12", "UC35"], "sections": [
        ("Ask SmartDesk bar", "Type a question and open the AI Assistant"),
        ("Quick actions", "VPN not working, Request a laptop, Other request"),
        ("My open tickets", "3-5 latest tickets with status and next step"),
        ("Popular guides", "Most-read KB articles"),
        ("Pending my action", "Tickets waiting for my reply or confirmation"),
    ]},
    {"id": "SCR-11", "name": "AI Assistant", "group": "Employee Portal", "route": "/app/assistant",
     "roles": "Employee", "ucs": ["UC12", "UC13", "UC14", "UC15"], "sections": [
        ("Conversation", "Chat history, suggested prompts, message composer"),
        ("Cited answer", "Steps with links to the published KB source"),
        ("No-source fallback", "Says it has no source; offers catalog or ticket"),
        ("Guided questions", "Asks only the missing required fields"),
        ("Ticket draft panel", "Type, title, summary, fields; edit, confirm or discard"),
        ("My ticket status", "Answers about my own tickets only"),
    ]},
    {"id": "SCR-12", "name": "Knowledge Base", "group": "Employee Portal", "route": "/app/kb",
     "roles": "Employee", "ucs": ["UC35"], "sections": [
        ("Search", "Keyword search across published articles"),
        ("Topic filter", "Network, Accounts, Devices, Software, Printing"),
        ("Results list", "Title, summary, last updated"),
        ("Featured articles", "Pinned guides for common issues"),
    ]},
    {"id": "SCR-13", "name": "KB Article", "group": "Employee Portal", "route": "/app/kb/:id",
     "roles": "Employee", "ucs": ["UC35"], "sections": [
        ("Article header", "Title, topic, last reviewed date"),
        ("Step-by-step content", "Numbered steps with screenshots"),
        ("Was this helpful?", "Yes / No feedback"),
        ("Still need help", "Open a request with this article linked"),
        ("Related articles", "Same topic suggestions"),
    ]},
    {"id": "SCR-14", "name": "Service Catalog", "group": "Employee Portal", "route": "/app/catalog",
     "roles": "Employee", "ucs": ["UC06"], "sections": [
        ("Catalog search", "Find a service by name or keyword"),
        ("Category tabs", "Report a problem, Request something, Propose a change"),
        ("Service cards", "Name, description, needs approval, expected time"),
        ("Not sure?", "Shortcut to the AI Assistant"),
    ]},
    {"id": "SCR-15", "name": "New Request", "group": "Employee Portal", "route": "/app/requests/new/:type",
     "roles": "Employee", "ucs": ["UC07", "UC14"], "sections": [
        ("Service summary", "Request type, approval needed, SLA target"),
        ("Dynamic form", "Fields defined by the request type, with inline validation"),
        ("Attachments", "Screenshots or files, type and size checked"),
        ("What happens next", "Approval and fulfilment steps"),
        ("Review & submit", "Preview, submit once, show ticket ID"),
    ]},
    {"id": "SCR-16", "name": "My Requests", "group": "Employee Portal", "route": "/app/requests",
     "roles": "Employee", "ucs": ["UC08"], "sections": [
        ("Search", "By ticket ID or title"),
        ("Filters", "Status, type, date range"),
        ("Ticket table", "ID, title, type, status, assignee, updated"),
        ("Empty state", "No tickets yet, with New request button"),
    ]},
    {"id": "SCR-17", "name": "Request Detail", "group": "Employee Portal", "route": "/app/requests/:id",
     "roles": "Employee", "ucs": ["UC08", "UC09", "UC10"], "sections": [
        ("Ticket header", "ID, type, status, priority, SLA target"),
        ("Progress tracker", "Submitted, approval, in progress, resolved"),
        ("Public conversation", "Comments and attachments, no internal notes"),
        ("Assignee & approval", "Who is working on it, approval decision and reason"),
        ("Resolution actions", "Confirm resolved or reopen with reason (7 days)"),
    ]},
    {"id": "SCR-18", "name": "My Assets", "group": "Employee Portal", "route": "/app/assets",
     "roles": "Employee", "ucs": ["UC11"], "sections": [
        ("Assigned devices", "Model, asset tag, serial number"),
        ("Handover record", "Date, handed over by, condition"),
        ("Report a problem", "Opens an incident linked to this device"),
    ]},

    # ---- IT Workspace ------------------------------------------------------
    {"id": "SCR-20", "name": "Agent Dashboard", "group": "IT Workspace", "route": "/it",
     "roles": "IT Staff, IT Manager", "ucs": ["UC16"], "sections": [
        ("Workload counters", "Unassigned, assigned to me, near breach, waiting"),
        ("My priority list", "My tickets ordered by SLA due time"),
        ("Fulfilment tasks", "Approved requests ready to fulfil"),
        ("Quick links", "Queue, inventory, KB editor"),
    ]},
    {"id": "SCR-21", "name": "Ticket Queue", "group": "IT Workspace", "route": "/it/tickets",
     "roles": "IT Staff, IT Manager", "ucs": ["UC16", "UC17", "UC18"], "sections": [
        ("Queue views", "Unassigned, My tickets, Team, All permitted"),
        ("Filters", "Type, status, priority, SLA, requester, team"),
        ("Ticket table", "ID, title, requester, priority, assignee, age, due"),
        ("Inline actions", "Pick up, assign, set priority"),
        ("Empty / loading", "Clear filters, skeleton rows, retry"),
    ]},
    {"id": "SCR-22", "name": "Ticket Detail", "group": "IT Workspace", "route": "/it/tickets/:id",
     "roles": "IT Staff, IT Manager", "ucs": ["UC17", "UC18", "UC19", "UC20", "UC21", "UC22"], "sections": [
        ("Header & SLA", "ID, type, status, priority, SLA countdown"),
        ("Request context", "Description, form fields, attachments, AI chat summary"),
        ("Reply & notes", "Public reply or internal note toggle"),
        ("Ticket actions", "Triage, assign, change status, transfer or escalate"),
        ("Resolve", "Resolution note required before Resolved"),
        ("Links", "Linked asset, related tickets, KB article"),
        ("Audit timeline", "Every change with actor and time"),
    ]},
    {"id": "SCR-23", "name": "Fulfilment Task", "group": "IT Workspace", "route": "/it/fulfilment/:id",
     "roles": "IT Staff", "ucs": ["UC26", "UC29"], "sections": [
        ("Approval status", "Locked until the request is Approved"),
        ("Checklist", "Steps defined by the request type"),
        ("Asset picker", "Only AVAILABLE assets matching the request"),
        ("Handover", "Assign device and record handover"),
        ("Complete", "Mark fulfilled and notify the requester"),
    ]},
    {"id": "SCR-24", "name": "Asset Inventory", "group": "IT Workspace", "route": "/it/assets",
     "roles": "IT Staff, IT Manager (read)", "ucs": ["UC28", "UC32"], "sections": [
        ("Stock summary", "Available, assigned, maintenance, retired"),
        ("Search & filters", "Type, status, location, holder"),
        ("Asset table", "Tag, model, status, holder, location"),
        ("Add asset", "Register with a tag unique per tenant"),
    ]},
    {"id": "SCR-25", "name": "Asset Detail", "group": "IT Workspace", "route": "/it/assets/:id",
     "roles": "IT Staff, IT Manager (read)", "ucs": ["UC28", "UC29", "UC30", "UC31", "UC32"], "sections": [
        ("Asset profile", "Model, serial, purchase date, warranty, location"),
        ("Lifecycle status", "Available, reserved, assigned, maintenance, retired"),
        ("Assign / recover", "Hand over to or take back from an employee"),
        ("Maintenance log", "Date, work done, technician, before/after status"),
        ("History", "Past holders and linked tickets"),
    ]},
    {"id": "SCR-26", "name": "KB Editor", "group": "IT Workspace", "route": "/it/kb",
     "roles": "IT Staff", "ucs": ["UC33"], "sections": [
        ("My drafts", "Draft, in review, published, retired"),
        ("Editor", "Title, topic, rich-text steps, images"),
        ("Visibility", "Which roles or departments can read it"),
        ("Submit for review", "Send the draft to an IT Manager"),
    ]},

    # ---- Manager Console ---------------------------------------------------
    {"id": "SCR-30", "name": "Approval Inbox", "group": "Manager Console", "route": "/manage/approvals",
     "roles": "IT Manager", "ucs": ["UC25"], "sections": [
        ("Pending list", "Requests waiting for my decision"),
        ("Filters", "Type, department, request date"),
        ("Request summary", "Requester, reason, needed-by date, stock available"),
        ("Decision", "Approve, or reject with a required reason"),
        ("Decision history", "Past decisions with approver and time"),
    ]},
    {"id": "SCR-31", "name": "Change Review", "group": "Manager Console", "route": "/manage/changes/:id",
     "roles": "IT Manager", "ucs": ["UC27"], "sections": [
        ("Change summary", "Site, current ISP, reason, proposed window"),
        ("Impact & rollback", "Affected users, downtime, rollback plan"),
        ("Approval", "Approve, reject or request more information"),
        ("Schedule & result", "Maintenance window and implementation outcome"),
    ]},
    {"id": "SCR-32", "name": "KB Review", "group": "Manager Console", "route": "/manage/kb",
     "roles": "IT Manager", "ucs": ["UC34"], "sections": [
        ("Review queue", "Drafts submitted for review"),
        ("Diff & preview", "Changes since the last version"),
        ("Publish / retire", "Publish to employees and the AI index, or retire"),
    ]},
    {"id": "SCR-33", "name": "SLA & Reports", "group": "Manager Console", "route": "/manage/reports",
     "roles": "IT Manager", "ucs": ["UC37", "UC38"], "sections": [
        ("Filters", "Date range, team, type, priority"),
        ("KPI cards", "Volume, SLA compliance, reopen rate, self-service rate"),
        ("Breach watch", "Near-breach and breached tickets"),
        ("Charts", "Volume trend, ageing, by category"),
        ("Export", "CSV or PDF using the same filters"),
    ]},
    {"id": "SCR-34", "name": "SLA Policies", "group": "Manager Console", "route": "/manage/sla",
     "roles": "IT Manager", "ucs": ["UC36"], "sections": [
        ("Business calendar", "Working hours, holidays, timezone"),
        ("Targets matrix", "Response and resolve time by type and priority"),
        ("Alert thresholds", "Warn at 80%, breach at 100%"),
        ("Pause rules", "Pause while waiting for the employee"),
    ]},
    {"id": "SCR-35", "name": "Approval Rules", "group": "Manager Console", "route": "/manage/approval-rules",
     "roles": "IT Manager", "ucs": ["UC24"], "sections": [
        ("Rule list", "Which request types need approval"),
        ("Approver", "Approver role or named person"),
        ("Conditions", "Department, cost, asset type"),
        ("Effective date", "New rules never change past decisions"),
    ]},

    # ---- Admin -------------------------------------------------------------
    {"id": "SCR-40", "name": "Organization Settings", "group": "Admin", "route": "/admin/org",
     "roles": "Org Admin", "ucs": ["UC03"], "sections": [
        ("Company profile", "Name, logo, default language"),
        ("Locations & departments", "Offices and departments for routing"),
        ("Regional settings", "Timezone, date format"),
    ]},
    {"id": "SCR-41", "name": "Members & Roles", "group": "Admin", "route": "/admin/members",
     "roles": "Org Admin", "ucs": ["UC04"], "sections": [
        ("Member table", "Name, email, role, status"),
        ("Invite", "Send invitation by email with a role"),
        ("Role assignment", "Employee, IT Staff, IT Manager, Org Admin"),
        ("Lock / unlock", "Block sign-in without deleting history"),
    ]},
    {"id": "SCR-42", "name": "Catalog Builder", "group": "Admin", "route": "/admin/catalog",
     "roles": "Org Admin", "ucs": ["UC23"], "sections": [
        ("Request types", "Create, reorder, publish or hide"),
        ("Form fields", "Field type, required, help text, validation"),
        ("Routing", "Ticket type, team, approval required"),
        ("Preview & publish", "Test as an employee, publish a version"),
    ]},
    {"id": "SCR-50", "name": "Tenants", "group": "Admin", "route": "/platform/tenants",
     "roles": "Platform Admin", "ucs": ["UC05"], "sections": [
        ("Tenant list", "Name, plan, status, created"),
        ("Activate / suspend", "Suspended tenants cannot create data"),
        ("Tenant metadata", "Contacts and limits; no ticket content by default"),
    ]},
]

# Parent page for each screen in the Relume tree (None = directly under group).
SITEMAP_PARENT = {
    "SCR-11": "SCR-10", "SCR-13": "SCR-12", "SCR-15": "SCR-14", "SCR-17": "SCR-16",
    "SCR-22": "SCR-21", "SCR-25": "SCR-24", "SCR-31": "SCR-30",
}
