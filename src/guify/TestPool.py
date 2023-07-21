import logging
from collections.abc import Iterable
from .BaseTest import BaseTest
from types import FunctionType

log = logging.getLogger('TestPool')

# The object containing all the tests
# their order, and their classes
# classes are all instances of BaseTest


class TestPool:
    def __init__(self, worker, additional_params):
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
        '''
        Returns a list of the tests in the order they should be run.
        '''
        return self._order

    @property
    def required_params(self):
        '''
        Returns a set of all the required parameters for all the tests.
        :rtype: set
        '''
        return_value = set(self.additional_params())
        for cls in self:
            return_value = return_value.union(cls.required_params)
        return return_value

    def add(self, func: FunctionType = None, name: str = None, priority: int = None, description: str = None):
        '''
        Add a test to the pool.
        :param func: The function to add.
        :param name: The name of the test.
        :param priority: The priority of the test.
        :param description: The description of the test.
        '''
        log.debug(f"Registering {func.__name__} as {name or func.__name__}")
        test = BaseTest(func, name, priority, description)
        test.run = func
        if priority is None:
            self._order.append(func.__name__)
        else:
            self._order.insert(priority, func.__name__)
        for param in test.required_params:
            if param not in self.worker.params:
                self.worker.params[param] = ''

        self._pool[func.__name__] = test

    def does_exist(self, name):
        '''
        Check if a test exists in the pool.
        :param name: The name of the test.
        :rtype: bool
        '''
        return name in self._order

    def get_test_from_name(self, name) -> BaseTest:
        '''
        Get a test from the pool by its name.
        :param name: The name of the test.
        :rtype: BaseTest
        '''
        return self._pool[name]

    def __iter__(self) -> Iterable[BaseTest]:
        '''
        Iterate over the tests in the pool.
        :rtype: Iterable[BaseTest]
        '''
        for i in range(len(self._order)):
            name = self._order[i]
            yield self._pool[name]
