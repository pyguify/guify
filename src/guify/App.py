from .TestWorker import TestWorker
from .BaseTest import BaseTest
import os
import logging
import platform
import sys
import eel
from pymsgbox import alert

log = logging.getLogger("\tindex.py")
worker = TestWorker()


class GUIfy:
    # report_dir is the directory of the reports

    # report_prefix is the prefix of the report file
    # report_prefix can be set to one of the arguments
    # that is required by registered functions. For example:
    # if a registered function requires argument name and age
    # then report_prefix can be set to 'name' or 'age'.
    def __init__(self, app_name='GUIfy', port=8080, report_dir=None, report_prefix=None, redirect_stdout=True):
        self._port = port
        self._app_name = app_name
        eel.expose(self.app_name)
        worker._report_dir = report_dir
        worker._report_prefix = report_prefix
        self.worker = worker
        self.monitor = self.worker.monitor
        self.config = self.worker.config_tab

        if redirect_stdout:
            sys.stdout = self.monitor

    def app_name(self):
        return self._app_name

    def register(self, priority: int = None, name: str = None, description: str = None):
        def decorator(func):
            self.worker.pool.add(func, name,
                                 priority, description)
        return decorator

    def prompt_user(self, prompt: str):
        return self.worker.set_prompt(prompt)

    def _get_eel_kwargs_from_dict(self, kwargs: dict):
        dirname = os.path.dirname(os.path.abspath(__file__))
        directory = kwargs.get('directory', os.path.join(dirname, 'web'))
        debug = kwargs.get('debug', False)
        app = kwargs.get('app', 'chrome')
        port = kwargs.get('port', self._port)
        page = kwargs.get('page', 'index.html')
        app_mode = kwargs.get('app_mode', True)
        return directory, debug, app, port, page, app_mode

    def run(self, _eel_kwargs: dict = {}):
        # _eel_kwargs is solely for development and testing purposes
        directory, debug, app, port, page, app_mode = self._get_eel_kwargs_from_dict(
            _eel_kwargs)

        log.debug("Starting GUIfy")
        eel_kwargs = dict(
            host='localhost',
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
