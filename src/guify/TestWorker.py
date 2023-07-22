import os.path
from jinja2 import Template
from configparser import ConfigParser
from eel import sleep
from .TestPool import TestPool
from .BaseTest import BaseTest
from threading import Thread, Event, Lock
import logging
from .constants import (
    OK,
    CANCEL,
    WAITING_FOR_RUN,
    RUNNING_TEST,
    PENDING_USER_INPUT,
    DONE,
)
from .Monitor import Monitor
from .ConfigTab import ConfigTab
import traceback
import eel

CFG_FILE_NAME = "settings.ini"
DEFAULT_REPORTS_FOLDER_NAME = "reports"

log = logging.getLogger("\tTestWorker")


class TestWorker(Thread):
    '''
    The TestWorker class is responsible for running the tests.

    '''
    _instance = None
    monitor = Monitor()
    config_tab = ConfigTab()

    # def __new__(cls, *args, **kwargs):
    #     if not isinstance(cls._instance, cls):
    #         cls._instance = object.__new__(
    #             cls, *args, **kwargs)  # type: ignore
    #     return cls._instance

    def __init__(self):
        super().__init__(name="TestWorker")
        self.pool = TestPool(self, self.additional_params)
        self._state = WAITING_FOR_RUN
        self._prompt_message = None
        self._prompt_title = None
        self._current_job = None
        self.pause = Event()
        self._halt = Event()
        self._lock = Lock()
        self.params = {}
        self._selected_tests = []
        self.queue = []

    @property
    def selected_tests(self):
        return self._selected_tests

    @selected_tests.setter
    def selected_tests(self, value) -> list:
        self._selected_tests = value

    @property
    def current_job(self):
        return self._current_job

    @current_job.setter
    def current_job(self, value):
        eel.set_current_job(value)
        self._current_job = value

    def additional_params(self):
        """
        Returns a list of additional parameters that are required
        to run the tests, but are not required by the tests themselves.

        For example, if a report generation is on, then the report prefix
        is required, but not by the tests themselves.

        :rtype: list
        """

        SETTINGS_FILE = os.path.join(os.getcwd(), 'settings.ini')
        if not os.path.exists(SETTINGS_FILE):
            cfg = ConfigParser()
            cfg.read_dict(
                {'reports': {'reports_dir': '', 'report_prefix': ''}})
            with open(SETTINGS_FILE, 'w') as f:
                cfg.write(f)
        report_prefix = self._get_settings("report_prefix")
        if len(report_prefix.strip()) > 0:
            return [report_prefix,]
        else:
            return []

    @property
    def prompt(self):
        return (self._prompt_title, self._prompt_message)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        eel.set_state(value)
        self._state = value

    def _get_settings(self, setting):
        """
        Return the directory of the reports.
        :return: The directory of the reports.
        :rtype: str
        """
        cfg = ConfigParser()
        cfg.read(os.path.join(os.getcwd(), 'settings.ini'))
        return cfg.get('reports', setting)

    def set_param(self, key, value):
        """
        Sets a parameter for the worker.

        :param key: The key of the parameter.
        :type key: str
        :param value: The value of the parameter.
        :type value: str
        """
        self.params[key] = value

    def raise_prompt(self, title, msg):
        self.pause.set()
        eel.prompt(title, msg)
        self.state = PENDING_USER_INPUT
        log.debug("Prompt returned: {}".format(msg))
        self._prompt_title = title
        self._prompt_message = msg
        self._wait_for_response()

    def _get_prefix(self):
        """
        Returns the prefix for the report name.
        """
        report_prefix = self._get_settings("report_prefix")
        return self.params[report_prefix] if len(report_prefix.strip()) > 0 else "report"

    def _create_report_folder(self, report_dir):
        """
        Creates the reports folder if it doesn't exist.
        """
        # creates the reports folder if it doesn't exist
        # if the folder already exists, does nothing
        if not os.path.isdir(report_dir):
            os.mkdir(report_dir)

    def _get_reports_path(self):
        """
        Returns the path to the reports folder.
        """
        report_dir = self._get_settings("reports_dir")
        if report_dir is None:
            log.debug("No report directory set, report generation is off")
            return None

        if os.path.isabs(report_dir):
            retval = report_dir
        else:
            retval = os.path.join(os.getcwd(), report_dir)

        self._create_report_folder(retval)
        return retval

    def finish_job(self, report: dict):
        """
        Called when all tests are finished running.
        :param report: The report of the tests.
        :type report: dict
        """
        # called when all tests are finished running
        self.pause.set()
        self.state = DONE

        if False in report.values():
            self.raise_prompt("Oops", "Some tests have failed.")
        else:
            self.raise_prompt("Done!", "All tests passed!")

        self._save_report(report)
        self.state = WAITING_FOR_RUN
        self.current_job = None
        self.pause.clear()
        self._halt.clear()
        log.debug('"Restarting" thread')
        super().__init__(name="TestWorker")

    def stop(self):
        """
        Stop the worker, but not the thread.
        """
        self.pause.clear()
        self._halt.set()
        self._lock.acquire()
        self.current_job = None

    def answer_prompt(self, response):
        """
        Answer the prompt with the given response.
        :param response: The response to the prompt.
        :type response: str
        """
        log.debug("Answering prompt with: {}".format(response))
        assert response in [
            OK,
            CANCEL,
        ], f"Gotten response other than '{OK}' or '{CANCEL}'"
        if response == OK:
            self.state = RUNNING_TEST
            self._prompt_message = None
            self._prompt_title = None
            eel.prompt(None, None)
            self.pause.clear()
            log.debug("Prompt cleared")
        else:
            self._prompt_message = None
            self._prompt_title = None
            self._halt.set()
            self.pause.clear()

    def _wait_for_response(self):
        """
        Wait until user to answer the prompt.
        """
        while self.pause.is_set():
            sleep(1)
        is_halted = self._halt.is_set()
        is_paused = self.pause.is_set()
        return not is_halted and not is_paused

    def _wait_for_unpause(self):
        """
        Wait until pause is cleared.
        """
        while self.pause.is_set():
            sleep(1)

    def _purge_kwargs(self, required: set):
        """
        Remove unnecessary kwargs that are not in "required" set.
        :param required: The required parameters.
        :type required: set
        """

        return {key: value for key, value in self.params.items() if key in required}

    def _run_test(self, test: BaseTest):
        """
        Run a test.
        :param test: The test to run.
        :type test: BaseTest

        :return: True if the test passed, False if the test failed.
        :rtype: bool
        """
        log.debug(f"Running test: {test._name}")
        params = self._purge_kwargs(test.required_params)
        try:
            self.current_job = test._name

            # Stop running if halt flag is True
            if self._halt.is_set():
                return False

            result = test.run(**params)

            log.info(
                f"Test: {test._name}\t Status:{'Pass' if result else 'Fail'}")

            self.current_job = None
            return result

        except Exception as exc:
            exc_str = f"{exc.__class__.__name__}: {exc} in {test._name}"
            log.error(exc_str)
            print(traceback.format_exc())

            self.raise_prompt("Error!", exc_str)
            return False

    def _save_report(self, report: dict):
        """
        Save the report to a file.
        :param report: The report to save.
        :type report: dict
        """

        log.debug("Saving report")
        reports_path = self._get_settings("reports_dir")
        if reports_path == '' or len(reports_path.strip()) == 0:
            return
        if not os.path.exists(reports_path):
            os.mkdir(reports_path)

        def get_filepath(i=1):
            # returns the file path for the report
            # if the file already exists, adds a number to the end of the filename
            # e.g. report.txt -> report_1.txt -> report_2.txt
            filename = f"{self._get_prefix()}_{i}.html"
            filepath = os.path.join(reports_path, filename)
            if os.path.isfile(filepath):
                return get_filepath(i + 1)
            else:
                return filepath

        with open(get_filepath(), 'w') as f:
            template = Template(
                open(os.path.join(os.path.dirname(__file__), 'report_template.html')).read())
            f.write(template.render(tests=report, params=self.params))

    def add_to_queue(self, test_name):
        """
        Add a test to the selection.
        :param test_name: The test name to add.
        :type test_name: str
        """
        if test_name not in self.selected_tests:
            self.selected_tests.append(test_name)

    def remove_from_queue(self, test_name):
        """
        Remove a test from the selection.
        :param test_name: The test name to remove.
        :type test_name: str
        """
        if test_name in self.selected_tests:
            self.selected_tests.remove(test_name)

    def start(self) -> None:
        """
        Start the worker thread.
        :param tests: The tests to run.
        :type tests: list

        :param parameters: The parameters to run the tests with.
        :type parameters: dict
        """
        self.state = RUNNING_TEST
        if self.params is None:
            self.state = WAITING_FOR_RUN
            raise AttributeError(
                "Missing attribute when starting test worker thread")

        if self.selected_tests == []:
            self.state = WAITING_FOR_RUN
            raise AttributeError("No tests selected")

        given_params = set(self.params.keys())
        required_params = set(self.additional_params())
        # Get required params for tests.
        for name in self.selected_tests:
            required_params = required_params.union(
                self.pool.get_test_from_name(name).required_params
            )

        # Checks whether we have enough kwargs to run all tests
        if not given_params.issuperset(required_params):
            missing = required_params.difference(given_params)
            self.state = WAITING_FOR_RUN
            raise AttributeError(f"Missing parameters to run tests: {missing}")
        self.queue = self.selected_tests.copy()

        super().start()

    def _get_initial_report(self):
        """
        Returns an initial report with all tests set to None.
        :rtype: dict
        """
        return {self.pool.get_test_from_name(test)._verbose_name: None for test in self.pool.order}

    def run(self):
        """
        Run all tests in the queue.
        """
        self.monitor.flush()
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

                report[test._verbose_name] = status
                if status is False:
                    self.stop()
                    break

        self.finish_job(report)
