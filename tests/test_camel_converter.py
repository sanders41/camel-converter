import pytest

from camel_converter import (
    dict_to_camel,
    dict_to_pascal,
    dict_to_snake,
    to_camel,
    to_pascal,
    to_snake,
)


@pytest.mark.parametrize(
    "test_dict, expected",
    [
        (
            {"convert_me": "val 1", "me_also": "val 2", "unchanged": "val 3", 1: "val 4"},
            {"convertMe": "val 1", "meAlso": "val 2", "unchanged": "val 3", 1: "val 4"},
        ),
        (
            {
                "convert_me": "val 1",
                "me_also": {
                    "nested_convert": 1,
                    "unchanged": 2,
                    "another_nest": {"one_more": "hi"},
                },
                1: {"another_nested": "a"},
            },
            {
                "convertMe": "val 1",
                "meAlso": {
                    "nestedConvert": 1,
                    "unchanged": 2,
                    "anotherNest": {"oneMore": "hi"},
                },
                1: {"anotherNested": "a"},
            },
        ),
        (
            {"test_convert": [{"change_me": 1, "unchanged": 2}, 1]},
            {"testConvert": [{"changeMe": 1, "unchanged": 2}, 1]},
        ),
        (
            {"test_convert": ({"change_me": 1, "unchanged": 2}, 1)},
            {"testConvert": ({"changeMe": 1, "unchanged": 2}, 1)},
        ),
    ],
)
def test_dict_to_camel(test_dict, expected):
    assert dict_to_camel(test_dict) == expected


@pytest.mark.parametrize(
    "test_dict, expected",
    [
        (
            {"convertMe": "val 1", "meAlso": "val 2", "unchanged": "val 3", 1: "val 4"},
            {"convert_me": "val 1", "me_also": "val 2", "unchanged": "val 3", 1: "val 4"},
        ),
        (
            {
                "convertMe": "val 1",
                "meAlso": {"nestedConvert": 1, "unchanged": 2, "anotherNest": {"oneMore": "hi"}},
                1: {"anotherNested": "a"},
            },
            {
                "convert_me": "val 1",
                "me_also": {
                    "nested_convert": 1,
                    "unchanged": 2,
                    "another_nest": {"one_more": "hi"},
                },
                1: {"another_nested": "a"},
            },
        ),
        (
            {"testConvert": [{"changeMe": 1, "unchanged": 2}, 1]},
            {"test_convert": [{"change_me": 1, "unchanged": 2}, 1]},
        ),
        (
            {"testConvert": ({"changeMe": 1, "unchanged": 2}, 1)},
            {"test_convert": ({"change_me": 1, "unchanged": 2}, 1)},
        ),
    ],
)
def test_dict_to_snake(test_dict, expected):
    assert dict_to_snake(test_dict) == expected


@pytest.mark.parametrize(
    "test_dict, expected",
    [
        (
            {"convert_me": "val 1", "me_also": "val 2", "changed": "val 3", 1: "val 4"},
            {"ConvertMe": "val 1", "MeAlso": "val 2", "Changed": "val 3", 1: "val 4"},
        ),
        (
            {
                "convert_me": "val 1",
                "me_also": {
                    "nested_convert": 1,
                    "changed": 2,
                    "another_nest": {"one_more": "hi"},
                },
                1: {"another_nested": "a"},
            },
            {
                "ConvertMe": "val 1",
                "MeAlso": {
                    "NestedConvert": 1,
                    "Changed": 2,
                    "AnotherNest": {"OneMore": "hi"},
                },
                1: {"AnotherNested": "a"},
            },
        ),
        (
            {"test_convert": [{"change_me": 1, "changed": 2}, 1]},
            {"TestConvert": [{"ChangeMe": 1, "Changed": 2}, 1]},
        ),
        (
            {"test_convert": ({"change_me": 1, "changed": 2}, 1)},
            {"TestConvert": ({"ChangeMe": 1, "Changed": 2}, 1)},
        ),
    ],
)
def test_dict_to_pascal(test_dict, expected):
    assert dict_to_pascal(test_dict) == expected


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
def test_to_pascal(test_str, expected_str):
    assert to_pascal(test_str) == expected_str


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
