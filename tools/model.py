"""Single source of truth for the SmartDesk diagrams.

Every generated artefact (XMind file, mind map PNG, use case diagrams, Relume
sitemap) reads from this module so that the documents and images never drift.
"""

# ---------------------------------------------------------------------------
# 1. Mind maps (XMind sheets)
# ---------------------------------------------------------------------------

TOP_DOWN_ROOT = "SmartDesk\nAI-assisted IT Helpdesk SaaS"

TOP_DOWN = [
    ("Why we need it", [
        "IT requests get lost in chat, email and hallway talk",
        "Employees don't know which request to choose",
        "The same issues keep coming back",
        "How-to guides are scattered everywhere",
        "Laptops are handed out with no approval or record",
        "Managers can't see backlog, deadlines or workload",
    ]),
    ("Who uses it", [
        "Employees ask for help and follow their requests",
        "IT Staff sort, fix and deliver",
        "IT Managers approve, set deadlines, read reports",
        "Org Admins set up people, roles and services",
        "Platform Admins look after customer workspaces",
        "The AI model helps, but can only read",
    ]),
    ("What it handles", [
        "Something broke: VPN, Wi-Fi, printer",
        "Something needed: VPN access, laptop, software",
        "Something to change: the office internet provider",
        "Which devices we own and who has them",
        "A library of how-to guides",
    ]),
    ("How a request flows", [
        "Try self-help first, then send a ticket",
        "IT sorts it, assigns it and fixes it",
        "Manager approves, IT delivers the device",
        "Employee confirms or reopens; everything is logged",
    ]),
    ("What the market shows", [
        "Jira Service Management: forms, queues, SLAs, assets",
        "Freshservice Freddy AI: self-service answers with sources",
        "Our angle: quick setup for small IT teams",
        "Still to check: will companies pay, and how much",
    ]),
    ("AI assistant", [
        "Answers from company guides and shows the source",
        "Walks people through a fix step by step",
        "Turns a chat into a ticket draft",
        "Tells you where your own tickets stand",
        "Says \"I don't know\" instead of guessing",
    ]),
    ("Ground rules", [
        "Each company sees only its own data",
        "The server checks every permission",
        "Incidents, requests and changes follow their own steps",
        "AI never approves, assigns or changes anything",
        "Every action is logged; no duplicate tickets",
    ]),
    ("What we build when", [
        "Release 1: VPN issues, laptops, guides, AI",
        "Release 2: approval rules, SLAs, alerts, reports",
        "Phase 2: internet changes, repair log, workspaces",
        "Not planned: network automation, ERP, mobile app",
    ]),
    ("How we measure success", [
        "Issues solved without IT",
        "Tickets that need no follow-up questions",
        "Time it takes to send a ticket",
        "Deadlines met and tickets reopened",
        "AI answers that cite the right guide",
    ]),
]

FEATURE_ROOT = "SmartDesk\nFeature map"

