import json
import os
import hashlib
from datetime import datetime, timezone

PLAYBOOKS = {
    "T1059.001": [
        "Capture the full decoded command line.",
        "Check outbound connections from the PowerShell process.",
        "Isolate host if the payload downloads or executes further code.",
    ],
    "T1003.001": [
        "Treat credentials on this host as compromised.",
        "Force password reset for accounts active on the host.",
        "Acquire memory image before reboot if possible.",
    ],
}

def build_case(rule, event):
    technique = rule["technique"]
    fingerprint = hashlib.sha1(
        f"{rule['title']}|{event.get('command')}".encode()
    ).hexdigest()[:10]

    return {
        "case_id": f"DVL-{fingerprint}",
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rule": rule["title"],
        "technique": technique,
        "event": event,
        "recommended_actions": PLAYBOOKS.get(technique, ["Investigate manually."]),
        "status": "new",
    }

def write_case(case, outdir="reports/cases"):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"{case['case_id']}.json")
    with open(path, "w") as f:
        json.dump(case, f, indent=2)
    return path