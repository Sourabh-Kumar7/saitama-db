import argparse

from saitamadb.cli.common.common import add_common_cmds
from saitamadb.cli.common import utils as cli_utils


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")
    sub_parser = parser.add_subparsers(dest="sub_command")
    add_common_cmds(sub_parser)
    args = parser.parse_args()
    rv = cli_utils.cmd_parser(vars(args))

    return rv
