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
    def __init__(self, app_name='GUIfy', port=8080):
        self._port = port
        self.app_name = app_name
        self.worker = worker
        self.monitor = worker.monitor
        self.config = worker.config_tab

    def register(self, priority: int = None, name: str = None, description: str = None):
        def decorator(func):
            log.debug(f"Registering {func.__name__} as {name}")
            test = BaseTest(worker.pool, func, name, priority, description)
            test.run = func
            self.worker.pool.add((func.__name__, test))
        return decorator

    def prompt_user(self, prompt: str):
        return self.worker.set_prompt(prompt)

    # _eel_kwargs is solely for development and testing purposes
    def run(self, _eel_kwargs: dict = None):
        log.debug("Starting GUIfy")
        
        directory = _eel_kwargs.get('directory', os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'web'))
        debug = _eel_kwargs.get('debug', False)
        app = _eel_kwargs.get('app', 'chrome')
        port = _eel_kwargs.get('port', self._port)
        page = _eel_kwargs.get('page', 'index.html')
        app_mode = _eel_kwargs.get('app_mode', True)
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