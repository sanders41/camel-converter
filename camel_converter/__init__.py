from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache, partial
from typing import TYPE_CHECKING, Any

from camel_converter._version import VERSION

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

__version__ = VERSION


class Converter:
    """Inheriting this class adds methods to convert class and instance variables."""

    def to_camel(self) -> dict[str, Any]:
        """Converts to the class and instance variables into a camel case dict.

        Returns:
            A dictionary with they class and instance variable namess converted from snake case to
            camel case.

        Examples
            >>> from camel_converrter import Converter
            >>> class SomeClass(Converter):
            >>>     some_value = "some value"
            >>>
            >>>     def __init__(self) -> None:
            >>>         self.another_value = "another value"
            >>>
            >>> example = SomeClass()
            >>> print(example)

            This will print `{"someValue": "some value", "anotherValue": "another value"}`
        """
        class_vars = {
            key: value
            for key, value in self.__class__.__dict__.items()
            if not key.startswith("_") and not callable(value)
        }

        return dict_to_camel({**class_vars, **self.__dict__})

    @classmethod
    def from_camel(cls, data: dict[str, Any]) -> Self:
        """Initialize a class with a dictionary of camel case variables.

        Args:
            data: The dictionary to convert

        Returns:
            An instance of the class

        Examples
            >>> from camel_converrter import Converter
            >>> class SomeClass(Converter):
            >>>     def __init__(self, some_value: str) -> None:
            >>>         self.some_value = "some value"
            >>>
            >>> example = SomeClass.from_camel({"someValue": "some value"})
            >>> print(example.some_value)

            This will print `some value`
        """
        return cls(**dict_to_snake(data))


def dict_to_camel(data: dict[Any, Any]) -> dict[Any, Any]:
    """Converts dictionary keys from snake case to camel case.

    Only keys of type string are converted, any other type is left unchanged.

    Args:
        data: The dictionary to convert

    Returns:
        A dictionary with they keys of type string converted from snake case to camel case

    Raises:
        TypeError: If data is not a dict
    """
    return _convert_dict(data, to_camel)


def dict_to_snake(
    data: dict[Any, Any], *, treat_digits_as_capitals: bool = False
) -> dict[Any, Any]:
    """Converts dictionary keys from camel case or pascal case to snake case.

    Only keys of type string are converted, any other type is left unchanged.

    Args:
        data:
            The dictionary to convert
        treat_digits_as_capitals:
            Whether to treat digits as capitals. For example myVariable2 would become my_variable_2
            rather than my_variable2.

    Returns:
        A dictionary with they keys of type string converted from camel case or pascal case to
        snake case

    Raises:
        TypeError: If data is not a dict
    """
    return _convert_dict(data, partial(to_snake, treat_digits_as_capitals=treat_digits_as_capitals))


def dict_to_pascal(data: dict[Any, Any]) -> dict[Any, Any]:
    """Converts dictionary keys from snake case to pascal case.

    Only keys of type string are converted, any other type is left unchanged.

    Args:
        data: The dictionary to convert

    Returns:
        A dictionary with they keys of type string converted from snake case to pascal case

    Raises:
        TypeError: If data is not a dict
    """
    return _convert_dict(data, to_pascal)


@lru_cache(maxsize=4096)
def to_camel(snake_string: str) -> str:
    """Converts a snake case string to camel case.

    Args:
        snake_string: String in snake case format. For example my_variable.

    Returns:
        The string in camel case format. For example myVariable.
    """
    words = _split_snake(snake_string)

    return words[0] + "".join(word.title() for word in words[1:])


@lru_cache(maxsize=4096)
def to_snake(camel_string: str, *, treat_digits_as_capitals: bool = False) -> str:
    """Converts a camel case or pascal case string to snake case.

    Args:
        camel_string:
            String in camel case or pascal case format. For example myVariable.
        treat_digits_as_capitals:
            Whether to treat digits as capitals. For example myVariable2 would become my_variable_2
            rather than my_variable2.

    Returns:
        The string in snake case format. For example my_variable.
    """

    def check_character(c: str) -> str:
        if c.isupper() or (treat_digits_as_capitals and c.isdigit()):
            return f"_{c}"
        else:
            return c

    return "".join(check_character(c) for c in camel_string).lstrip("_").lower()


@lru_cache(maxsize=4096)
def to_pascal(snake_string: str) -> str:
    """Converts a snake case string to pascal case.

    Args:
        snake_string: String in snake case format. For example my_variable.

    Returns:
        The string in pascal case format. For example MyVariable.
    """
    words = _split_snake(snake_string)

    return "".join(word.title() for word in words)


def _split_snake(snake_string: str) -> list[str]:
    return snake_string.split("_")


def _convert_dict(data: dict[Any, Any], convert_key: Callable[[str], str]) -> dict[Any, Any]:
    if not isinstance(data, dict):
        raise TypeError(f"Expected a dict, got {type(data).__name__}")

    return _convert_value(data, convert_key)


def _convert_value(value: Any, convert_key: Callable[[str], str]) -> Any:
    if isinstance(value, dict):
        return {
            (convert_key(k) if isinstance(k, str) else k): _convert_value(v, convert_key)
            for k, v in value.items()
        }

    if isinstance(value, list):
        return [_convert_value(v, convert_key) for v in value]

    if isinstance(value, tuple):
        return tuple([_convert_value(v, convert_key) for v in value])

    return value
