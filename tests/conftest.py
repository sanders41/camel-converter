import pytest

from camel_converter import to_camel, to_snake, to_upper_camel


@pytest.fixture(autouse=True)
def clear_cache():
    yield
    to_camel.cache_clear()
    to_snake.cache_clear()
    to_upper_camel.cache_clear()
