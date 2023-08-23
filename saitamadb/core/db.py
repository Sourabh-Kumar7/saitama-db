from typing import Optional, Dict

import pandas as pd

from saitamadb.common import utils as db_utils
from saitamadb.errors.schema_error import SchemaError


# types
SchemaDictType = Dict[str, Dict[str, object]]


class SaitamaDb:
    """The main API for the DB"""

    def __init__(self, db_name: str, schema: Optional[SchemaDictType] = None,
                 db_path: Optional[str] = None, allow_data_duplication: bool = False,
                 in_memory: bool = False) -> None:

        self._db_name = db_name
        self._schema = schema
        self._data_dupe = allow_data_duplication
        self._in_memory = in_memory

        # db variables
        self._db: pd.DataFrame = None
        self._db_path: str = db_utils.get_db_path(db_name)

        if db_path:
            self._db_path = f"{db_path}/{self._db_name}"

        # validate the user defined schema
        self._validate_schema()

        # meta data about the db
        if self._schema:
            self._columns = list(self._schema.keys())

        # start the loading sequence
        self._load_initial_schema()
        self._reload_db()

    def _validate_schema(self) -> None:
        if self._schema:
            db_utils.validate_schema(self._schema)

    def _load_initial_schema(self) -> None:
        """Loads the schema that was provided when the DB was created for the first time"""
        if not self._in_memory:
            db_utils.create_db_folders(self._db_path)
        if not self._in_memory:
            schema = db_utils.load_cached_schema(self._db_path)
        else:
            schema = None
        if schema:
            if self._schema:
                if not schema == self._schema:
                    raise SchemaError(
                        "The schema provided does not match with the initial schema")
            else:
                self._schema = schema.copy()
                self._columns = list(self._schema.keys())
        else:
            if not self._schema:
                raise SchemaError("The schema is not provided")
            else:
                if not self._in_memory:
                    db_utils.dump_cached_schema(self._db_path, self._schema)
