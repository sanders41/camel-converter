import pytest

from camel_converter import to_camel, to_pascal, to_snake


@pytest.fixture(autouse=True)
def clear_cache():
    yield
    to_camel.cache_clear()
    to_snake.cache_clear()
    to_pascal.cache_clear()
