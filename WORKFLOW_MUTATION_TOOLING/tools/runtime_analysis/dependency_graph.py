import json
from pathlib import Path

IMPORT_FILE="logs/import_map.json"

def build_graph():
    data=json.load(open(IMPORT_FILE))
    graph={}
    for module,imports in data.items():
        graph[module]=imports
    json.dump(graph,open("logs/dependency_graph.json","w"),indent=2)

if __name__=="__main__":
    build_graph()
