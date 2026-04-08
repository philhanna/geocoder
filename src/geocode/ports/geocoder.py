from abc import ABC, abstractmethod
from typing import Tuple


class GeocoderPort(ABC):
    @abstractmethod
    def geocode(self, address: str) -> Tuple[float, float]:
        """Return (latitude, longitude) for the given address."""
