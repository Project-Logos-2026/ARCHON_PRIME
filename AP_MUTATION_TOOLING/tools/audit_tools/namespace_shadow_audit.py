from pathlib import Path
from audit_utils import write_log,generate_id

def run(target):

    names={}
    issues=[]

    for p in Path(target).rglob("*.py"):

        name=p.stem

        if name in names:

            issues.append({
                "id":generate_id(name),
                "module":name,
                "file_a":names[name],
                "file_b":str(p),
                "issue":"namespace_shadow"
            })

        else:
            names[name]=str(p)

    write_log("namespace_shadow_audit",target,"namespace_shadow",issues)
