import argparse
import sys
from typing import Optional, Tuple

from geocoder import GeocodeError
from geocoder.adapters.census_geocoder_adapter import CensusGeocoderAdapter
from geocoder.adapters.sqlite_cache_adapter import SqliteCacheAdapter
from geocoder.application.core import geocode as _geocode
from geocoder.ports import GeocodeCachePort


class _TrackingCache(GeocodeCachePort):
    """Cache adapter wrapper that records whether the last lookup was a hit.

    Used by the CLI in verbose mode to report whether a result was served
    from the local cache or fetched from the geocoding API.
    """

    def __init__(self, inner: GeocodeCachePort) -> None:
        """Wrap an existing cache adapter.

        Args:
            inner: The cache adapter to delegate all operations to.
        """
        self._inner = inner
        self.hit = False

    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        """Delegate to the inner cache and record whether the lookup was a hit.

        Args:
            address: The normalised address string to look up.

        Returns:
            ``(latitude, longitude)`` if found, else ``None``.
        """
        result = self._inner.lookup(address)
        self.hit = result is not None
        return result

    def store(self, address: str, latitude: float, longitude: float, jsonstring: str) -> None:
        """Delegate storage to the inner cache adapter.

        Args:
            address: The normalised address string.
            latitude: Latitude in decimal degrees.
            longitude: Longitude in decimal degrees.
            jsonstring: Full JSON response from the geocoding API as a string.
        """
        self._inner.store(address, latitude, longitude, jsonstring)


def main() -> None:
    """Entry point for the geocode command-line interface.

    Parses command-line arguments, geocodes the given address, and prints
    the result as ``(latitude, longitude)``. With ``--verbose``, also prints
    whether the result was served from the local cache or the API.

    Exits with status code 1 if the address cannot be geocoded.
    """
    parser = argparse.ArgumentParser(description="Geocode an address.")
    parser.add_argument("address", help="Address to geocode")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show whether result came from cache or API")
    args = parser.parse_args()

    try:
        if args.verbose:
            cache = _TrackingCache(SqliteCacheAdapter())
            lat, lon = _geocode(args.address, cache, CensusGeocoderAdapter())
            source = "cache" if cache.hit else "API"
            print(f"({lat}, {lon})  [{source}]")
        else:
            from geocoder import geocode
            lat, lon = geocode(args.address)
            print(f"({lat}, {lon})")
    except GeocodeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
