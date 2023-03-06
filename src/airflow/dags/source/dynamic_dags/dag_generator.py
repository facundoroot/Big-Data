import logging
import colorlog

def logger(name: str) -> logging.Logger:

    """
    Configure logger

    Args:
        *   name: Name for logger

    Returns: Logger object with specified name and colors
    """

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s %(name)s::%(asctime)s:: %(message)s",
        log_colors={
            'WARNING': 'yellow',
            'ERROR': 'red',
        },
        reset=True,
        style='%',
        datefmt='%d-%H:%M'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    LOGGER = logging.getLogger(name)
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.DEBUG)

    return LOGGER

LOGGER = logger('Dag generator')
