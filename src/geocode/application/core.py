from typing import Tuple

from ..ports import GeocodeCachePort, GeocoderPort


class GeocodeError(Exception):
    """Raised when an address cannot be geocoded."""


def geocode(
    address: str,
    cache: GeocodeCachePort,
    geocoder: GeocoderPort,
) -> Tuple[float, float]:
    """
    Geocode an address using the given cache and geocoder ports.

    Returns:
        (latitude, longitude)

    Raises:
        GeocodeError: if the address is blank, not found, or the geocoder fails.
    """
    if not address or not address.strip():
        raise GeocodeError("Address is blank.")

    normalized = address.strip()

    result = cache.lookup(normalized)
    if result is not None:
        return result

    latitude, longitude, jsonstring = geocoder.geocode(normalized)
    cache.store(normalized, latitude, longitude, jsonstring)
    return (latitude, longitude)
