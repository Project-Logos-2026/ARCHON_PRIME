import ast
import json
from pathlib import Path

def extract_imports(file):
    imports=[]
    try:
        tree=ast.parse(open(file).read())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                for n in node.names:
                    imports.append(n.name)
            if isinstance(node,ast.ImportFrom):
                imports.append(node.module)
    except:
        pass
    return imports

def scan():
    result={}
    for p in Path(".").rglob("*.py"):
        result[str(p)]=extract_imports(p)
    json.dump(result,open("logs/import_map.json","w"),indent=2)

if __name__=="__main__":
    scan()
