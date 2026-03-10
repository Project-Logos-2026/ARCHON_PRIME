import ast
from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    symbols={}
    issues=[]

    for p in Path(target).rglob("*.py"):

        try:
            tree=ast.parse(open(p).read())

            for node in ast.walk(tree):

                if isinstance(node,ast.FunctionDef) or isinstance(node,ast.ClassDef):

                    name=node.name

                    if name in symbols:

                        issues.append({
                            "id":generate_id(name+str(p)),
                            "symbol":name,
                            "file_a":symbols[name],
                            "file_b":str(p),
                            "issue":"symbol_collision"
                        })

                    else:
                        symbols[name]=str(p)

        except Exception:
            pass

    write_log("symbol_collision_audit",target,"symbol_collision",issues)
