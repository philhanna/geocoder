from pathlib import Path

import pytest
import yaml

import geocode.config as geocode_config

SAMPLE_CONFIG_PATH = Path(__file__).parent.parent / "sample_config.yaml"


@pytest.fixture()
def config_path(tmp_path, monkeypatch):
    """
    Point geocode.config at sample_config.yaml, but redirect the db_path to a
    temporary directory so each test starts with an empty cache.
    """
    sample = yaml.safe_load(SAMPLE_CONFIG_PATH.read_text())
    sample["cache"]["db_path"] = str(tmp_path / "geocode_cache.db")

    patched = tmp_path / "config.yaml"
    patched.write_text(yaml.dump(sample))

    monkeypatch.setattr(geocode_config, "DEFAULT_CONFIG_PATH", patched)
    return patched
