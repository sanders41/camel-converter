from __future__ import annotations

from re import findall


def to_camel(snake_string: str) -> str:
    words = _split_snake(snake_string)

    return words[0] + "".join(word.title() for word in words[1:])


def to_snake(camel_string: str) -> str:
    words = findall("[a-zA-Z][^A-Z]*", camel_string)

    return "_".join(word.lower() for word in words)


def to_upper_camel(snake_string: str) -> str:
    words = _split_snake(snake_string)

    return "".join(word.title() for word in words)


def _split_snake(snake_string: str) -> list[str]:
    return snake_string.split("_")
