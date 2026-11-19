from __future__ import annotations

from collections.abc import Callable
from functools import cached_property, lru_cache, partial
from typing import Any, Self

from camel_converter._version import VERSION

__version__ = VERSION

_CONTAINERS = (dict, list, tuple)


class Converter:
    """Inheriting this class adds methods to convert class and instance variables."""

    def to_camel(self, *, preserve_leading_trailing_underscore: bool = False) -> dict[str, Any]:
        """Converts to the class and instance variables into a camel case dict.

        Args:
            preserve_leading_trailing_underscore:
                Whether to keep leading and trailing underscores. For example _my_variable would
                become _myVariable rather than MyVariable. Defaults to False.

        Returns:
            A dictionary with they class and instance variable namess converted from snake case to
            camel case.

        Examples
            >>> from camel_converter import Converter
            >>> class SomeClass(Converter):
            >>>     some_value = "some value"
            >>>
            >>>     def __init__(self) -> None:
            >>>         self.another_value = "another value"
            >>>
            >>> example = SomeClass()
            >>> print(example.to_camel())

            This will print `{"someValue": "some value", "anotherValue": "another value"}`
        """
        class_vars = {
            key: value
            for cls in reversed(type(self).__mro__)
            for key, value in cls.__dict__.items()
            if not key.startswith("_")
            and not callable(value)
            and not isinstance(value, (property, cached_property, classmethod, staticmethod))
        }

        return dict_to_camel(
            {**class_vars, **self.__dict__},
            preserve_leading_trailing_underscore=preserve_leading_trailing_underscore,
        )

    @classmethod
    def from_camel(
        cls, data: dict[str, Any], *, preserve_leading_trailing_underscore: bool = False
    ) -> Self:
        """Initialize a class with a dictionary of camel case variables.

        Args:
            data: The dictionary to convert
            preserve_leading_trailing_underscore:
                Whether to keep leading and trailing underscores. For example _myVariable would
                become _my_variable rather than my_variable. Defaults to False.

        Returns:
            An instance of the class

        Examples
            >>> from camel_converter import Converter
            >>> class SomeClass(Converter):
            >>>     def __init__(self, some_value: str) -> None:
            >>>         self.some_value = some_value
            >>>
            >>> example = SomeClass.from_camel({"someValue": "some value"})
            >>> print(example.some_value)

            This will print `some value`
        """
        return cls(
            **dict_to_snake(
                data, preserve_leading_trailing_underscore=preserve_leading_trailing_underscore
            )
        )


def dict_to_camel(
    data: dict[Any, Any], *, preserve_leading_trailing_underscore: bool = False
) -> dict[Any, Any]:
    """Converts dictionary keys from snake case to camel case.

    Only keys of type string are converted, any other type is left unchanged.

    Args:
        data:
            The dictionary to convert
        preserve_leading_trailing_underscore:
            Whether to keep leading and trailing underscores. For example _my_variable would
            become _myVariable rather than MyVariable. Defaults to False.

    Returns:
        A dictionary with they keys of type string converted from snake case to camel case

    Raises:
        TypeError: If data is not a dict
    """
    return _convert_dict(
        data,
        partial(
            to_camel, preserve_leading_trailing_underscore=preserve_leading_trailing_underscore
        ),
    )


def dict_to_snake(
    data: dict[Any, Any],
    *,
    treat_digits_as_capitals: bool = False,
    preserve_leading_trailing_underscore: bool = False,
) -> dict[Any, Any]:
    """Converts dictionary keys from camel case or pascal case to snake case.

    Only keys of type string are converted, any other type is left unchanged.

    Args:
        data:
            The dictionary to convert
        treat_digits_as_capitals:
            Whether to treat digits as capitals. For example myVariable2 would become my_variable_2
            rather than my_variable2.
        preserve_leading_trailing_underscore:
            Whether to keep leading and trailing underscores. For example _myVariable would
            become _my_variable rather than my_variable. Defaults to False.

    Returns:
        A dictionary with they keys of type string converted from camel case or pascal case to
        snake case

    Raises:
        TypeError: If data is not a dict
    """
    return _convert_dict(
        data,
        partial(
            to_snake,
            treat_digits_as_capitals=treat_digits_as_capitals,
            preserve_leading_trailing_underscore=preserve_leading_trailing_underscore,
        ),
    )


