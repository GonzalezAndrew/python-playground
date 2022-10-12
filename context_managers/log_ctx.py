import sys
from typing import IO
from typing import Optional
import contextlib
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("test.log"), logging.StreamHandler()],
)

logger = logging.getLogger("test")
"""
the exitstack() context manager allows you to add things to the context manager
and will get torn down eventually 
"""


def output_line(
    s: str, stream: IO[str] = sys.stdout, filename: Optional[str] = None
) -> None:
    with contextlib.ExitStack() as exit_stack:
        streams = [stream]

        if filename:
            # add new resource to context manager
            # also add the value you got in and append it to list of streams

            streams.append(exit_stack.enter_context(logger.info(msg=s)))

        for output_stream in streams:
            if s is not None:
                output_stream.write(f"{s}\n")
            output_stream.flush()


output_line("hello world")
output_line("goodbye world", filename="log.log")
output_line("hello again", filename="log.log")
