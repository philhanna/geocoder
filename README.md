# Geocode

Converts a U.S. street address into latitude and longitude coordinates using
the [U.S. Census Bureau Geocoding API](https://geocoding.geo.census.gov/geocoder/).
Results are cached in a local SQLite database so that repeat lookups for the
same address do not make a network call.

## Installation

Requires Python 3.9+.

**Linux/macOS**
```bash
git clone https://github.com/philhanna/geocode.git
cd geocode
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

**Windows**
```bat
git clone https://github.com/philhanna/geocode.git
cd geocode
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Configuration

The application looks for its config file in a platform-specific location:

| Platform | Default config path |
|----------|-------------------|
| Linux/macOS | `~/.config/geocode/config.yaml` |
| Windows | `%APPDATA%\geocode\config.yaml` |

**Linux/macOS**
```bash
mkdir -p ~/.config/geocode
cp sample_config.yaml ~/.config/geocode/config.yaml
```

**Windows**
```bat
mkdir "%APPDATA%\geocode"
copy sample_config.yaml "%APPDATA%\geocode\config.yaml"
```

Edit the file to set the path where the cache database should be stored:

**Linux/macOS**
```yaml
cache:
  db_path: ~/.local/share/geocode/cache.db
```

**Windows**
```yaml
cache:
  db_path: ~\AppData\Local\geocode\cache.db
```

The database file and its parent directory are created automatically on first
use.

## Usage

### Command line

**Linux/macOS**
```bash
./geocode "1600 Pennsylvania Ave NW, Washington, DC"
(38.8987, -77.0366)
```

**Windows**
```bat
geocode.bat "1600 Pennsylvania Ave NW, Washington, DC"
(38.8987, -77.0366)
```

Use `--verbose` (or `-v`) to see whether the result was served from the local
cache or fetched from the API:

```
./geocode -v "1600 Pennsylvania Ave NW, Washington, DC"
(38.8987, -77.0366)  [API]

./geocode -v "1600 Pennsylvania Ave NW, Washington, DC"
(38.8987, -77.0366)  [cache]
```

On error the script exits with status code 1, making it safe to use in shell
pipelines.

### Python API

```python
from geocode import geocode, GeocodeError

try:
    lat, lon = geocode("7500 Cadbury Ct, Raleigh, NC")
    print(f"Latitude: {lat}, Longitude: {lon}")
except GeocodeError as e:
    print(f"Error: {e}")
```

## Cache

Results are stored in the SQLite database configured under `cache.db_path`.
You can inspect the cache directly:

**Linux/macOS**
```bash
sqlite3 ~/.local/share/geocode/cache.db \
  "SELECT address, latitude, longitude FROM geocode_cache;"
```

**Windows**
```bat
sqlite3 "%LOCALAPPDATA%\geocode\cache.db" "SELECT address, latitude, longitude FROM geocode_cache;"
```
