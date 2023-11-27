from warnings import warn

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
        # __version__ was added with Pydantic 2 so we know if this errors the version is < 2.
        # Still check the version as a fail safe incase __version__ gets added to verion 1.
        if int(pydantic.__version__[:1]) >= 2:  # type: ignore[attr-defined]
            model_config = pydantic.ConfigDict(alias_generator=to_camel, populate_by_name=True)  # type: ignore[attr-defined]
        else:  # pragma: no cover
            warn(
                "The use of Pydantic less than version 2 is depreciated and will be removed in a future release",
                DeprecationWarning,
            )

            # Raise an AttributeError to match the AttributeError on __version__ because in either
            # case we need to get to the same place.
            raise AttributeError
    except AttributeError:  # pragma: no cover

        class Config:
            alias_generator = to_camel
            allow_population_by_field_name = True