FEATURES = [
    ("Accounts & access", [
        "Sign in and sign out", "Edit my profile", "Company settings",
        "Invite people and set roles", "Pause or reopen a workspace",
    ]),
    ("Employee self-service", [
        "Browse IT services", "Fill in a request form", "Follow my tickets",
        "Add comments and files", "Confirm the fix or reopen", "See my devices",
    ]),
    ("AI assistant", [
        "Answers with sources", "Step-by-step fixes",
        "Ticket draft from a chat", "\"Where's my ticket?\"",
    ]),
    ("Ticket handling", [
        "Queue with filters", "Sort and prioritise", "Assign or pick up",
        "Replies and internal notes", "Hand over or escalate", "Resolve and close",
        "Link a device or ticket",
    ]),
    ("Services & approvals", [
        "Request forms", "Approval rules", "Approve or reject with a reason",
        "Delivery checklist", "Internet provider changes",
    ]),
    ("IT devices", [
        "Add and update devices", "Hand over a device", "Take a device back",
        "Repair log", "Stock and history",
    ]),
    ("How-to guides", [
        "Write drafts", "Review and publish", "Search and read",
    ]),
    ("Deadlines & reports", [
        "SLA targets", "Deadline alerts", "Reports and export",
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
    "UC07": ("Submit a request with the right form", "Employee Self-service", "P0", ["Employee"]),
    "UC08": ("Find and track my tickets", "Employee Self-service", "P0", ["Employee"]),
    "UC09": ("Add comments and files to my ticket", "Employee Self-service", "P0", ["Employee"]),
    "UC10": ("Confirm resolution or reopen a ticket", "Employee Self-service", "P0", ["Employee"]),
    "UC11": ("View assets assigned to me", "Employee Self-service", "P1", ["Employee"]),
    "UC12": ("Ask a question and get an answer from company guides", "AI Assistant", "P0", ["Employee"]),
    "UC13": ("Get step-by-step troubleshooting", "AI Assistant", "P1", ["Employee"]),
    "UC14": ("Turn a chat into a ticket draft", "AI Assistant", "P0", ["Employee"]),
    "UC15": ("Ask in chat where my ticket stands", "AI Assistant", "P1", ["Employee"]),
    "UC16": ("View and filter the ticket queue", "Ticket Management", "P0", ["IT Staff"]),
    "UC17": ("Triage and set ticket priority", "Ticket Management", "P0", ["IT Staff"]),
    "UC18": ("Assign or pick up a ticket", "Ticket Management", "P0", ["IT Staff", "IT Manager"]),
    "UC19": ("Update status and technical notes", "Ticket Management", "P0", ["IT Staff"]),
    "UC20": ("Transfer or escalate a ticket", "Ticket Management", "P1", ["IT Staff", "IT Manager"]),
    "UC21": ("Resolve and close a ticket", "Ticket Management", "P0", ["IT Staff"]),
    "UC22": ("Link a ticket to a device or another ticket", "Ticket Management", "P1", ["IT Staff"]),
    "UC23": ("Manage request types and forms", "Catalog & Approval", "P0", ["Org Admin"]),
    "UC24": ("Configure approval rules", "Catalog & Approval", "P1", ["IT Manager"]),
    "UC25": ("Approve or reject a request with reason", "Catalog & Approval", "P0", ["IT Manager"]),
    "UC26": ("Carry out and record the delivery work", "Catalog & Approval", "P1", ["IT Staff"]),
    "UC27": ("Review and plan an internet provider change", "Catalog & Approval", "P2", ["IT Manager"]),
    "UC28": ("Add and update IT devices", "IT Assets", "P0", ["IT Staff"]),
    "UC29": ("Assign and hand over a device", "IT Assets", "P0", ["IT Staff"]),
    "UC30": ("Take a device back from an employee", "IT Assets", "P1", ["IT Staff"]),
    "UC31": ("Log repairs and maintenance", "IT Assets", "P2", ["IT Staff"]),
    "UC32": ("View device stock and history", "IT Assets", "P1", ["IT Manager"]),
    "UC33": ("Write and edit guide drafts", "Knowledge Base", "P0", ["IT Staff"]),
    "UC34": ("Review, publish and retire guides", "Knowledge Base", "P0", ["IT Manager"]),
    "UC35": ("Search and read guides without the AI", "Knowledge Base", "P0", ["Employee"]),
    "UC36": ("Set SLA targets by type and priority", "SLA & Reporting", "P1", ["IT Manager"]),
    "UC37": ("Get alerts when a deadline is at risk", "SLA & Reporting", "P1", ["IT Manager"]),
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
        ("Sign-in form", "Work email and password, with a show-password option"),
        ("Error message", "One friendly message for any failed sign-in, without saying why"),
        ("Company picker", "Choose a company if your email belongs to more than one"),
        ("Need help?", "How to reset your password or reach IT"),
    ]},
    {"id": "SCR-02", "name": "My Profile", "group": "Shared", "route": "/profile",
     "roles": "All", "ucs": ["UC02", "UC01"], "sections": [
        ("Your details", "Name, phone, department, location and photo"),
        ("Your role", "Shows your role and company; only an admin can change it"),
        ("Notifications", "Choose email or in-app alerts for updates and approvals"),
        ("Sign out", "End your session on this device"),
    ]},
    {"id": "SCR-03", "name": "Notification Center", "group": "Shared", "route": "/notifications",
     "roles": "All", "ucs": ["UC37", "UC10", "UC25"], "sections": [
        ("Notification list", "Ticket updates, approvals and deadline warnings, newest first"),
        ("Filters", "Show unread only, or filter by type and date"),
        ("Open the source", "Jump straight to the ticket, approval or device"),
        ("Mark as read", "Mark one or all notifications as read"),
    ]},
    {"id": "SCR-04", "name": "Error Pages", "group": "Shared", "route": "/403, /404",
     "roles": "All", "ucs": [], "sections": [
        ("Plain explanation", "Says the page is missing or you don't have access"),
        ("Way back", "A button back to your home page"),
    ]},

    # ---- Employee Portal ---------------------------------------------------
    {"id": "SCR-10", "name": "Employee Home", "group": "Employee Portal", "route": "/app",
     "roles": "Employee", "ucs": ["UC06", "UC08", "UC12", "UC35"], "sections": [
        ("Ask SmartDesk", "Type a question and get help from the assistant"),
        ("Quick actions", "VPN not working, request a laptop, something else"),
        ("My open tickets", "Your latest tickets, their status and next step"),
        ("Popular guides", "The how-to guides people read most"),
        ("Waiting for you", "Tickets that need your reply or confirmation"),
    ]},
    {"id": "SCR-11", "name": "AI Assistant", "group": "Employee Portal", "route": "/app/assistant",
     "roles": "Employee", "ucs": ["UC12", "UC13", "UC14", "UC15"], "sections": [
        ("Chat", "Conversation, suggested questions and a message box"),
        ("Answer with source", "Steps plus a link to the guide they came from"),
        ("When it doesn't know", "Says so honestly and offers the catalog or a ticket"),
        ("Follow-up questions", "Asks only for the details the ticket still needs"),
        ("Ticket draft", "Review the draft, then confirm, edit or discard it"),
        ("My ticket status", "Answers about your own tickets only"),
    ]},
    {"id": "SCR-12", "name": "Knowledge Base", "group": "Employee Portal", "route": "/app/kb",
     "roles": "Employee", "ucs": ["UC35"], "sections": [
        ("Search", "Search all published guides"),
        ("Topic filter", "Network, Accounts, Devices, Software, Printing"),
        ("Results", "Title, short summary and last update"),
        ("Featured guides", "Pinned guides for the most common issues"),
    ]},
    {"id": "SCR-13", "name": "KB Article", "group": "Employee Portal", "route": "/app/kb/:id",
     "roles": "Employee", "ucs": ["UC35"], "sections": [
        ("Title", "Guide name, topic and when it was last checked"),
        ("Steps", "Numbered steps with screenshots"),
        ("Was this helpful?", "A quick thumbs up or down"),
        ("Still need help?", "Open a request with this guide attached"),
        ("Related guides", "More guides on the same topic"),
    ]},
    {"id": "SCR-14", "name": "Service Catalog", "group": "Employee Portal", "route": "/app/catalog",
     "roles": "Employee", "ucs": ["UC06"], "sections": [
        ("Search", "Find a service by name or keyword"),
        ("Categories", "Report a problem, request something, propose a change"),
        ("Service cards", "What it is, whether it needs approval, how long it takes"),
        ("Not sure?", "Ask the assistant to help you choose"),
    ]},
    {"id": "SCR-15", "name": "New Request", "group": "Employee Portal", "route": "/app/requests/new/:type",
     "roles": "Employee", "ucs": ["UC07", "UC14"], "sections": [
        ("About this service", "What you're asking for, approval and expected time"),
        ("Request form", "Only the fields this service needs, checked as you go"),
        ("Attachments", "Add screenshots or files, up to 10 MB"),
        ("What happens next", "The steps after you submit"),
        ("Submit", "Check your answers and get a ticket number"),
    ]},
    {"id": "SCR-16", "name": "My Requests", "group": "Employee Portal", "route": "/app/requests",
     "roles": "Employee", "ucs": ["UC08"], "sections": [
        ("Search", "Find a ticket by number or title"),
        ("Filters", "Status, type and date"),
        ("Ticket list", "Number, title, type, status, owner, last update"),
        ("Nothing yet", "A friendly prompt to make your first request"),
    ]},
    {"id": "SCR-17", "name": "Request Detail", "group": "Employee Portal", "route": "/app/requests/:id",
     "roles": "Employee", "ucs": ["UC08", "UC09", "UC10"], "sections": [
        ("Summary", "Ticket number, type, status, priority and deadline"),
        ("Progress", "Where your ticket is, step by step"),
        ("Conversation", "Messages and files between you and IT"),
        ("Who's on it", "Who is working on it and the approval decision"),
        ("Confirm or reopen", "Confirm the fix, or reopen within 7 days"),
    ]},
    {"id": "SCR-18", "name": "My Assets", "group": "Employee Portal", "route": "/app/assets",
     "roles": "Employee", "ucs": ["UC11"], "sections": [
        ("My devices", "Model, asset tag and serial number"),
        ("Handover", "When you got it, from whom, and its condition"),
        ("Report a problem", "Opens a ticket already linked to this device"),
    ]},

    # ---- IT Workspace ------------------------------------------------------
    {"id": "SCR-20", "name": "Agent Dashboard", "group": "IT Workspace", "route": "/it",
     "roles": "IT Staff, IT Manager", "ucs": ["UC16"], "sections": [
        ("Workload", "Unassigned, mine, close to deadline, waiting"),
        ("My priorities", "Your tickets, most urgent first"),
        ("Ready to deliver", "Approved requests waiting for IT"),
        ("Shortcuts", "Queue, devices and guide editor"),
    ]},
    {"id": "SCR-21", "name": "Ticket Queue", "group": "IT Workspace", "route": "/it/tickets",
     "roles": "IT Staff, IT Manager", "ucs": ["UC16", "UC17", "UC18"], "sections": [
        ("Views", "Unassigned, mine, my team, everything I can see"),
        ("Filters", "Type, status, priority, deadline, requester, team"),
        ("Ticket list", "Number, title, requester, priority, owner, deadline"),
        ("Quick actions", "Pick up, assign or set priority from the list"),
        ("Empty or loading", "Clear filters, or retry if nothing loads"),
    ]},
    {"id": "SCR-22", "name": "Ticket Detail", "group": "IT Workspace", "route": "/it/tickets/:id",
     "roles": "IT Staff, IT Manager", "ucs": ["UC17", "UC18", "UC19", "UC20", "UC21", "UC22"], "sections": [
        ("Summary", "Ticket number, status, priority and time left"),
        ("What was asked", "Description, form answers, files and chat summary"),
        ("Reply or note", "Reply to the employee or leave an IT-only note"),
        ("Actions", "Prioritise, assign, change status, hand over or escalate"),
        ("Resolve", "Explain the fix before marking it resolved"),
        ("Links", "Related device, tickets and guide"),
        ("History", "Every change, who made it and when"),
    ]},
    {"id": "SCR-23", "name": "Fulfilment Task", "group": "IT Workspace", "route": "/it/fulfilment/:id",
     "roles": "IT Staff", "ucs": ["UC26", "UC29"], "sections": [
        ("Approval", "Stays locked until a manager approves"),
        ("Checklist", "The steps for this kind of request"),
        ("Pick a device", "Shows only devices that are free to hand out"),
        ("Hand over", "Give the device and record the handover"),
        ("Finish", "Close the task and let the employee know"),
    ]},
    {"id": "SCR-24", "name": "Asset Inventory", "group": "IT Workspace", "route": "/it/assets",
     "roles": "IT Staff, IT Manager (read)", "ucs": ["UC28", "UC32"], "sections": [
        ("Stock", "How many devices are free, in use or in repair"),
        ("Search & filters", "Type, status, location and holder"),
        ("Device list", "Tag, model, status, holder and location"),
        ("Add device", "Register a device with its own asset tag"),
    ]},
    {"id": "SCR-25", "name": "Asset Detail", "group": "IT Workspace", "route": "/it/assets/:id",
     "roles": "IT Staff, IT Manager (read)", "ucs": ["UC28", "UC29", "UC30", "UC31", "UC32"], "sections": [
        ("Device details", "Model, serial, purchase date, warranty, location"),
        ("Status", "Free, reserved, in use, in repair or retired"),
        ("Hand over / take back", "Give it to someone or take it back"),
        ("Repair log", "When, what was done and by whom"),
        ("History", "Who had it before and related tickets"),
    ]},
    {"id": "SCR-26", "name": "KB Editor", "group": "IT Workspace", "route": "/it/kb",
     "roles": "IT Staff", "ucs": ["UC33"], "sections": [
        ("My guides", "Drafts, guides in review and live guides"),
        ("Editor", "Write steps with text and images"),
        ("Who can read it", "Everyone, or only certain teams"),
        ("Send for review", "Ask an IT Manager to check it"),
    ]},

    # ---- Manager Console ---------------------------------------------------
    {"id": "SCR-30", "name": "Approval Inbox", "group": "Manager Console", "route": "/manage/approvals",
     "roles": "IT Manager", "ucs": ["UC25"], "sections": [
        ("Waiting for you", "Requests that need your decision"),
        ("Filters", "Type, department and date"),
        ("Request summary", "Who asked, why, by when, and what's in stock"),
        ("Decision", "Approve, or reject with a short reason"),
        ("Past decisions", "What was decided, by whom and when"),
    ]},
    {"id": "SCR-31", "name": "Change Review", "group": "Manager Console", "route": "/manage/changes/:id",
     "roles": "IT Manager", "ucs": ["UC27"], "sections": [
        ("The change", "Office, current provider, reason, proposed date"),
        ("Impact & backup plan", "Who is affected, downtime, how to roll back"),
        ("Decision", "Approve, reject or ask for more details"),
        ("Schedule & result", "When it happens and how it went"),
    ]},
    {"id": "SCR-32", "name": "KB Review", "group": "Manager Console", "route": "/manage/kb",
     "roles": "IT Manager", "ucs": ["UC34"], "sections": [
        ("To review", "Guides waiting for your review"),
        ("Compare & preview", "See what changed since the last version"),
        ("Publish or retire", "Make it live for employees and the AI, or take it down"),
    ]},
    {"id": "SCR-33", "name": "SLA & Reports", "group": "Manager Console", "route": "/manage/reports",
     "roles": "IT Manager", "ucs": ["UC37", "UC38"], "sections": [
        ("Filters", "Date range, team, type and priority"),
        ("Key numbers", "Ticket volume, deadlines met, reopens, self-service"),
        ("At-risk tickets", "Tickets close to or past their deadline"),
        ("Charts", "Trends over time and by category"),
        ("Export", "Download as CSV or PDF with the same filters"),
    ]},
    {"id": "SCR-34", "name": "SLA Policies", "group": "Manager Console", "route": "/manage/sla",
     "roles": "IT Manager", "ucs": ["UC36"], "sections": [
        ("Working hours", "Office hours, holidays and timezone"),
        ("Targets", "How fast to respond and resolve, by type and priority"),
        ("Alerts", "Warn at 80% of the deadline, alert when it's missed"),
        ("Pause rules", "Stop the clock while waiting on the employee"),
    ]},
    {"id": "SCR-35", "name": "Approval Rules", "group": "Manager Console", "route": "/manage/approval-rules",
     "roles": "IT Manager", "ucs": ["UC24"], "sections": [
        ("Rules", "Which requests need approval"),
        ("Approver", "A role or a specific person"),
        ("When it applies", "Department, cost or device type"),
        ("Start date", "Past decisions stay as they were"),
    ]},

    # ---- Admin -------------------------------------------------------------
    {"id": "SCR-40", "name": "Organization Settings", "group": "Admin", "route": "/admin/org",
     "roles": "Org Admin", "ucs": ["UC03"], "sections": [
        ("Company profile", "Name, logo and default language"),
        ("Offices & teams", "Used to send tickets to the right people"),
        ("Regional settings", "Timezone and date format"),
    ]},
    {"id": "SCR-41", "name": "Members & Roles", "group": "Admin", "route": "/admin/members",
     "roles": "Org Admin", "ucs": ["UC04"], "sections": [
        ("Members", "Name, email, role and status"),
        ("Invite", "Invite people by email and pick their role"),
        ("Roles", "Employee, IT Staff, IT Manager or Org Admin"),
        ("Lock / unlock", "Block access without losing their history"),
    ]},
    {"id": "SCR-42", "name": "Catalog Builder", "group": "Admin", "route": "/admin/catalog",
     "roles": "Org Admin", "ucs": ["UC23"], "sections": [
        ("Services", "Create, reorder, publish or hide"),
        ("Form fields", "Add fields, mark required ones, write help text"),
        ("Routing", "Which team gets it and whether it needs approval"),
        ("Preview & publish", "Try it as an employee, then publish"),
    ]},
    {"id": "SCR-50", "name": "Tenants", "group": "Admin", "route": "/platform/tenants",
     "roles": "Platform Admin", "ucs": ["UC05"], "sections": [
        ("Companies", "Name, plan, status and start date"),
        ("Pause / reopen", "A paused company can only read its data"),
        ("Company details", "Contacts and limits only, never ticket content"),
    ]},
]

# Parent page for each screen in the Relume tree (None = directly under group).
SITEMAP_PARENT = {
    "SCR-11": "SCR-10", "SCR-13": "SCR-12", "SCR-15": "SCR-14", "SCR-17": "SCR-16",
    "SCR-22": "SCR-21", "SCR-25": "SCR-24", "SCR-31": "SCR-30",
}
