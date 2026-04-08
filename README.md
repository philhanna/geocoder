# Geocode

Converts a U.S. street address into latitude and longitude coordinates using
the [U.S. Census Bureau Geocoding API](https://geocoding.geo.census.gov/geocoder/).
Results are cached in a local SQLite database so that repeat lookups for the
same address do not make a network call.

## Installation

Requires Python 3.9+.

### As a standalone tool

**Linux/macOS**
```bash
git clone https://github.com/philhanna/geocoder.git
cd geocoder
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

**Windows**
```bat
git clone https://github.com/philhanna/geocoder.git
cd geocoder
python -m venv .venv
.venv\Scripts\activate.bat
pip install -e ".[dev]"
```

### As a library dependency

To use `geocoder` as a dependency in another project, install it directly from GitHub:

```bash
pip install git+https://github.com/philhanna/geocoder.git
```

Then call it from your code:

```python
from geocoder import geocode, GeocodeError

lat, lon = geocode("1600 Pennsylvania Ave NW, Washington, DC")
```

## Configuration

The application looks for its config file in a platform-specific location:

| Platform | Default config path |
|----------|-------------------|
| Linux/macOS | `~/.config/geocoder/config.yaml` |
| Windows | `%APPDATA%\geocoder\config.yaml` |

**Linux/macOS**
```bash
mkdir -p ~/.config/geocoder
cp sample_config.yaml ~/.config/geocoder/config.yaml
```

**Windows**
```bat
mkdir "%APPDATA%\geocoder"
copy sample_config.yaml "%APPDATA%\geocoder\config.yaml"
```

Edit the file to set the path where the cache database should be stored:

**Linux/macOS**
```yaml
cache:
  db_path: ~/.local/share/geocoder/cache.db
```

**Windows**
```yaml
cache:
  db_path: ~\AppData\Local\geocoder\cache.db
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
from geocoder import geocode, GeocodeError

try:
    lat, lon = geocode("123 Main St, Raleigh, NC")
    print(f"Latitude: {lat}, Longitude: {lon}")
except GeocodeError as e:
    print(f"Error: {e}")
```

## Cache

Results are stored in the SQLite database configured under `cache.db_path`.
You can inspect the cache using the `sqlite3` command-line tool:

- **Linux**: install via your package manager — `sudo apt install sqlite3` (Debian/Ubuntu) or `sudo dnf install sqlite` (Fedora/RHEL)
- **macOS**: included with the OS; also available via `brew install sqlite`
- **Windows**: download the precompiled binary from https://www.sqlite.org/download.html and add it to your `PATH`



**Linux/macOS**
```bash
sqlite3 ~/.local/share/geocoder/cache.db \
  "SELECT address, latitude, longitude FROM geocode_cache;"
```

**Windows**
```bat
sqlite3 "%LOCALAPPDATA%\geocoder\cache.db" "SELECT address, latitude, longitude FROM geocode_cache;"
```
