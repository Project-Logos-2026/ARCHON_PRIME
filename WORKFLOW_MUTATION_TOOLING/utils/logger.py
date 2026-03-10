import datetime
import json
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def log(event, data=None):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event": event,
        "data": data or {},
    }
    with open(LOG_DIR / "execution_log.json", "a") as f:
        f.write(json.dumps(entry) + "\n")
