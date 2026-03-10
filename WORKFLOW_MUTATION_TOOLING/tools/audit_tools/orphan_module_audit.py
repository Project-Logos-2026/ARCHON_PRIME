import ast
from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    imports=set()
    files=set()

    issues=[]

    for p in Path(target).rglob("*.py"):

        files.add(p.stem)

        try:
            tree=ast.parse(open(p).read())

            for node in ast.walk(tree):

                if isinstance(node,ast.Import):
                    for n in node.names:
                        imports.add(n.name.split(".")[0])

        except Exception:
            pass

    for f in files:
        if f not in imports:

            issues.append({
                "id":generate_id(f),
                "module":f,
                "issue":"orphan_module"
            })

    write_log("orphan_module_audit",target,"orphan_module",issues)
