import sys
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
