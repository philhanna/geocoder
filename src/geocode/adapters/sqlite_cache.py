import sqlite3
from typing import Optional, Tuple

from .. import config as geocode_config
from ..ports import GeocodeCachePort


class SqliteCacheAdapter(GeocodeCachePort):
    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = geocode_config.get_db_path()
        self._db_path = db_path
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
        with sqlite3.connect(self._db_path) as con:
            row = con.execute(
                "SELECT latitude, longitude FROM geocode_cache WHERE address = ?",
                (address,),
            ).fetchone()
        return (row[0], row[1]) if row else None

    def store(self, address: str, latitude: float, longitude: float, jsonstring: str) -> None:
        with sqlite3.connect(self._db_path) as con:
            con.execute(
                """
                INSERT OR REPLACE INTO geocode_cache (address, latitude, longitude, jsonstring)
                VALUES (?, ?, ?, ?)
                """,
                (address, latitude, longitude, jsonstring),
            )
