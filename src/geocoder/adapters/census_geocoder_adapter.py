import json
from typing import Tuple

import requests

from ..application.core import GeocodeError
from ..ports import GeocoderPort


class CensusGeocoderAdapter(GeocoderPort):
    """Geocoder adapter backed by the U.S. Census Bureau Geocoding API.

    Implements :class:`GeocoderPort` by calling the Census Bureau's
    one-line address geocoding endpoint. Returns coordinates together with
    the full API response payload for storage in the cache.

    Reference: https://geocoding.geo.census.gov/geocoder/
    """

    _BASE_URL = (
        "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    )

    def geocode(self, address: str) -> Tuple[float, float, str]:
        """Resolve an address to coordinates using the Census geocoding API.

        Args:
            address: The normalised address string to geocode.

        Returns:
            A three-tuple of ``(latitude, longitude, jsonstring)`` where
            ``jsonstring`` is the full API response serialised as JSON.

        Raises:
            GeocodeError: if the HTTP request fails, the response is not valid
                JSON, no address matches are returned, or coordinates are
                missing from the response.
        """
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

        return (latitude, longitude, json.dumps(payload))
