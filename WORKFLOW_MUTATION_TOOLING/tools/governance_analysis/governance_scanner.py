import json
from pathlib import Path


def scan():
    gov=[]
    for p in Path(".").rglob("*governance*.py"):
        gov.append(str(p))
    json.dump(gov,open("logs/governance_modules.json","w"),indent=2)

if __name__=="__main__":
    scan()
