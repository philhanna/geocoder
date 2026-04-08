import sqlite3
from pathlib import Path
from typing import Optional, Tuple

from .. import config as geocode_config
from ..ports import GeocodeCachePort


class SqliteCacheAdapter(GeocodeCachePort):
    """Cache adapter backed by a local SQLite database.

    Implements :class:`GeocodeCachePort` using a single SQLite table,
    ``geocode_cache``. The database file path is read from the application
    config if not supplied explicitly.

    The table is created on first use. Existing databases that pre-date the
    ``jsonstring`` column are migrated automatically via ``ALTER TABLE``.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialise the adapter and ensure the database schema exists.

        Args:
            db_path: Path to the SQLite database file. Supports ``~``
                expansion. If ``None``, the path is read from the application
                config via :func:`geocode.config.get_db_path`.
        """
        if db_path is None:
            db_path = geocode_config.get_db_path()
        self._db_path = str(Path(db_path).expanduser())
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._db_path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS geocode_cache (
                    address TEXT PRIMARY KEY,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    jsonstring TEXT
                )
                """
            )
            try:
                con.execute(
                    "ALTER TABLE geocode_cache ADD COLUMN jsonstring TEXT"
                )
            except sqlite3.OperationalError:
                pass  # column already exists

    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        """Return cached coordinates for an address, if present.

        Args:
            address: The normalised address string to look up.

        Returns:
            ``(latitude, longitude)`` if found in the cache, else ``None``.
        """
        with sqlite3.connect(self._db_path) as con:
            row = con.execute(
                "SELECT latitude, longitude FROM geocode_cache WHERE address = ?",
                (address,),
            ).fetchone()
        return (row[0], row[1]) if row else None

    def store(self, address: str, latitude: float, longitude: float, jsonstring: str) -> None:
        """Persist a geocode result, replacing any existing entry.

        Args:
            address: The normalised address string.
            latitude: Latitude in decimal degrees.
            longitude: Longitude in decimal degrees.
            jsonstring: Full JSON response from the geocoding API as a string.
        """
        with sqlite3.connect(self._db_path) as con:
            con.execute(
                """
                INSERT OR REPLACE INTO geocode_cache (address, latitude, longitude, jsonstring)
                VALUES (?, ?, ?, ?)
                """,
                (address, latitude, longitude, jsonstring),
            )