def dict_to_pascal(
    data: dict[Any, Any], *, preserve_leading_trailing_underscore: bool = False
) -> dict[Any, Any]:
    """Converts dictionary keys from snake case to pascal case.

    Only keys of type string are converted, any other type is left unchanged.

    Args:
        data:
            The dictionary to convert
        preserve_leading_trailing_underscore:
            Whether to keep leading and trailing underscores. For example _my_variable would
            become _MyVariable rather than MyVariable. Defaults to False.

    Returns:
        A dictionary with they keys of type string converted from snake case to pascal case

    Raises:
        TypeError: If data is not a dict
    """
    return _convert_dict(
        data,
        partial(
            to_pascal, preserve_leading_trailing_underscore=preserve_leading_trailing_underscore
        ),
    )


@lru_cache(maxsize=4096)
def to_camel(snake_string: str, *, preserve_leading_trailing_underscore: bool = False) -> str:
    """Converts a snake case string to camel case.

    Args:
        snake_string:
            String in snake case format. For example my_variable.
        preserve_leading_trailing_underscore:
            Whether to keep leading and trailing underscores. For example _my_variable would
            become _myVariable rather than MyVariable. Defaults to False.

    Returns:
        The string in camel case format. For example myVariable.
    """
    prefix, words, suffix = _split_snake(snake_string, preserve_leading_trailing_underscore)

    return prefix + words[0] + "".join(word.title() for word in words[1:]) + suffix


@lru_cache(maxsize=4096)
def to_snake(
    camel_string: str,
    *,
    treat_digits_as_capitals: bool = False,
    preserve_leading_trailing_underscore: bool = False,
) -> str:
    """Converts a camel case or pascal case string to snake case.

    Args:
        camel_string:
            String in camel case or pascal case format. For example myVariable.
        treat_digits_as_capitals:
            Whether to treat digits as capitals. For example myVariable2 would become my_variable_2
            rather than my_variable2.
        preserve_leading_trailing_underscore:
            Whether to keep leading and trailing underscores. For example _myVariable would
            become _my_variable rather than my_variable. Defaults to False.

    Returns:
        The string in snake case format. For example my_variable.
    """
    if not preserve_leading_trailing_underscore:
        return (
            "".join(
                f"_{c}" if c.isupper() or (treat_digits_as_capitals and c.isdigit()) else c
                for c in camel_string
            )
            .lstrip("_")
            .lower()
        )

    return "".join(
        f"_{c}"
        if i > 0
        and camel_string[i - 1] != "_"
        and (c.isupper() or (treat_digits_as_capitals and c.isdigit()))
        else c
        for i, c in enumerate(camel_string)
    ).lower()


@lru_cache(maxsize=4096)
def to_pascal(snake_string: str, *, preserve_leading_trailing_underscore: bool = False) -> str:
    """Converts a snake case string to pascal case.

    Args:
        snake_string:
            String in snake case format. For example my_variable.
        preserve_leading_trailing_underscore:
            Whether to keep leading and trailing underscores. For example _my_variable would
            become _MyVariable rather than MyVariable. Defaults to False.

    Returns:
        The string in pascal case format. For example MyVariable.
    """
    prefix, words, suffix = _split_snake(snake_string, preserve_leading_trailing_underscore)

    return prefix + "".join(word.title() for word in words) + suffix


def _split_snake(
    snake_string: str, preserve_leading_trailing_underscore: bool
) -> tuple[str, list[str], str]:
    if not preserve_leading_trailing_underscore:
        return "", snake_string.split("_"), ""

    core = snake_string.strip("_")
    prefix = snake_string[: len(snake_string) - len(snake_string.lstrip("_"))]
    suffix = snake_string[len(prefix) + len(core) :]
    return prefix, core.split("_"), suffix


def _convert_dict(data: dict[Any, Any], convert_key: Callable[[str], str]) -> dict[Any, Any]:
    if not isinstance(data, dict):
        raise TypeError(f"Expected a dict, got {type(data).__name__}")

    return _convert_value(data, convert_key)


def _convert_value(value: Any, convert_key: Callable[[str], str]) -> Any:
    if isinstance(value, dict):
        return {
            (convert_key(k) if isinstance(k, str) else k): (
                _convert_value(v, convert_key) if isinstance(v, _CONTAINERS) else v
            )
            for k, v in value.items()
        }

    if isinstance(value, list):
        return [_convert_value(v, convert_key) if isinstance(v, _CONTAINERS) else v for v in value]

    return tuple(
        [_convert_value(v, convert_key) if isinstance(v, _CONTAINERS) else v for v in value]
    )
