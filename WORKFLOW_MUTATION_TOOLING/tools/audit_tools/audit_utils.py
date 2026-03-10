import datetime
import hashlib
import json
from pathlib import Path

LOG_DIR = Path("/workspaces/ARCHON_PRIME/AUDIT_LOGS")
LOG_DIR.mkdir(exist_ok=True)


def generate_id(text):
    return hashlib.sha1(text.encode()).hexdigest()[:12]


def today():
    d = datetime.date.today()
    return f"{d.month}-{d.day}-{d.year}"


def write_log(name, target, error_type, issues):

    files = set([i["file"] for i in issues if "file" in i])

    data = {
        "header": {
            "audit": name,
            "target_directory": target,
            "identity_tag": generate_id(name + target),
            "error_type": error_type,
            "total_errors": len(issues),
            "files_affected": len(files),
            "date": today(),
        },
        "issues": issues,
    }

    out = LOG_DIR / (name + ".json")

    with open(out, "w") as f:
        json.dump(data, f, indent=2)
