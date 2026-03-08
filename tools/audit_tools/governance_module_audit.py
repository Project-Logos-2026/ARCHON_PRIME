import ast
from pathlib import Path
from audit_utils import write_log,generate_id

KEYWORDS=[
    "governance",
    "contract",
    "enforce",
    "validate",
    "policy",
    "rule",
    "constraint"
]

def run(target):

    issues=[]

    for p in Path(target).rglob("*.py"):

        try:

            text=open(p).read().lower()

            for k in KEYWORDS:

                if k in text:

                    issues.append({
                        "id":generate_id(str(p)+k),
                        "module":str(p),
                        "keyword":k,
                        "issue":"governance_module"
                    })

                    break

        except:
            pass

    write_log(
        "governance_module_audit",
        target,
        "governance_module",
        issues
    )
