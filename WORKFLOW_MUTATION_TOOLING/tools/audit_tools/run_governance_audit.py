import sys

import governance_contract_audit
import governance_coverage_map
import governance_module_audit


def run(target):

    governance_contract_audit.run(target)

    governance_module_audit.run(target)

    governance_coverage_map.run(target)

if __name__=="__main__":

    target=sys.argv[1]

    run(target)
