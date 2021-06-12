# Camel Converter

[![CI Status](https://github.com/sanders41/camel-converter/workflows/CI/badge.svg?branch=main&event=push)](https://github.com/sanders41/camel-converter/actions?query=workflow%3CI+branch%3Amain+event%3Apush)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/camel-converter/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/camel-converter/main)
[![Coverage](https://codecov.io/github/sanders41/camel-converter/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/camel-converter)
[![PyPI version](https://badge.fury.io/py/camel-converter.svg)](https://badge.fury.io/py/camel-converter)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camel-converter?color=5cc141)](https://github.com/sanders41/camel-converter)

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

### Optional Extras

An optional extra is provided for [Pydantic](https://pydantic-docs.helpmanual.io/) that provides a
base class to automatically convert between snake case and camel case. To use this Pydantic class
install camel converter with:

```sh
pip install camel-converter[pydantic]
```

Then your Pydantic classes can inherit from CamelBase.

```py
from camel_converter.pydantic_base import CamelBase


class MyModel(CamelBase):
    test_field: str


my_data = MyModel(**{"testField": "my value"})
print(my_data.test_field)
```

will result in `my value` being printed.

With setting up your model in this way `myField` from the source, i.e. JSON data, will map to `my_field` in your model.

## Contributing

If you are interesting in contributing to this project please see our [contributing guide](CONTRIBUTING.md)
