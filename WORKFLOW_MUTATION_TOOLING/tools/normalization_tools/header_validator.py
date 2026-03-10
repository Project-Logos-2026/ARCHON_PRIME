import json
from pathlib import Path


def check_headers():
    missing = []
    for p in Path(".").rglob("*.py"):
        text = open(p).read().strip()
        if not text.startswith("#"):
            missing.append(str(p))
    json.dump(missing, open("logs/header_violations.json", "w"), indent=2)


if __name__ == "__main__":
    check_headers()
