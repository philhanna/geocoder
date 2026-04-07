import sqlite3
from typing import Tuple
from urllib.parse import urlencode

import requests


class GeocodeError(Exception):
    """Raised when an address cannot be geocoded."""


def geocode(address: str) -> Tuple[float, float]:
    """
    Geocode an address using a local SQLite cache first, then the U.S. Census
    Bureau Geocoding API if needed.

    Returns:
        (latitude, longitude)

    Raises:
        GeocodeError: if the address is blank, not found, or the API fails.
    """
    if not address or not address.strip():
        raise GeocodeError("Address is blank.")

    normalized_address = address.strip()
    db_path = "geocode_cache.db"

    # 1. Look in cache
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS geocode_cache (
                address TEXT PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
            """
        )
        conn.commit()

        row = conn.execute(
            """
            SELECT latitude, longitude
            FROM geocode_cache
            WHERE address = ?
            """,
            (normalized_address,),
        ).fetchone()

        if row is not None:
            latitude, longitude = row
            return (latitude, longitude)

        # 2. Not in cache: call Census API
        base_url = (
            "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
        )
        params = {
            "address": normalized_address,
            "benchmark": "Public_AR_Current",
            "format": "json",
        }

        try:
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            raise GeocodeError(f"Error calling Census geocoding API: {e}") from e

        try:
            payload = response.json()
        except ValueError as e:
            raise GeocodeError("Census API did not return valid JSON.") from e

        matches = payload.get("result", {}).get("addressMatches", [])
        if not matches:
            raise GeocodeError(f"Address not found: {normalized_address}")

        first_match = matches[0]
        coords = first_match.get("coordinates", {})
        longitude = coords.get("x")
        latitude = coords.get("y")

        if latitude is None or longitude is None:
            raise GeocodeError("Census API response did not include coordinates.")

        # 3. Store in cache
        conn.execute(
            """
            INSERT OR REPLACE INTO geocode_cache (address, latitude, longitude)
            VALUES (?, ?, ?)
            """,
            (normalized_address, latitude, longitude),
        )
        conn.commit()

        return (latitude, longitude)

    finally:
        conn.close()
