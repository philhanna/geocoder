from abc import ABC, abstractmethod
from typing import Optional, Tuple


class GeocodeCachePort(ABC):
    @abstractmethod
    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        """Return (latitude, longitude) if cached, else None."""

    @abstractmethod
    def store(self, address: str, latitude: float, longitude: float, jsonstring: str) -> None:
        """Persist a geocode result."""
