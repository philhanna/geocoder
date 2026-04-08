# geocoder
from typing import Tuple

from .adapters.census_geocoder_adapter import CensusGeocoderAdapter
from .adapters.sqlite_cache_adapter import SqliteCacheAdapter
from .application.core import GeocodeError
from .application.core import geocode as _geocode

__all__ = ["geocode", "GeocodeError"]


def geocode(address: str) -> Tuple[float, float]:
    """
    Geocode an address using the default SQLite cache and Census Bureau adapter.

    Returns:
        (latitude, longitude)

    Raises:
        GeocodeError: if the address is blank, not found, or the API fails.
    """
    return _geocode(address, SqliteCacheAdapter(), CensusGeocoderAdapter())
