import pytest

from camel_converter import to_camel, to_snake, to_upper_camel


@pytest.mark.parametrize(
    "test_str, expected_str",
    [("this_is_a_test", "thisIsATest"), ("this_is_a_12_test", "thisIsA12Test")],
)
def test_to_camel(test_str, expected_str):
    assert to_camel(test_str) == expected_str


@pytest.mark.parametrize(
    "test_str, expected_str",
    [("this_is_a_test", "ThisIsATest"), ("this_is_a_12_test", "ThisIsA12Test")],
)
def test_to_upper_camel(test_str, expected_str):
    assert to_upper_camel(test_str) == expected_str


@pytest.mark.parametrize(
    "test_str, expected_str",
    [
        ("thisIsATest", "this_is_a_test"),
        ("ThisIsATest", "this_is_a_test"),
        ("aTestWith12Number", "a_test_with_12_number"),
    ],
)
def test_to_snake(test_str, expected_str):
    assert to_snake(test_str) == expected_str
