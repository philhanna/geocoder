# Changelog

## Unreleased

### Added
- Document how to obtain the `sqlite3` command-line tool in README

## [0.1.0] - 2026-04-07

### Added
- Windows support: `DEFAULT_CONFIG_PATH` resolves to `%APPDATA%\geocode\config.yaml` on Windows
- `geocode.bat` launcher for Windows
- Windows conventions documented in README
- Unit tests for `SqliteCacheAdapter`, `geocode()` use case, and `_TrackingCache` (13 tests)
- Comprehensive docstrings on all classes and methods
- README with installation, configuration, CLI usage, and Python API documentation
- `--verbose` / `-v` flag on the CLI to show whether result came from cache or API
- `geocode` bash launcher script at project root
- CLI adapter at `src/geocode/adapters/geocode.py`
- SQLite cache database and parent directory created automatically on first use
- Full Census API JSON response stored as `jsonstring` column in the cache; existing databases migrated automatically
- `geocode.application` package containing the use case (`core.py`)
- `geocode.ports` package with `GeocodeCachePort` and `GeocoderPort` split into individual modules
- Cache database path read from `~/.config/geocode/config.yaml` (configurable)
- `sample_config.yaml` at project root; `tests/conftest.py` fixture for unit tests
- `pyproject.toml` with `hatchling` build backend, `pyyaml` and `requests` dependencies
- Ports and Adapters architecture: `geocode.ports`, `geocode.application`, `geocode.adapters`

### Changed
- Adapter and port modules renamed to match their class names
  (`census.py` → `census_geocoder_adapter.py`, `sqlite_cache.py` → `sqlite_cache_adapter.py`,
  `cache.py` → `geocode_cache_port.py`, `geocoder.py` → `geocoder_port.py`)
- `GeocoderPort.geocode()` returns `(latitude, longitude, jsonstring)` instead of `(latitude, longitude)`
- `GeocodeCachePort.store()` accepts a `jsonstring` parameter

### Initial
- `geocode()` function with SQLite cache and U.S. Census Bureau Geocoding API
