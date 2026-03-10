import ast
from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    imports={}
    issues=[]

    for p in Path(target).rglob("*.py"):

        try:
            tree=ast.parse(open(p).read())

            deps=[]

            for node in ast.walk(tree):

                if isinstance(node,ast.Import):
                    for n in node.names:
                        deps.append(n.name)

                if isinstance(node,ast.ImportFrom):
                    if node.module:
                        deps.append(node.module)

            imports[str(p)]=deps

        except Exception:
            pass

    for a in imports:
        for b in imports[a]:
            if b in imports:
                if a in imports[b]:

                    issues.append({
                        "id":generate_id(a+b),
                        "file_a":a,
                        "file_b":b,
                        "issue":"circular_dependency"
                    })

    write_log("circular_dependency_audit",target,"dependency_cycle",issues)
