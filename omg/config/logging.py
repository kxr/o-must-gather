import sys
from os import getenv
from loguru import logger


def _is_debug_or_trace(record):
    return (
        record["level"].name == "DEBUG"
        or
        record["level"].name == "TRACE"
    )


def _is_info(record):
    return record["level"].name == "INFO"


def _is_success(record):
    return record["level"].name == "SUCCESS"


def _is_warning_or_error(record):
    return (
        record["level"].name == "WARNING"
        or
        record["level"].name == "ERROR"
    )


_debug_fmt = (
    "<level>{level}</level> "
    "[<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>] "
    "{message}"
)
_info_fmt = (
    "<level>{level}</level> {message}"
)
_success_fmt = (
    "<bold>{message}</bold>"
)


def setup_logging(loglevel):

    # If loglevel is not set, we check the env['OMG_LOG_LEVEL']
    # else we set it to default "normal"
    if not loglevel:
        env_log_level = getenv("OMG_LOG_LEVEL")
        if (env_log_level and env_log_level in ['normal', 'info', 'debug', 'trace']):
            loglevel = env_log_level
        else:
            loglevel = "normal"

    # Map the loglevel to loguru's standard/default loglevel
    # normal -> SUCCESS(25)
    # info   -> INFO(20)
    # debug  -> DEBUG(10)
    # trace  -> TRACE(5)
    if loglevel == 'normal':
        level = 25
    elif loglevel == 'info':
        level = 20
    elif loglevel == 'debug':
        level = 10
    elif loglevel == 'trace':
        level = 5
    else:
        raise ValueError('Invalid loglevel: ' + str(loglevel))

    logger.remove()

    # debug or trace uses _debug_fmt format
    if level <= 10:
        logger.add(sys.stderr, colorize=True, level=level,
                   filter=_is_debug_or_trace, format=_debug_fmt)

    # info uses _info_fmt format
    if level <= 20:
        logger.add(sys.stderr, colorize=True, level=level,
                   filter=_is_info, format=_info_fmt)

    # normal/default uses _success_fmt for success logs
    # and _info_fmt for error and warning logs
    if level <= 25:
        logger.add(sys.stderr, colorize=True, level=level,
                   filter=_is_success, format=_success_fmt)
        logger.add(sys.stderr, colorize=True, level=level,
                   filter=_is_warning_or_error, format=_info_fmt)
