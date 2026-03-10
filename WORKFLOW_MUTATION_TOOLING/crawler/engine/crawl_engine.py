from pathlib import Path


def crawl():
    for p in Path(".").rglob("*.py"):
        print("Processing:",p)

if __name__=="__main__":
    crawl()
