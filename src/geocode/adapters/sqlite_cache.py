# geocode.adapters.sqlite_cache
import sqlite3
from typing import Optional, Tuple

from ..ports import GeocodeCachePort


class SqliteCacheAdapter(GeocodeCachePort):
    def __init__(self, db_path: str = "geocode_cache.db") -> None:
        self._db_path = db_path
        with sqlite3.connect(self._db_path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS geocode_cache (
                    address TEXT PRIMARY KEY,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )
                """
            )

    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        with sqlite3.connect(self._db_path) as con:
            row = con.execute(
                "SELECT latitude, longitude FROM geocode_cache WHERE address = ?",
                (address,),
            ).fetchone()
        return (row[0], row[1]) if row else None

    def store(self, address: str, latitude: float, longitude: float) -> None:
        with sqlite3.connect(self._db_path) as con:
            con.execute(
                """
                INSERT OR REPLACE INTO geocode_cache (address, latitude, longitude)
                VALUES (?, ?, ?)
                """,
                (address, latitude, longitude),
            )
