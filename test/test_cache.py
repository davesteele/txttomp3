
import pytest
import os
import cache


@pytest.fixture
def hash_dir(tmpdir):
    dir = os.path.join(str(tmpdir), "cache")
    cache.set_base_dir(dir)
    return dir


@pytest.fixture
def decorated(hash_dir):
    @cache.cache
    def func(arg):
        return arg

    return func


def test_hash_eq():
    assert(cache.get_hash('foo') == cache.get_hash('foo'))


def test_hash_ne():
    assert(cache.get_hash('foo') != cache.get_hash('bar'))


def test_multiple_keys():
    assert(cache.get_hash("foo", "bar") != cache.get_hash("foo", "foo"))


def test_hash_dir_fxt(hash_dir):
    assert("cache" in hash_dir)


def test_no_dir(hash_dir):
    assert(not os.path.exists(hash_dir))


def test_create_dir(hash_dir):
    cache.set_cache(b"xxx", "foo")
    assert(os.path.exists(hash_dir))


def test_retrieve(hash_dir):
    cache.set_cache(b"xxx", "foo")
    assert(cache.get_cache("foo") == b"xxx")


def test_miss(hash_dir):
    assert(cache.get_cache("foo") == None)


def test_decorator(decorated):
    assert(decorated(b"foo") == b"foo")


def test_decorator_twice(decorated):
    assert(decorated(b"foo") == b"foo")
    assert(decorated(b"foo") == b"foo")


def test_decorator_cache(decorated):
    decorated(b"foo")
    assert(cache.get_cache(b"foo") == b"foo")
