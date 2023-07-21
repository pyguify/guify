import os
import logging
import platform
import sys
import eel
from pymsgbox import alert
from .TestWorker import TestWorker
from configparser import ConfigParser

log = logging.getLogger("\tindex.py")
worker = TestWorker()


class GUIfy:
    # report_dir is the directory of the reports

    # report_prefix is the prefix of the report file
    # report_prefix can be set to one of the arguments
    # that is required by registered functions. For example:
    # if a registered function requires argument name and age
    # then report_prefix can be set to 'name' or 'age'.
    def __init__(self, app_name='GUIfy', port=8080, redirect_stdout=True):
        """
        Initialize the GUIfy object.

        :param app_name: The name of the app to display in the GUI.
        :type app_name: str (default: "GUIfy")

        :param port: The port to run the GUI on.
        :type port: int (default: 8080)

        :param report_dir: The directory to save the reports in.
        :type report_dir: str or None

        :param report_prefix: The prefix of the report file.
        :type report_prefix: str or none

        :param redirect_stdout: Whether to redirect stdout to the GUI.
        :type redirect_stdout: bool (default: True)
        """
        self._port = port
        self._app_name = app_name
        eel.expose(self.app_name)
        self.worker = worker
        self.monitor = self.worker.monitor
        self.config = self.worker.config_tab

        if redirect_stdout:
            sys.stdout = self.monitor

    def _get_eel_kwargs_from_dict(self, kwargs: dict):
        dirname = os.path.dirname(os.path.abspath(__file__))
        directory = kwargs.get('directory', os.path.join(dirname, 'web'))
        debug = kwargs.get('debug', False)
        app = kwargs.get('app', 'chrome')
        port = kwargs.get('port', self._port)
        page = kwargs.get('page', 'index.html')
        app_mode = kwargs.get('app_mode', True)
        return directory, debug, app, port, page, app_mode

    def app_name(self):
        """
        return the name of the app
        :return: The name of the app
        :rtype: str
        """
        return self._app_name

    def register(self, priority: int = None, name: str = None, description: str = None):
        """
        A decorator to register a function to the GUI.

        :param priority: The priority of the function. The higher the priority,
        the higher the function will appear in the GUI.
        :type priority: int or None

        :param name: The name of the function to display in the GUI.
        :type name: str or None

        :param description: The description of the function to display in the GUI.
        :type description: str or None

        :return: The decorator function.
        :rtype: function
        """
        def decorator(func):
            self.worker.pool.add(func, name,
                                 priority, description)
        return decorator

    def prompt_user(self, title: str, prompt: str):
        """
        Prompt the user for input.
        Shows a prompt to the user to click Ok or Cancel and waits for the user to respond.

        :param prompt: The prompt to show to the user.
        :type prompt: str

        :return: The response of the user.
        :rtype: str

        :raises: ValueError if prompt is not a string.
        """
        self.worker.raise_prompt(title, prompt)

    def sleep(self, seconds: int):
        """
        Sleep for the specified number of seconds.

        :param seconds: The number of seconds to sleep.
        :type seconds: int

        :raises: ValueError if seconds is not an integer.
        """
        eel.sleep(seconds)

    def run(self, host='localhost', _eel_kwargs: dict = {}):
        """
        Run the main loop of the GUI.
        """
        directory, debug, app, port, page, app_mode = self._get_eel_kwargs_from_dict(
            _eel_kwargs)

        log.debug("Starting GUIfy")
        eel_kwargs = dict(
            host=host,
            size=(1280, 800),
            app_mode=app_mode,
        )
        log.debug("initiating eel")
        eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])
        try:
            log.debug("starting eel")
            eel.start(page, mode=app, port=port, **eel_kwargs)
        except EnvironmentError as env:

            if "[WinError 10048]" in str(env):
                log.exception(f"Port {port} is already in use")
                alert(
                    f"ERROR!: Another program is using port {port}. Please close it and try again.\n\n{str(env)}",
                    title="IO ERROR!")
                raise
            else:
                log.debug("Chrome not found, trying Microsoft Edge")
                # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
                if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
                    eel.start(page, mode='edge', **eel_kwargs)
                else:
                    raise

        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO, filename="log.txt")
