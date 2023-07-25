from src import guify
from src.guify.BaseTest import BaseTest
import pytest
from time import sleep

TEST_NAME = "Passing test"
TEST_PRIORITY = 1
TEST_DESCRIPTION = "This is a passing test."


@pytest.fixture()
def BaseTestFixture():
    def passing_test(length):
        sleep(length)
        return True

    test = BaseTest(passing_test, TEST_NAME, TEST_PRIORITY, TEST_DESCRIPTION)


class testBaseTest:
    def test_properties(self, BaseTestFixture):
        assert BaseTestFixture.name == TEST_NAME.title()
        assert BaseTestFixture.priority == TEST_PRIORITY
        assert BaseTestFixture.description == TEST_DESCRIPTION
        assert BaseTestFixture.run(0.1) is True
        assert BaseTestFixture.required_params == {"length"}
