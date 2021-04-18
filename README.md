# Camel Converter

[![CI Status](https://github.com/sanders41/camel-converter/workflows/CI/badge.svg?branch=main&event=push)](https://github.com/sanders41/camel-converter/actions?query=workflow%3CI+branch%3Amain+event%3Apush)
[![Coverage](https://codecov.io/github/sanders41/camel-converter/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/camel-converter)
[![PyPI version](https://badge.fury.io/py/camel-converter.svg)](https://badge.fury.io/py/camel-converter)

In JSON keys are frequently in camelCase format, while variable names in Python typically
snake_case. The purpose of this pacakgae is to help convert between the two formats.

## Usage

- To convert from camel case to snake case:

  ```py
  from camel_converter import to_snake

  snake = to_snake("myString")
  ```

  This will convert `myString` into `my_string`

- To convert from snake case to camel case:

  ```py
  from camel_converter import to_camel

  camel = to_camel("my_string")
  ```

  This will convert `my_string` into `myString`

- To convert from snake to upper camel case:

  ```py
  from camel_converter import to_upper_camel

  upper_camel = to_upper_camel("my_string")
  ```

  This will convert `my_string` into `MyString`

If you are using [Pydantic](https://pydantic-docs.helpmanual.io/), a common usage of Pydantic where
this package is useful is in [FastAPI](https://fastapi.tiangolo.com/) you can use this package in
your models to automatically do the conversion.

```py
from pydantic import BaseModel

from camel_converter import to_camel


class MyModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    my_field: str
```

With setting up your model in this way `myField` from the source, i.e. JSON data, will map to `my_field` in your model.

You can also setup a model to inherit the config settings from so the `class Config` does not have to be manually set on every model:

```py
from pydantic import BaseModel

from camel_converter import to_camel


class MyBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MyModel(MyBaseModel):
    my_field: str


class AnotherModel(MyBaseModel):
    another_field: int
```

## Contributing

If you are interesting in contributing to this project please see our [contributing guide](CONTRIBUTING.md)
