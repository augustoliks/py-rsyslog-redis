import pyrsyslogredis
import pytest


@pytest.fixture
def log_raw_from_rsyslog() -> str:
    return '{"application": "app-a", "unixtime": 1607814928.69489}'


def test_retrieve_channel_from_log_raw(log_raw_from_rsyslog):
    channel, _ = pyrsyslogredis.on_processed(log_raw_from_rsyslog)
    assert channel == "app-a"


def test_retrieve_log_parsed_from_log_raw(log_raw_from_rsyslog):
    _, log_parsed = pyrsyslogredis.on_processed(log_raw_from_rsyslog)
    assert log_parsed == log_raw_from_rsyslog
