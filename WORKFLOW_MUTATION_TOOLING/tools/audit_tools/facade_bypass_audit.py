import ast
from pathlib import Path

from audit_utils import generate_id, write_log

FACADE = "imports"


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        try:

            tree = ast.parse(open(p).read())

            for node in ast.walk(tree):

                if isinstance(node, ast.ImportFrom):

                    if node.module and not node.module.startswith(FACADE):

                        issues.append(
                            {
                                "id": generate_id(str(p) + node.module),
                                "file": str(p),
                                "module": node.module,
                                "issue": "facade_bypass",
                            }
                        )

        except Exception:
            pass

    write_log("facade_bypass_audit", target, "facade_bypass", issues)
