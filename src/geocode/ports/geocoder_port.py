from abc import ABC, abstractmethod
from typing import Tuple


class GeocoderPort(ABC):
    """Abstract port for a geocoding service.

    Secondary (driven) port. Implementations resolve a free-text address to
    geographic coordinates by calling an external geocoding API or service.
    """

    @abstractmethod
    def geocode(self, address: str) -> Tuple[float, float, str]:
        """Resolve an address to geographic coordinates.

        Args:
            address: The normalised address string to geocode.

        Returns:
            A three-tuple of ``(latitude, longitude, jsonstring)`` where
            ``jsonstring`` is the full API response serialised as JSON.

        Raises:
            GeocodeError: if the address cannot be resolved or the service
                returns an unexpected response.
        """
