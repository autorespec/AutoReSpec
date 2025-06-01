import yaml
import os

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(config_dir, "..","config.yaml")

        with open(config_path, "r") as file:
            self.settings = yaml.safe_load(file)

    def get(self, key, default=None):
        return self.settings.get(key, default)

config = Config()