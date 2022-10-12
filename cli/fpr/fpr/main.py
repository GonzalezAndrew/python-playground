import argparse
import logging
import platform
import sys
from typing import Optional
from typing import Sequence

from fpr.commands.crawl import crawl
from fpr.error_handler import error_handler
from fpr.output import output

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("fpr.log")],
)

logger = logging.getLogger(__name__)


def __add_output_argument(parser: argparse.ArgumentParser) -> None:
    """
    Adds the output argument to the given parser.
    :param parser: The argparser to add the output argument to.
    :return: Nothing.
    :rtype: None
    """
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output file the report will be sent to.",
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    output(msg="Starting fpr tool.")

    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="fpr",
        description="A command line tool used to obtain permissions on a given path.",
    )

    subparser = parser.add_subparsers(dest="command")

    crawl_parser = subparser.add_parser("crawl")
    crawl_parser.add_argument(
        "-p",
        "--path",
        type=str,
        required=True,
        help="The path which will be traversed.",
    )
    __add_output_argument(crawl_parser)

    help = subparser.add_parser("help", help="Show the help for a specific command.")
    help.add_argument("help_cmd", nargs="?", help="Command to show help for.")

    if len(argv) == 0:
        parser.print_help()

    args = parser.parse_args(argv)

    if args.command == "help" and args.help_cmd:
        parser.parse_args([args.help_cmd, "--help"])
        return 0
    elif args.command == "help":
        parser.parse_args(["--help"])
        return 0

    with error_handler():
        if args.command == "crawl":
            output(msg="User selected crawl command.")
            return crawl(args)
        else:
            raise NotImplementedError(f"The command {args.command} is not implemented.")


if __name__ == "__main__":
    try:
        # for now this will stay here. fpr does not support windows but will eventaully
        uname = platform.uname()
        if uname.system in ("win-7", "win", "Windows"):
            output(
                msg=f"The fpr cli tool does not support the {uname.system} system.",
                logger=logger,
                lvl="error",
            )
            raise NotImplementedError(
                f"The fpr cli tool does not support the {uname.system} system.",
            )
        else:
            output(
                msg=f"The fpr cli tool is running on the {uname.system} platform.",
                logger=logger,
            )
    except Exception as e:
        raise e
    else:
        raise SystemExit(main())
