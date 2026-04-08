from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "geocode" / "config.yaml"


def load(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_db_path(config_path: Path = DEFAULT_CONFIG_PATH) -> str:
    return load(config_path)["cache"]["db_path"]
