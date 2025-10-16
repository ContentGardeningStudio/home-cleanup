# TODO: Basic logging setup.
# def setup_logging(verbosity: int = 0) -> None: ...
# Levels: 0=WARNING, 1=INFO, 2=DEBUG

import logging
import sys


def setup_logging(verbosity: int = 0) -> None:
    """
    Configure logging based on verbosity level.

    Levels:
        0 = WARNING
        1 = INFO
        2 = DEBUG
    """
    # Map verbosity to logging levels
    if verbosity <= 0:
        level = logging.INFO
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    # Basic logging config
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    logging.debug("Logging initialized at %s level",
                  logging.getLevelName(level))
