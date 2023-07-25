from src import guify
from src.guify.TestWorker import TestWorker
import pytest
from time import sleep

TEST_NAME = "Passing test"
TEST_PRIORITY = 1
TEST_DESCRIPTION = "This is a passing test."


@pytest.fixture()
def worker():
    return TestWorker()


@pytest.fixture()
def populated_worker(worker):
    def passing_test(length):
        sleep(length)
        return True

    worker.pool.add(passing_test, TEST_NAME, TEST_PRIORITY, TEST_DESCRIPTION)
    return worker


class TestTestWorker:
    def initiated(self, worker):
        assert worker.current_job is None
        assert worker.params == {}
        assert worker._prompt_message == None
        assert worker._prompt_title == None
        assert worker.queue == []

    def test_properties(self, worker):
        self.initiated(worker)
        assert worker.queue == []
        assert worker.pool.required_params == set()
        assert worker.prompt == (None, None)

    def test_add(self, worker):
        self.initiated(worker)
        assert worker.pool.does_exist(TEST_NAME) is False

        with pytest.raises(KeyError):
            worker.pool.get_test_from_name(TEST_NAME) is None

        def test():
            return True

        worker.pool.add(test, TEST_NAME,
                        TEST_PRIORITY, TEST_DESCRIPTION)

        assert worker.pool.does_exist(test.__name__) is True
        assert worker.pool.get_test_from_name(test.__name__) is not None
