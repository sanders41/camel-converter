import sys
from concurrent.futures import ThreadPoolExecutor
from importlib import reload
from unittest.mock import patch

import pytest

from camel_converter.pydantic_base import CamelBase


def test_camel_config():
    class Test(CamelBase):
        test_field: str

    got = Test(**{"testField": "test"})

    assert got.model_dump() == {"test_field": "test"}


def test_camel_config_missing_import():
    with patch.dict(sys.modules, {"pydantic": None}):
        with pytest.raises(ImportError):
            reload(sys.modules["camel_converter.pydantic_base"])


def test_camel_config_threaded():
    if not hasattr(sys, "_is_gil_enabled") or sys._is_gil_enabled():
        pytest.skip("Free-threading is not enabled")

    class Test(CamelBase):
        test_field: str

    def populate(values: dict) -> Test:
        return Test(**values)

    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(populate, {"testField": "value 1"})
        future2 = executor.submit(populate, {"testField": "value 2"})

        result1 = future1.result()
        result2 = future2.result()

    assert result1.model_dump() == {"test_field": "value 1"}
    assert result2.model_dump() == {"test_field": "value 2"}
