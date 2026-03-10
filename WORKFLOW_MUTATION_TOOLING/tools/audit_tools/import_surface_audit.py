import ast
from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):
        try:
            tree = ast.parse(open(p).read())
            for node in ast.walk(tree):

                if isinstance(node, ast.ImportFrom):
                    if node.module and "." in node.module:

                        issues.append(
                            {
                                "id": generate_id(str(p) + node.module),
                                "file": str(p),
                                "line": node.lineno,
                                "module": node.module,
                                "issue": "deep_import",
                            }
                        )

        except Exception:
            pass

    write_log("import_surface_audit", target, "deep_import", issues)
