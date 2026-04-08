from abc import ABC, abstractmethod
from typing import Optional, Tuple


class GeocodeCachePort(ABC):
    """Abstract port for a geocode result cache.

    Secondary (driven) port. Implementations persist and retrieve geocode
    results so that repeat lookups for the same address avoid unnecessary
    calls to an external geocoding service.
    """

    @abstractmethod
    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        """Return the cached coordinates for an address, if present.

        Args:
            address: The normalised address string to look up.

        Returns:
            ``(latitude, longitude)`` if the address is cached, else ``None``.
        """

    @abstractmethod
    def store(self, address: str, latitude: float, longitude: float, jsonstring: str) -> None:
        """Persist a geocode result.

        Args:
            address: The normalised address string.
            latitude: Latitude in decimal degrees.
            longitude: Longitude in decimal degrees.
            jsonstring: Full JSON response from the geocoding API as a string.
        """
