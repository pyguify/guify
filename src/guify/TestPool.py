import logging
from collections.abc import Iterable
from .BaseTest import BaseTest
from types import FunctionType

log = logging.getLogger('TestPool')

# The object containing all the tests
# their order, and their classes
# classes are all instances of BaseTest


class TestPool:
    def __init__(self, worker, *additional_params):
        # additional_params is any other params that
        # might be required (not by the tests)
        self.additional_params = additional_params
        self.worker = worker
        self.config_tab = worker.config_tab
        self.monitor = worker.monitor
        self._order: list[str] = []
        self._pool: dict[str: BaseTest] = {}

    # The list with the order of the tests
    # Order is set according to the priority
    # param given by the BaseTest class
    @property
    def order(self):
        return self._order

    @property
    def required_params(self):
        return_value = set(self.additional_params)
        for cls in self:
            return_value = return_value.union(cls.required_params)
        return return_value

    def add(self, func: FunctionType = None, name: str = None, priority: int = None, description: str = None):
        log.debug(f"Registering {func.__name__} as {name or func.__name__}")
        test = BaseTest(func, name, priority, description)
        test.run = func
        if priority is None:
            self._order.append(func.__name__)
        else:
            self._order.insert(priority, func.__name__)

        self._pool[func.__name__] = test

    def does_exist(self, name):
        return name in self._order

    def get_test_from_name(self, name) -> BaseTest:
        return self._pool[name]

    def __iter__(self) -> Iterable[BaseTest]:
        for i in range(len(self._order)):
            name = self._order[i]
            yield self._pool[name]
