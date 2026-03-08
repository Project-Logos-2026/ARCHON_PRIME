import ast
from pathlib import Path
from audit_utils import write_log,generate_id

def run(target):

    issues=[]

    for p in Path(target).rglob("*.py"):

        try:
            tree=ast.parse(open(p).read())

            imports=[]
            names=set()

            for node in ast.walk(tree):

                if isinstance(node,ast.Import):
                    for n in node.names:
                        imports.append(n.name)

                if isinstance(node,ast.Name):
                    names.add(node.id)

            for imp in imports:
                if imp.split(".")[0] not in names:

                    issues.append({
                        "id":generate_id(str(p)+imp),
                        "file":str(p),
                        "import":imp,
                        "issue":"unused_import"
                    })

        except:
            pass

    write_log("unused_import_audit",target,"unused_import",issues)
