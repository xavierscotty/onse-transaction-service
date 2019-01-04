import pytest

import mock
from transaction_service import channel


@pytest.fixture
def channel():
    return channel()


@pytest.fixture
def channel_client(channel):
    return channel.test_client()
