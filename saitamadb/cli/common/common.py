# the objective of this module it to house all the commonly used commands
# the user might user, like the creation, delete and the purge ...etc. to name a few
import os
from argparse import _SubParsersAction


def create_cmd(sub_parser: _SubParsersAction) -> None:
    create = sub_parser.add_parser("create")
    create.add_argument("name", type=str, help="The name of the DB")
    create.add_argument("schema", type=str,
                        help="The path to the schema with which to create the DB from (*.json)")
    create.add_argument("-d", type=str, nargs="?",
                        default=os.path.join(os.getcwd(), "saitama-db"),
                        help="The directory where all the DB's are stored.")


def purge_cmd(sub_parser: _SubParsersAction) -> None:
    purge = sub_parser.add_parser("purge")
    purge.add_argument("name", type=str, help="The name of the DB to purge.")
    purge.add_argument("-d", type=str, nargs="?",
                       default=os.path.join(os.getcwd(), "saitama-db"),
                       help="The directory where all the DB's are stored.")


def delete_cmd(sub_parser: _SubParsersAction) -> None:
    delete = sub_parser.add_parser("delete")
    delete.add_argument("name", type=str, help="The name of the DB to delete.")
    delete.add_argument("-d", type=str, nargs="?",
                        default=os.path.join(os.getcwd(), "saitama-db"),
                        help="The directory where all the DB's are stored.")


def add_common_cmds(sub_parser: _SubParsersAction) -> None:
    create_cmd(sub_parser)
    purge_cmd(sub_parser)
    delete_cmd(sub_parser)
