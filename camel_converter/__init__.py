from __future__ import annotations

import re
from functools import lru_cache

to_camel_pattern = re.compile(r"([a-zA-Z][^A-Z0-9]*|[0-9]+)")


@lru_cache(maxsize=256)
def to_camel(snake_string: str) -> str:
    """Converts a snake case string to camel case.

    Args:
        snake_string: String in snake case format. For example my_variable.

    Returns:
        The string in camel case format. For example myVariable.
    """
    words = _split_snake(snake_string)

    return words[0] + "".join(word.title() for word in words[1:])


@lru_cache(maxsize=256)
def to_snake(camel_string: str) -> str:
    """Converts a camel case string to snake case.

    Args:
        camel_string: String in camel case format. For example myVariable.

    Returns:
        The string in snake case format. For example my_variable.
    """
    words = to_camel_pattern.findall(camel_string)

    return "_".join(word.lower() for word in words)


@lru_cache(maxsize=256)
def to_upper_camel(snake_string: str) -> str:
    """Converts a snake case string to camel case.

    Args:
        snake_string: String in snake case format. For example my_variable.

    Returns:
        The string in upper camel case format. For example MyVariable.
    """
    words = _split_snake(snake_string)

    return "".join(word.title() for word in words)


def _split_snake(snake_string: str) -> list[str]:
    return snake_string.split("_")
