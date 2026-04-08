from abc import ABC, abstractmethod
from typing import Optional, Tuple


class GeocodeCachePort(ABC):
    @abstractmethod
    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        """Return (latitude, longitude) if cached, else None."""

    @abstractmethod
    def store(self, address: str, latitude: float, longitude: float) -> None:
        """Persist a geocode result."""


class GeocoderPort(ABC):
    @abstractmethod
    def geocode(self, address: str) -> Tuple[float, float]:
        """Return (latitude, longitude) for the given address."""
