import contextlib
import logging
import traceback
from typing import Generator


logger = logging.getLogger(__name__)


class Error(RuntimeError):
    pass


def _log_and_exit(msg: str, ret_code: int, exc: BaseException, traceback: str) -> None:
    log_msg = f"{msg}: {type(exec).__name__} -> {exc}"
    logger.warning(log_msg)
    logger.warning(str(traceback))
    raise SystemExit(ret_code)


@contextlib.contextmanager
def error_handler() -> Generator[None, None, None]:
    """context manager for error handling."""
    try:
        yield
    except Exception as e:
        if isinstance(e, Error):
            msg, ret_code = "An error has occured", 1
        else:
            msg, ret_code = "An unexpected error has occured", 3

        _log_and_exit(msg, ret_code, e, traceback.format_exc())
