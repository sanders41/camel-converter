try:
    from pydantic import BaseModel  # type: ignore
except ImportError:
    raise ImportError("camel-converter must be installed with the pydantic extra to use this class")

from camel_converter import to_camel


class CamelBase(BaseModel):
    """A Pydantic model that provides a base configuration for conveting between camel and snake case.

    If another Pydantic model inherit from this class it will get the ability to do this conversion
    between camel and snake case without having to add the configuration to the new model.
    """

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
