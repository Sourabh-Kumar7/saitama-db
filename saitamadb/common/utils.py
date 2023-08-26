import os
import pickle
from pathlib import Path
from typing import Dict, Union

import pandas as pd

from saitamadb.common import params as db_params
from saitamadb.errors.schema_error import SchemaError

SchemaDictType = Dict[str, Dict[str, object]]


def get_db_path(db_name: str) -> str:
    """returns the absolute path of the DB"""
    # default = os.path.join(os.path.expanduser("~"), ".cache", "saitama-db")
    default = os.path.join(".", db_params.DB_NAME)
    db_directory = os.environ.get("SAITAMA_DB_PATH", default=default)

    return os.path.join(db_directory, db_name)


def validate_schema(schema: SchemaDictType) -> bool:
    """Check whether all the keys in schema are valid"""

    valid_field_property_keys = ["type", "required", "default"]

    for key, values in schema.items():
        if not isinstance(key, str):
            raise SchemaError(
                f"The type of the key must be 'str' not {type(key)!r}")

        if "type" not in values:
            raise SchemaError(
                f"The 'type' of the field {key!r} is not defined")

        if values["type"] not in ["int", "str", "bool", "float"]:
            raise SchemaError(
                "The value of 'type' must be any of ('int', 'str', 'bool') with quotes.")

        if not all([i in valid_field_property_keys for i in values]):
            raise SchemaError(
                f"The field properties must only include {valid_field_property_keys!r}")

        if "default" in values:
            if type(values["default"]).__name__ != values["type"]:
                raise SchemaError(
                    f"The type of 'default' must be {values['type']!r} for the field {key!r}")

        if "required" in values:
            if not isinstance(values["required"], bool):
                raise SchemaError(
                    f"The type of 'required' must be 'bool' not {type(values['required']).__name__!r}")

    return True


def create_db_folders(db_path: str) -> None:
    path = Path(db_path)
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)


def load_cached_schema(db_path: str) -> Union[SchemaDictType, None]:
    """Loads the existing schema, that was provided when the DB was created for the first time."""
    c_schema_path = os.path.join(db_path, "db.schema")

    if Path(c_schema_path).is_file():
        with open(c_schema_path, "rb") as f:
            return pickle.load(f)
    else:
        return None


def dump_cached_schema(db_path: str, schema: SchemaDictType) -> None:
    """Dumps the schema in a pickle form for later use"""
    c_schema_path = os.path.join(db_path, "db.schema")

    with open(c_schema_path, "wb") as f:
        pickle.dump(schema, f)


def load_db(db_path: str, db_name: str) -> Union[pd.DataFrame, None]:
    """loads the df from the pickle file"""
    path = os.path.join(db_path, f"{db_name}.db")
    if Path(path).is_file():
        return pd.read_pickle(path)
    else:
        return None
