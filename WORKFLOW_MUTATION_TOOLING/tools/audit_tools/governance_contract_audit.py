import re
from pathlib import Path
from audit_utils import write_log,generate_id

GOV_TERMS = [
    "governance",
    "contract",
    "policy",
    "protocol",
    "rule",
    "constraint",
    "spec",
    "design"
]

def run(target):

    issues=[]

    for p in Path(target).rglob("*"):

        if p.suffix.lower() in [".md",".txt",".yaml",".yml",".json"]:

            try:

                text=open(p).read().lower()

                for term in GOV_TERMS:

                    if term in text:

                        issues.append({
                            "id":generate_id(str(p)+term),
                            "artifact":str(p),
                            "governance_term":term,
                            "issue":"governance_contract"
                        })

                        break

            except:
                pass

    write_log(
        "governance_contract_audit",
        target,
        "governance_contract",
        issues
    )
