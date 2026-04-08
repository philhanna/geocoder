from typing import Optional, Tuple

import pytest

from geocoder.application.core import GeocodeError, geocode
from geocoder.ports import GeocodeCachePort, GeocoderPort


class StubCache(GeocodeCachePort):
    def __init__(self):
        self._data = {}

    def lookup(self, address: str) -> Optional[Tuple[float, float]]:
        return self._data.get(address)

    def store(self, address: str, latitude: float, longitude: float, jsonstring: str) -> None:
        self._data[address] = (latitude, longitude)


class StubGeocoder(GeocoderPort):
    def __init__(self, result: Tuple[float, float, str] = (35.5, -78.5, "{}")):
        self._result = result
        self.call_count = 0

    def geocode(self, address: str) -> Tuple[float, float, str]:
        self.call_count += 1
        return self._result


def test_blank_address_raises():
    with pytest.raises(GeocodeError):
        geocode("", StubCache(), StubGeocoder())


def test_whitespace_only_address_raises():
    with pytest.raises(GeocodeError):
        geocode("   ", StubCache(), StubGeocoder())


def test_cache_hit_returns_cached_result_without_calling_geocoder():
    cache = StubCache()
    cache.store("123 Main St", 35.5, -78.5, "{}")
    geocoder = StubGeocoder(result=(99.0, 99.0, "{}"))

    result = geocode("123 Main St", cache, geocoder)

    assert result == (35.5, -78.5)
    assert geocoder.call_count == 0


def test_cache_miss_calls_geocoder_and_returns_coordinates():
    cache = StubCache()
    geocoder = StubGeocoder(result=(35.5, -78.5, "{}"))

    result = geocode("123 Main St", cache, geocoder)

    assert result == (35.5, -78.5)
    assert geocoder.call_count == 1


def test_cache_miss_stores_result_for_subsequent_lookup():
    cache = StubCache()
    geocoder = StubGeocoder(result=(35.5, -78.5, "{}"))

    geocode("123 Main St", cache, geocoder)

    assert cache.lookup("123 Main St") == (35.5, -78.5)


def test_address_is_stripped_before_cache_lookup():
    cache = StubCache()
    cache.store("123 Main St", 35.5, -78.5, "{}")
    geocoder = StubGeocoder(result=(99.0, 99.0, "{}"))

    result = geocode("  123 Main St  ", cache, geocoder)

    assert result == (35.5, -78.5)
    assert geocoder.call_count == 0
