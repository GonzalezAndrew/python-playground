import argparse
import json
import logging
import os
import stat
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from fpr.output import output

logger = logging.getLogger(__name__)


class Report:
    """Container class for aggregating all data."""

    def __init__(self, path: str) -> None:
        self._results = {
            "inital_path": path,
            "results": [],
        }  # type: Dict[str, str, List[Any]]


def __check_permissions(file: str) -> Dict[str, Union[str, bool]]:
    """A function which checks the file permissions of a given file and returns the output.
    :param file: The file which will have its permissions checked.
    :return: A dictonary containing data on the files permissions.
    :rtype: dict{str}
    """

    # ALL_R = (stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    # ALL_W = (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    # ALL_OTHER = (stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)

    mode = os.stat(file).st_mode

    results = {"filename": file}  # type: Dict[str, Union[str, bool]]
    results["is_directory"] = True if stat.S_ISDIR(mode) != 0 else False

    output(msg=f"Checking permissions for the file {file}", logger=logger, lvl="info")

    if mode & stat.S_IROTH:
        output(
            msg=f"all users has read access on the file. {file}",
            logger=logger,
            lvl="info",
        )
        results["allusers_read_access"] = True
    else:
        results["allusers_read_access"] = False

    if mode & stat.S_IWOTH:
        output(
            msg=f"all users has write permission on the file. {file}",
            logger=logger,
            lvl="info",
        )
        results["allusers_write_access"] = True
    else:
        results["allusers_write_access"] = False

    if mode & stat.S_IXOTH:
        output(
            msg=f"all users has execute permission on the file. {file}",
            logger=logger,
            lvl="info",
        )
        results["allusers_execute_access"] = True
    else:
        results["allusers_execute_access"] = False

    output(msg="")

    return results


def __ls(path: str) -> List[str]:
    """
    A function which traverses through a subdirectory, finding all files when given a path.
    :params path: The path which will be traversed.
    :return: A list of files when traversing the given path.
    :rtype: list[str]
    """
    files = []

    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            output(
                msg=f"The file {filename} is a directory. Going to continue to traverse.",
                logger=logger,
                lvl="info",
            )
            files.append(os.path.join(path, filename))
            # its a dir, recurse
            resp = __ls(os.path.join(path, filename))
            # collecte recurse data
            files.extend(resp)
        elif os.path.isfile(os.path.join(path, filename)):
            files.append(os.path.join(path, filename))
        else:
            output(
                msg=f"The file {filename} is not a file or directory.",
                logger=logger,
                lvl="warning",
            )
    return files


def crawl(args: argparse.Namespace) -> int:
    """Delegation functino for the crawl command."""

    if args.path:
        output(msg="Starting the crawl process.", logger=logger)
        try:
            if os.path.exists(args.path):
                output(
                    msg=f"The path {args.path} exists. Continuing.",
                    logger=logger,
                    lvl="info",
                )
                files = __ls(args.path)

                report = Report(path=args.path)
                for file in files:
                    resp = __check_permissions(file)
                    report._results["results"].append(resp)

                if args.output:
                    with open(args.output, "w") as out:
                        json.dump(report._results, out, indent=4)
                    out.close()
            else:
                output(
                    msg=f"No folder exists from the given path: {args.path}",
                    logger=logger,
                    lvl="error",
                )
                raise FileNotFoundError(
                    f"No folder exists from the given path: {args.path}",
                )
        except Exception as e:
            output(msg=str(e), logger=logger, lvl="error")
            raise e
