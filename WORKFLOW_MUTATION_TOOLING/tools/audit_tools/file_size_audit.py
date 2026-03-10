from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        size = p.stat().st_size

        if size > 50000:

            issues.append(
                {
                    "id": generate_id(str(p)),
                    "file": str(p),
                    "size_bytes": size,
                    "issue": "oversized_module",
                }
            )

    write_log("file_size_audit", target, "oversized_module", issues)
