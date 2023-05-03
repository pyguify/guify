import inspect
import os
from importlib.machinery import SourceFileLoader
from .BaseTest import BaseTest
from .ConfigTab import ConfigTab

# Constants
DOT = '.'

TEST_SCRIPTS = 'test_scripts'  # Folder name
INIT_FILE = '__init__.py'
