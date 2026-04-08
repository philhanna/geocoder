import sqlite3

import pytest

from geocoder.adapters.sqlite_cache_adapter import SqliteCacheAdapter


@pytest.fixture()
def cache(tmp_path):
    return SqliteCacheAdapter(db_path=str(tmp_path / "test.db"))


def test_lookup_miss(cache):
    assert cache.lookup("123 Main St") is None


def test_lookup_hit_after_store(cache):
    cache.store("123 Main St", 35.5, -78.5, '{"result": {}}')
    assert cache.lookup("123 Main St") == (35.5, -78.5)


def test_store_overwrites_existing_entry(cache):
    cache.store("123 Main St", 35.5, -78.5, '{"result": {}}')
    cache.store("123 Main St", 36.0, -79.0, '{"result": "updated"}')
    assert cache.lookup("123 Main St") == (36.0, -79.0)


def test_migration_adds_jsonstring_column(tmp_path):
    db_path = str(tmp_path / "old.db")
    with sqlite3.connect(db_path) as con:
        con.execute(
            """
            CREATE TABLE geocode_cache (
                address TEXT PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
            """
        )
        con.execute(
            "INSERT INTO geocode_cache VALUES (?, ?, ?)",
            ("123 Main St", 35.5, -78.5),
        )

    cache = SqliteCacheAdapter(db_path=db_path)

    assert cache.lookup("123 Main St") == (35.5, -78.5)
    cache.store("456 Oak Ave", 36.0, -79.0, '{"result": {}}')
    assert cache.lookup("456 Oak Ave") == (36.0, -79.0)
