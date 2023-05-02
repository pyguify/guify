import os.path
from pathlib import Path
from configparser import ConfigParser
from eel import sleep
from .TestPool import TestPool
from .BaseTest import BaseTest
from threading import Thread, Event, Lock
import logging
from .constants import OK, CANCEL, WAITING_FOR_RUN, RUNNING_TEST, PENDING_USER_INPUT, DONE
from .Monitor import Monitor
from .ConfigTab import ConfigTab

CFG_FILE_NAME = 'settings.ini'
DEFAULT_REPORTS_FOLDER_NAME = 'reports'

log = logging.getLogger("\tTestWorker")


class TestWorker(Thread):
    _instance = None
    monitor = Monitor()
    config_tab = ConfigTab()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(
                cls, *args, **kwargs)  # type: ignore
        return cls._instance

    def __init__(self):
        super().__init__(name='TestWorker')
        self.cfg = TestWorker._init_config()
        self.prefix_var = self.cfg.get('DEFAULT', 'report_name_prefix')

        if self.prefix_var != '' and self.prefix_var is not None:
            self.additional_params = [self.prefix_var,]
        else:
            self.additional_params = []

        self.pool = TestPool(self, *self.additional_params)
        self._state = WAITING_FOR_RUN
        self._prompt = None
        self.currently_running = None
        self.pause = Event()
        self._halt = Event()
        self._lock = Lock()
        self.queue = []

    @staticmethod
    def _init_config() -> ConfigParser:
        # initialize the config file
        # if no config file is found, create a new one
        # if config file is found, load it
        cfg = ConfigParser()
        cfg_path = os.path.join(os.getcwd(), CFG_FILE_NAME)
        if not os.path.isfile(cfg_path):
            log.debug("Config file not found, creating new one.")
            cfg['DEFAULT'] = {
                'reports_dir': '',
                'report_name_prefix': '',
            }
            with open(cfg_path, 'w') as f:
                cfg.write(f)
        else:
            log.debug("Config file found, loading...")
            if not cfg.has_option('DEFAULT', 'reports_dir'):
                cfg.set('DEFAULT', 'reports_dir', '')
            cfg.read(cfg_path)

        return cfg

    @property
    def prompt(self):
        return self._prompt

    @property
    def state(self):
        return self._state

    def _get_prefix(self):
        # returns the prefix for the report name
        # if no prefix is set, returns 'report'
        # prefix is set in settings.ini
        # can be set to one of the arguments given to
        # one of the tests
        return self.params[self.prefix_var] if self.prefix_var else 'report'

    def _get_reports_path(self):
        # returns the path to the reports folder
        # if no path is set, returns the default path
        # default path is 'reports' folder in the current working directory
        # path is set in settings.ini
        default_path = os.path.join(os.getcwd(), DEFAULT_REPORTS_FOLDER_NAME)
        configured_path = self.cfg.get('DEFAULT', 'reports_dir')
        if configured_path == '' or configured_path is None:
            log.debug("Reports path is not configured in settings.ini")
            if not os.path.isdir(default_path):
                log.debug(
                    "Couldn't find default report directory, creating new folder.")
                p = Path(default_path)
                p.mkdir()
            retval = os.path.abspath(default_path)
        else:
            log.debug("Report directory is configured")
            if not os.path.isdir(configured_path):
                log.debug("Reports directory does not exist, creating...")
                p = Path(configured_path)
                p.mkdir(parents=True)

            log.debug("REPORTS PATH:" + configured_path)
            retval = configured_path

        return retval

    def finish_job(self, report: dict):
        # called when all tests are finished running
        self.pause.set()
        self._state = DONE

        if False in report.values():
            self._prompt = 'fail'
        else:
            self._prompt = 'pass'

        self._save_report(report)
        self._wait_for_unpause()
        self._state = WAITING_FOR_RUN
        self.currently_running = None

        log.debug('"Restarting" thread')
        super().__init__(name='TestWorker')

    def set_prompt(self, message):
        self.pause.set()
        self._state = PENDING_USER_INPUT
        self._prompt = message
        return self._wait_for_response()

    def stop(self):
        self._halt.set()
        self._lock.acquire()
        self.currently_running = None

    def answer_prompt(self, response):
        assert response in [
            OK, CANCEL], f"Gotten response other than '{OK}' or '{CANCEL}'"
        if response == OK:
            self.pause.clear()
            self._state = RUNNING_TEST
            self._prompt = None
        else:
            self._prompt = None
            self._halt.set()
            self.pause.clear()

    def _wait_for_response(self):
        while self.pause.is_set():
            sleep(1)
        is_halted = self._halt.is_set()
        is_paused = self.pause.is_set()
        return not is_halted and not is_paused

    def _wait_for_unpause(self):
        while self.pause.is_set():
            sleep(1)

    def _purge_kwargs(self, required: set):
        # remove unnecessary kwargs that are not in "required" set.
        return {key: value for key, value in self.params.items() if key in required}

    def _run_test(self, test: BaseTest):
        log.debug(f"Running test: {test._name}")
        params = self._purge_kwargs(test.required_params)
        try:
            self.currently_running = test.name

            # Stop running if halt flag is True
            if self._halt.is_set():
                return False

            result = test.run(**params)

            log.info(
                f"Test: {test._name}\t Status:{'Pass' if result else 'Fail'}")

            return result

        except Exception as exc:
            exc_str = f"Exception: {exc} in {test._name}"
            log.error(exc_str)

            self.stop()

            self.set_prompt(exc_str)
            return False

    def _save_report(self, report: dict):

        reports_path = self._get_reports_path()

        def get_filepath(i=1):
            # returns the file path for the report
            # if the file already exists, adds a number to the end of the filename
            # e.g. report.txt -> report_1.txt -> report_2.txt
            filename = f"{self._get_prefix()}_{i}.txt"
            filepath = os.path.join(reports_path, filename)
            if os.path.isfile(filepath):
                return get_filepath(i + 1)
            else:
                return filepath

        with open(get_filepath(), 'x') as file:
            file.write("Test name\tStatus\n")
            for name, status in report.items():
                if status is True:
                    status = "Pass"
                elif status is False:
                    status = "Fail"
                else:  # if status is None
                    status = "Did not run"
                file.write(f"{name}:\t{status}\n")

    def start(self, tests: list = None, parameters: dict = None) -> None:
        self._state = RUNNING_TEST
        if parameters is None or tests is None:
            self._state = WAITING_FOR_RUN
            raise AttributeError(
                "Missing attribute when starting test worker thread")

        given_params = set(parameters.keys())
        required_params = set(self.additional_params)
        # Get required params for tests.
        for name in tests:
            required_params = required_params.union(
                self.pool.get_test_from_name(name).required_params
            )

        # Checks whether we have enough kwargs to run all tests
        if not given_params.issuperset(required_params):
            missing = required_params.difference(given_params)
            self._state = WAITING_FOR_RUN
            raise AttributeError(f"Missing parameters to run tests: {missing}")
        self.params = parameters
        self.queue = tests

        super().start()

    def _get_initial_report(self):
        return {key: None for key in self.queue}

    def run(self):
        self.monitor.clear_text()
        self._halt.clear()
        report = self._get_initial_report()
        log.info("Starting Worker Thread")
        for test in self.pool:
            if self._halt.is_set():
                break
            # Skip this iteration if test is not meant to run
            if test._name in self.queue:
                self.queue.remove(test._name)
                status = self._run_test(test)

                report[test._name] = status
                if status is False:
                    self._halt.set()
                    break

        self.finish_job(report)
