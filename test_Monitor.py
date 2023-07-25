from src import guify
from src.guify.Monitor import Monitor
import pytest


@pytest.fixture()
def monitor():
    return Monitor()


class TestMonitor:
    def test_set_text(self, monitor):
        monitor.set_text("This is a test")
        assert monitor.text == "This is a test"

    def test_write(self, monitor):
        monitor.write("This is a test")
        assert monitor.text == "This is a test"

    def test_flush(self, monitor):
        monitor.write("This is a test")
        monitor.flush()
        assert monitor.text == ""
