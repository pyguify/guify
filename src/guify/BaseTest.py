from .ConfigTab import ConfigTab
from .Monitor import Monitor
import sys
import os
from types import FunctionType

EXCLUDED_PARAMS = {"self", "args", "kwargs"}


class BaseTest:
    verbose_name: str = None
    description: str = ''
    initial_prompt = None

    def __init__(self, test_pool, func: FunctionType, verbose_name=None, priority=None, description=None, initial_prompt=None):
        self.verbose_name = verbose_name or self.verbose_name
        self.priority = priority
        self.description = description or self.description
        self.pool = test_pool
        self.monitor: Monitor = test_pool.monitor
        self.config: ConfigTab = test_pool.config_tab
        self._func = func

    @property
    def name(self):
        if self.verbose_name:
            return self.verbose_name
        else:
            return self.__class__.__name__

    @property
    def required_params(self):
        all_vars = self.run.__code__.co_varnames
        args = set(all_vars[:self.run.__code__.co_argcount])
        test_params = args.difference(
            EXCLUDED_PARAMS)
        return test_params

    def get_config(self, section, param) -> str:
        pass

    def prompt_user(self, prompt) -> bool:
        pass

    def run(self, *args, **kwargs) -> bool:
        return self._func(*args, **kwargs)
