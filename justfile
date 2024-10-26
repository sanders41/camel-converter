@_default:
  just --list

@lint:
  echo mypy
  just --justfile {{justfile()}} mypy
  echo ruff-check
  just --justfile {{justfile()}} ruff-check
  echo ruff-format
  just --justfile {{justfile()}} ruff-format

@mypy:
  uv run mypy camel_converter tests

@ruff-check:
  uv run ruff check camel_converter tests

@ruff-format:
  uv run ruff format camel_converter tests

@test *args="":
  -uv run pytest {{args}}

@install:
  uv sync --frozen --all-extras

@lock:
  uv lock
