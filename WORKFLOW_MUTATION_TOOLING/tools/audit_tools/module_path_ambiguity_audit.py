from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    modules = {}
    issues = []

    for p in Path(target).rglob("*.py"):

        short = p.stem

        if short in modules:

            issues.append(
                {
                    "id": generate_id(short),
                    "module": short,
                    "file_a": modules[short],
                    "file_b": str(p),
                    "issue": "module_path_ambiguity",
                }
            )

        else:
            modules[short] = str(p)

    write_log("module_path_ambiguity_audit", target, "module_path_ambiguity", issues)
