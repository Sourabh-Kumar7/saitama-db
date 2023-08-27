from saitamadb.core.db import SaitamaDb

# define the schema for the DB
db_schema = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int", "required": True},
    "place": {"type": "str", "default": "canada"}
}

# initialize the db
db = SaitamaDb(db_name="sourabh-db", schema=db_schema)

db.add([
    {"name": "sourabh", "age": 24},
    {"name": "sneha", "age": 24, "place": "boston"}
])

db.commit()
