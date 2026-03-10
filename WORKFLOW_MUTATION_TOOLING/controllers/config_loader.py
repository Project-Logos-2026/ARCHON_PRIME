import json
import os


class ConfigLoader:

    def __init__(self, root_path):
        self.root = root_path

    def load_json(self, path):
        with open(os.path.join(self.root, path)) as f:
            return json.load(f)

    def load_crawl_config(self):
        return self.load_json("config/crawl_config.json")

    def load_repair_config(self):
        return self.load_json("config/repair_config.json")

    def load_simulation_config(self):
        return self.load_json("config/simulation_config.json")

    def load_module_registry(self):
        return self.load_json("registry/module_registry.json")

    def load_audit_registry(self):
        return self.load_json("registry/audit_registry.json")

    def load_repair_registry(self):
        return self.load_json("registry/repair_registry.json")

    def load_simulation_registry(self):
        return self.load_json("registry/simulation_registry.json")

    def load_all(self):
        return {
            "crawl_config": self.load_crawl_config(),
            "repair_config": self.load_repair_config(),
            "simulation_config": self.load_simulation_config(),
            "module_registry": self.load_module_registry(),
            "audit_registry": self.load_audit_registry(),
            "repair_registry": self.load_repair_registry(),
            "simulation_registry": self.load_simulation_registry(),
        }
