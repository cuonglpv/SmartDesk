"""Capture prototype screens into docs/images/ui/ with headless Chrome/Edge."""

from common import DOCS, ROOT, screenshot

PROTOTYPE = (ROOT / "prototype" / "index.html").resolve().as_uri()
OUT = DOCS / "images" / "ui"

# (file name, route, viewport height)
SHOTS = [
    ("01-employee-home", "/app", 1080),
    ("02-ai-assistant-draft", "/app/assistant?demo=vpn", 900),
    ("03-ai-assistant-no-source", "/app/assistant?demo=nosource", 900),
    ("04-service-catalog", "/app/catalog", 960),
    ("05-new-request-validation", "/app/requests/new/laptop?demo=invalid", 960),
    ("06-request-detail-resolved", "/app/requests/INC-1016", 1000),
    ("07-agent-queue", "/it/tickets", 760),
    ("08-agent-ticket-detail", "/it/tickets/INC-1042", 1180),
    ("09-agent-resolve-validation", "/it/tickets/INC-1042?demo=resolve", 1180),
    ("10-fulfilment-locked", "/it/fulfilment/SR-1038", 860),
    ("11-manager-approval-reject-reason", "/manage/approvals?demo=reject", 900),
    ("12-manager-reports", "/manage/reports", 900),
    ("13-asset-inventory", "/it/assets", 760),
]

if __name__ == "__main__":
    for name, route, height in SHOTS:
        print(screenshot(f"{PROTOTYPE}#{route}", OUT / f"{name}.png", 1440, height, scale=1))
