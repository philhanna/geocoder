import pytest

from geocoder.adapters.geocode import _TrackingCache
from geocoder.adapters.sqlite_cache_adapter import SqliteCacheAdapter


@pytest.fixture()
def tracking_cache(tmp_path):
    inner = SqliteCacheAdapter(db_path=str(tmp_path / "test.db"))
    return _TrackingCache(inner)


def test_hit_is_false_after_miss(tracking_cache):
    tracking_cache.lookup("123 Main St")
    assert tracking_cache.hit is False


def test_hit_is_true_after_hit(tracking_cache):
    tracking_cache.store("123 Main St", 35.5, -78.5, "{}")
    tracking_cache.lookup("123 Main St")
    assert tracking_cache.hit is True


def test_hit_resets_to_false_on_subsequent_miss(tracking_cache):
    tracking_cache.store("123 Main St", 35.5, -78.5, "{}")
    tracking_cache.lookup("123 Main St")  # hit
    tracking_cache.lookup("456 Oak Ave")  # miss
    assert tracking_cache.hit is False
