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
            test = BaseTest(worker.pool, func, name, priority, description)
            test.run = func
            self.worker.pool.add((func.__name__, test))
        return decorator

    def prompt_user(self, prompt: str):
        return self.worker.set_prompt(prompt)

    def run(self):
        debug = 'dev' in sys.argv
        """Start Eel with either production or development configuration."""
        @eel.expose
        def app_name():
            return self.app_name

        if debug:
            directory = 'src\\guify\\web'
            app = None
            port=3001
            page = {port:3000}
            app_mode = False
        else:
            directory = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'web')
            app = 'chrome'
            port=self._port
            page = 'index.html'
            app_mode = True

        eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])
        eel_kwargs = dict(
            host='localhost',
            size=(1280, 800),
            app_mode=app_mode,
        )
        try:
            print(port)
            eel.start(page, mode=app, port=port, **eel_kwargs)
        except EnvironmentError as env:
            if "[WinError 10048]" in str(env):
                alert(
                    f"ERROR!: Another program is using port 8080. Please close it and try again.\n\n{str(env)}",
                    title="IO ERROR!")
                raise
            else:
                # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
                if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
                    eel.start(page, mode='edge', **eel_kwargs)
                else:
                    raise

        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO, filename="log.txt")