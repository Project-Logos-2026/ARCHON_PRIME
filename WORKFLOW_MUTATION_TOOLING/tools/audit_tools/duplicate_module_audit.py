from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    names={}
    issues=[]

    for p in Path(target).rglob("*.py"):

        name=p.name

        if name in names:

            issues.append({
                "id":generate_id(name),
                "file_a":names[name],
                "file_b":str(p),
                "issue":"duplicate_module"
            })

        else:
            names[name]=str(p)

    write_log("duplicate_module_audit",target,"duplicate_module",issues)
