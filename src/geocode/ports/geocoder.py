from abc import ABC, abstractmethod
from typing import Tuple


class GeocoderPort(ABC):
    @abstractmethod
    def geocode(self, address: str) -> Tuple[float, float, str]:
        """Return (latitude, longitude, jsonstring) for the given address."""
