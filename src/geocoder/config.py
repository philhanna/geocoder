import os
import platform
from pathlib import Path

import yaml

if platform.system() == "Windows":
    DEFAULT_CONFIG_PATH = Path(os.environ["APPDATA"]) / "geocoder" / "config.yaml"
else:
    DEFAULT_CONFIG_PATH = Path.home() / ".config" / "geocoder" / "config.yaml"


def load(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """Load and return the YAML configuration file as a dictionary.

    Args:
        config_path: Path to the YAML config file. Defaults to
            ``~/.config/geocoder/config.yaml`` on Linux/macOS or
            ``%APPDATA%\\geocoder\\config.yaml`` on Windows.

    Returns:
        Parsed contents of the config file.

    Raises:
        FileNotFoundError: if the config file does not exist.
        yaml.YAMLError: if the file is not valid YAML.
    """
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_db_path(config_path: Path = DEFAULT_CONFIG_PATH) -> str:
    """Return the cache database path from the configuration file.

    Reads ``cache.db_path`` from the config file. The returned value may
    contain a leading ``~``, which callers are responsible for expanding.

    Args:
        config_path: Path to the YAML config file. Defaults to
            ``~/.config/geocoder/config.yaml`` on Linux/macOS or
            ``%APPDATA%\\geocoder\\config.yaml`` on Windows.

    Returns:
        The configured database file path string.

    Raises:
        FileNotFoundError: if the config file does not exist.
        KeyError: if ``cache.db_path`` is missing from the config.
    """
    return load(config_path)["cache"]["db_path"]
