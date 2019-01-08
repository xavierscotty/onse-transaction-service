import pytest

from transaction_service.app import Application


@pytest.fixture(scope="function")
def app():
    return Application()
