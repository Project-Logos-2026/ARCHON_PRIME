from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        text = open(p).read()

        if not text.startswith("#"):

            issues.append(
                {"id": generate_id(str(p)), "file": str(p), "issue": "missing_header"}
            )

    write_log("header_schema_audit", target, "header_violation", issues)
