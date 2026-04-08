from typing import Tuple

import requests

from ..core import GeocodeError
from ..ports import GeocoderPort


class CensusGeocoderAdapter(GeocoderPort):
    _BASE_URL = (
        "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    )

    def geocode(self, address: str) -> Tuple[float, float]:
        params = {
            "address": address,
            "benchmark": "Public_AR_Current",
            "format": "json",
        }

        try:
            response = requests.get(self._BASE_URL, params=params, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            raise GeocodeError(f"Error calling Census geocoding API: {e}") from e

        try:
            payload = response.json()
        except ValueError as e:
            raise GeocodeError("Census API did not return valid JSON.") from e

        matches = payload.get("result", {}).get("addressMatches", [])
        if not matches:
            raise GeocodeError(f"Address not found: {address}")

        coords = matches[0].get("coordinates", {})
        longitude = coords.get("x")
        latitude = coords.get("y")

        if latitude is None or longitude is None:
            raise GeocodeError("Census API response did not include coordinates.")

        return (latitude, longitude)
