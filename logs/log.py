import functools
from loguru import logger


def log_dec(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        logger.info(f'Running {func.__name__}')
        result = func(*args, **kwargs)
        logger.info(f'Ended {func.__name__}')
        return result
    return wraps
