import yaml
from pathlib import Path


class Settings:
    def __init__(self, config_file='config.yml'):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_file, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found. Using default values.")
            return {}

    @property
    def log_save_path(self):
        """Get the log save path."""
        return Path(self.config.get('log_save_path', './data'))

    @property
    def clean_log_save_path(self):
        """Get the clean log save path."""
        return self.config.get('clean_log_save_path', 'clean_log')

    @property
    def log_open_coding(self):
        """Get the log open coding."""
        return self.config.get('log_open_coding', 'utf8')

    @property
    def re_compile(self):
        return self.config.get('re_compile', None)

    def get(self, key, default=None):
        """Get a configuration value by key."""
        return self.config.get(key, default)

    def __str__(self):
        """String representation of the current settings."""
        return f"Settings(config_file='{self.config_file}', config={self.config})"


# Usage example
if __name__ == "__main__":
    settings = Settings()
    print(f"Log save path: {settings.log_save_path}")
    print(f"Clean log save path: {settings.clean_log_save_path}")
    print(f"Log open coding: {settings.log_open_coding}")
