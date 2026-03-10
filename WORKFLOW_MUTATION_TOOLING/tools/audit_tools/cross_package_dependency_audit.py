import ast
from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        try:

            tree = ast.parse(open(p).read())

            pkg = p.parts[-2]

            for node in ast.walk(tree):

                if isinstance(node, ast.ImportFrom):

                    if node.module and node.module.split(".")[0] != pkg:

                        issues.append(
                            {
                                "id": generate_id(str(p) + node.module),
                                "file": str(p),
                                "module": node.module,
                                "issue": "cross_package_dependency",
                            }
                        )

        except Exception:
            pass

    write_log(
        "cross_package_dependency_audit", target, "cross_package_dependency", issues
    )
