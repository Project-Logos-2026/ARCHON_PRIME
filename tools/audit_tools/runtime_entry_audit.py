from pathlib import Path
from audit_utils import write_log,generate_id

def run(target):

    issues=[]

    for p in Path(target).rglob("*.py"):

        text=open(p).read()

        if "__main__" in text:

            issues.append({
                "id":generate_id(str(p)),
                "file":str(p),
                "issue":"runtime_entrypoint"
            })

    write_log("runtime_entry_audit",target,"runtime_entrypoint",issues)
