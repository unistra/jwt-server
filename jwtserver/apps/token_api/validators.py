import json
from pathlib import PosixPath
from typing import TypeVar

from django.conf import settings
from django.core.exceptions import ValidationError
from jsonschema.exceptions import ValidationError as SchemaValidationError
from jsonschema.validators import validate

T = TypeVar("T")


class JSONSchemaValidator:
    schema: PosixPath

    def __init__(self, schema: str):
        self.schema = schema

    def __call__(self, value: T) -> T:
        with open(settings.JSONSCHEMA_ROOT / self.schema) as schema_file:
            schema = json.load(schema_file)
            try:
                validate(value, schema=schema)
            except SchemaValidationError as err:
                raise ValidationError("JSON Schema validation error\n" + str(err))
        return value
