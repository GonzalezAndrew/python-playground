import sys
from typing import Any
from typing import IO


def output(
    msg: str,
    stream: IO[str] = sys.stdout,
    logger: Any = None,
    lvl: str = "info",
) -> None:
    """Write to stdout and logfile.
    :param msg: The message to write to stdout and or the logfile.
    :param stream: The output stream to write to.
    :param logger: The logging object to write the msg to.
    :param lvl: The logging level. (info, error, warning)
    :return: None
    :rtype: None
    """
    streams = [stream]
    for output_stream in streams:
        if msg is not None:
            output_stream.write(f"{msg}\n")
        output_stream.flush()
    if logger:
        if lvl == "error":
            logger.error(msg)
        elif lvl == "warning":
            logger.warning(msg)
        else:
            logger.info(msg)
