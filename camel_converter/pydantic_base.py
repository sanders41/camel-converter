try:
    from pydantic import BaseModel  # type: ignore
except ImportError:
    raise ImportError("camel-converter must be installed with the pydantic extra to use this class")

from camel_converter import to_camel


class CamelBase(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
