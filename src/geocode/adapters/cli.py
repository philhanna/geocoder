import argparse
import sys
from typing import Optional, Tuple

from geocode import GeocodeError
from geocode.adapters.census_geocoder_adapter import CensusGeocoderAdapter
from geocode.adapters.sqlite_cache_adapter import SqliteCacheAdapter
from geocode.application.core import geocode as _geocode
from geocode.ports import GeocodeCachePort


class _TrackingCache(GeocodeCachePort):
    """Wraps a cache adapter and records whether the last lookup was a hit."""

    def __init__(self, inner: GeocodeCachePort) -> None:
        self._inner = inner
        self.hit = False

    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        result = self._inner.lookup(address)
        self.hit = result is not None
        return result

    def store(self, address: str, latitude: float, longitude: float, jsonstring: str) -> None:
        self._inner.store(address, latitude, longitude, jsonstring)


def main() -> None:
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
            from geocode import geocode
            lat, lon = geocode(args.address)
            print(f"({lat}, {lon})")
    except GeocodeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
