"""
    Rsyslog *omprog* plugin

    Propagate message logs for python instance.
    Rsylog (action) > Python (readlines) > Redis (pubsub channel)
"""

import redis
import sys
import os
import logging
import json
from typing import Tuple


logging.basicConfig(
    stream=sys.stderr,
    level=os.getenv('RSYSLOG_PYTHON_REDIS_LOG_LEVEL', 'WARNING'),
    format='%(asctime)s %(levelname)s %(message)s'
)
REDIS_ADDRESS: str = os.getenv('RSYSLOG_PYTHON_REDIS_ADDRESS', '127.0.0.1')
REDIS_PORT = int(os.getenv('RSYSLOG_PYTHON_REDIS_PORT', 6379))


def on_init() -> redis.Redis:
    """
    Connect Redis

    Apart from processing the logs received from rsyslog, you want your plugin
    to be able to report its own logs in some way. This will facilitate
    diagnosing problems and debugging your code. Here we set up the standard
    Python logging system to output the logs to stderr. In the rsyslog
    configuration, you can configure the 'omprog' action to capture the stderr
    of your plugin by specifying the action's "output" parameter.

    Raises:
        Exception: If redis connection error occurs.
    """
    logging.debug("on_init called")

    # Tell rsyslog we are ready to start processing messages:
    print("OK", flush=True)

    redis_connection = redis.Redis(
        host=REDIS_ADDRESS,
        port=REDIS_PORT,
        db=0
    )

    return redis_connection


def on_processed(log_raw: str) -> Tuple[str, str]:
    """
    Process one log message received from rsyslog

    If this function raises an error, the message will be retried by rsyslog.

    Args:
        log_raw: the log message. Does NOT include a trailing newline.
    Raises:
        RecoverableError: If a recoverable error occurs. The message will be
            retried without restarting the plugin.
        Exception: If a non-recoverable error occurs. The plugin will be
            restarted before retrying the message.
    """
    logging.debug("on_message called")

    log_gelf_format = json.loads(log_raw)

    redis_channel = log_gelf_format['application']
    payload = json.dumps(log_gelf_format)

    return redis_channel, payload


def on_send(redis_connection: redis.Redis, channel: str, log: str):
    redis_connection.publish(channel, log)


def on_exit():
    """
    notify rsyslog success

    Do everything that is needed to finish processing (e.g. close files,
    handles, disconnect from systems...). This is being called immediately
    before exiting.
    This function should not raise any error. If it does, the error will be
    logged as a warning and ignored.
    """
    logging.debug("on_exit called")
    print("OK", flush=True)
    sys.exit(0)


def receive_log_from_rsyslog() -> str:
    """
    receive log from rsyslog action omprog

    Any line written to stdout that is not a status code will be
    treated as a recoverable error by 'omprog', and cause the action
    to be temporarily suspended. In this skeleton, we simply return
    a one-line representation of the Python exception. (If debugging
    is enabled in rsyslog, this line will appear in the debug logs.)
    """
    line = sys.stdin.readline()
    return line


def main():
    try:
        redis_connection = on_init()
    except Exception as e:
        logging.exception(f"Initialization error, exiting program | {e}")
        sys.exit(1)

    try:
        log_raw = receive_log_from_rsyslog()
    except Exception as e:
        logging.exception(e)
        sys.exit(1)

    try:
        redis_channel, log_processed = on_processed(log_raw)
    except Exception as e:
        logging.exception(e)
        sys.exit(1)

    try:
        on_send(redis_connection, redis_channel, log_processed)
    except Exception as e:
        logging.exception(e)
        sys.exit(1)

    on_exit()


if not os.getenv('TEST_PY_RSYSLOG_REDIS'):
    main()
