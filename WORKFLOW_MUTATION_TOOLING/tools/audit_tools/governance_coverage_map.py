import json
from pathlib import Path

from audit_utils import generate_id, write_log

LOG_DIR = Path("/workspaces/ARCHON_PRIME/AUDIT_LOGS")

def run(target):

    contracts=json.load(open(LOG_DIR/"governance_contract_audit.json"))
    modules=json.load(open(LOG_DIR/"governance_module_audit.json"))

    contract_list=[c["artifact"] for c in contracts["issues"]]
    module_list=[m["module"] for m in modules["issues"]]

    issues=[]

    for contract in contract_list:

        paired=False

        for module in module_list:

            if contract.split("/")[-1].split(".")[0] in module:

                issues.append({
                    "id":generate_id(contract+module),
                    "contract":contract,
                    "module":module,
                    "issue":"governance_enforced"
                })

                paired=True
                break

        if not paired:

            issues.append({
                "id":generate_id(contract),
                "contract":contract,
                "module":None,
                "issue":"missing_enforcement_module"
            })

    write_log(
        "governance_coverage_map",
        target,
        "governance_pairing",
        issues
    )
