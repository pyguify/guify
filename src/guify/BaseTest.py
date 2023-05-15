from types import FunctionType

EXCLUDED_PARAMS = {"self", "args", "kwargs"}


class BaseTest:
    def __init__(self, func: FunctionType, verbose_name=None, priority=None, description=None):
        if verbose_name is not None:
            self._verbose_name = verbose_name
        else:
            self._verbose_name = func.__name__.replace(
                "_", " ")
        self.priority = priority
        self.description = description
        self.run = func
        self._name = func.__name__

    @property
    def name(self):
        '''
        Return the name of this test.
        '''
        return self._verbose_name.title()

    @property
    def required_params(self):
        '''
        Return a set of the required parameters for this test.
        '''
        all_vars = self.run.__code__.co_varnames

        # remove all variables that are not parameters
        args = set(all_vars[:self.run.__code__.co_argcount])

        # remove all excluded parameters
        test_params = args.difference(
            EXCLUDED_PARAMS)

        return test_params
