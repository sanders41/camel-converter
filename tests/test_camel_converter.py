import pytest

from camel_converter import to_camel, to_snake, to_upper_camel


def test_to_camel():
    test_str = "this_is_a_test"
    expected = "thisIsATest"

    assert to_camel(test_str) == expected


def test_to_upper_camel():
    test_str = "this_is_a_test"
    expected = "ThisIsATest"

    assert to_upper_camel(test_str) == expected


@pytest.mark.parametrize("test_str", ["thisIsATest", "ThisIsATest"])
def test_to_snake(test_str):
    expected = "this_is_a_test"

    assert to_snake(test_str) == expected
