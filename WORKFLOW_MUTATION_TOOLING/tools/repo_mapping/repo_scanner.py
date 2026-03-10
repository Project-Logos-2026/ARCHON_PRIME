import json
import os
from pathlib import Path

ROOT = Path(".")
OUT = Path("logs/repo_scan.json")


def scan_repo():
    result = []
    for root, _dirs, files in os.walk(ROOT):
        for f in files:
            result.append(str(Path(root) / f))
    return result


if __name__ == "__main__":
    data = scan_repo()
    OUT.parent.mkdir(exist_ok=True)
    json.dump(data, open(OUT, "w"), indent=2)
    print("Repo scan complete:", len(data), "files")
