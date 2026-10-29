"""Capture prototype screens into docs/images/ui/<role>/ with headless Chrome/Edge."""

import shutil

from common import DOCS, ROOT, screenshot

PROTOTYPE = (ROOT / "prototype" / "index.html").resolve().as_uri()
OUT = DOCS / "images" / "ui"

# role folder -> [(file name, route, viewport height)]
SHOTS = {
    "common": [
        ("01-sign-in", "/login", 820),
        ("02-sign-in-error", "/login?demo=signinerror", 820),
        ("03-sign-in-choose-company", "/login?demo=company", 820),
        ("04-not-found", "/app/requests/INC-1047", 520),
    ],
    "employee": [
        ("01-home", "/app", 1080),
        ("02-ai-answer-with-source", "/app/assistant?demo=answer", 900),
        ("03-ai-ticket-draft", "/app/assistant?demo=vpn", 900),
        ("04-ai-no-source", "/app/assistant?demo=nosource", 900),
        ("05-ai-ticket-status", "/app/assistant?demo=status", 900),
        ("06-knowledge-base", "/app/kb", 760),
        ("07-kb-article", "/app/kb/KB-024", 820),
        ("08-service-catalog", "/app/catalog", 1060),
        ("09-new-request", "/app/requests/new/laptop", 1000),
        ("10-new-request-errors", "/app/requests/new/laptop?demo=invalid", 1060),
        ("11-my-requests", "/app/requests", 640),
        ("12-request-in-progress", "/app/requests/INC-1042", 1060),
        ("13-request-waiting-approval", "/app/requests/SR-1038", 900),
        ("14-request-resolved", "/app/requests/INC-1016", 1060),
        ("15-my-assets", "/app/assets", 560),
        ("16-profile", "/profile?role=employee", 860),
        ("17-profile-error", "/profile?role=employee&demo=profileerror", 900),
    ],
    "it-staff": [
        ("01-dashboard", "/it?role=staff", 820),
        ("02-ticket-queue", "/it/tickets?role=staff", 700),
        ("03-ticket-detail", "/it/tickets/INC-1042?role=staff", 1180),
        ("04-internal-note", "/it/tickets/INC-1042?role=staff&demo=internal", 1180),
        ("05-resolve-needs-note", "/it/tickets/INC-1042?role=staff&demo=resolve", 1180),
        ("06-fulfilment-locked", "/it/fulfilment/SR-1038?role=staff", 820),
        ("07-fulfilment-ready", "/it/fulfilment/SR-1038?role=staff&demo=approved", 820),
        ("08-asset-inventory", "/it/assets?role=staff", 720),
        ("09-kb-editor-spec", "/it/kb?role=staff", 520),
        ("10-profile", "/profile?role=staff", 860),
    ],
    "it-manager": [
        ("01-approval-inbox", "/manage/approvals", 860),
        ("02-reject-needs-reason", "/manage/approvals?demo=reject", 900),
        ("03-approved", "/manage/approvals?demo=approve", 860),
        ("04-sla-reports", "/manage/reports", 860),
        ("05-ticket-queue", "/it/tickets?role=manager", 700),
        ("06-asset-inventory-read-only", "/it/assets?role=manager", 720),
        ("07-sla-policies-spec", "/manage/sla", 520),
        ("08-kb-review-spec", "/manage/kb", 520),
        ("09-profile", "/profile?role=manager", 860),
    ],
}

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    for role, shots in SHOTS.items():
        for name, route, height in shots:
            print(screenshot(f"{PROTOTYPE}#{route}", OUT / role / f"{name}.png", 1440, height, scale=1))
