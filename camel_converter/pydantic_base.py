try:
    import pydantic  # type: ignore
except ImportError:
    raise ImportError("camel-converter must be installed with the pydantic extra to use this class")

from camel_converter import to_camel


class CamelBase(pydantic.BaseModel):
    """A Pydantic model that provides a base configuration for conveting between camel and snake case.

    If another Pydantic model inherit from this class it will get the ability to do this conversion
    between camel and snake case without having to add the configuration to the new model.
    """

    try:
        # __version__ was added with Pydantic 2 so we know if this errors the version is < 2
        pydantic.__version__  # type: ignore[attr-defined]
        model_config = pydantic.ConfigDict(alias_generator=to_camel, populate_by_name=True)  # type: ignore[attr-defined]
    except AttributeError:  # pragma: no cover

        class Config:
            alias_generator = to_camel
            allow_population_by_field_name = True
