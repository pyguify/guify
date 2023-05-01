import inspect
import os
from importlib.machinery import SourceFileLoader
from .BaseTest import BaseTest
from .ConfigTab import ConfigTab

# Constants
DOT = '.'

TEST_SCRIPTS = 'test_scripts'  # Folder name
INIT_FILE = '__init__.py'

# def get_test_scripts_module():
#     cwd = os.getcwd()
#     this_module_dir, this_filename = os.path.split(__file__)
#     src_dir, package_name = os.path.split(this_module_dir)
#     project_dir, src_dir_name = os.path.split(src_dir)
#     test_scripts_path = os.path.join(project_dir, TEST_SCRIPTS)
#     init_file_path = os.path.join(test_scripts_path, INIT_FILE)
#     test_scripts = SourceFileLoader(TEST_SCRIPTS, init_file_path).load_module()
#     return test_scripts


# def get_all_tests():

#     def filter_(c):
#         if (inspect.isclass(c) and c is not test_scripts.BaseTest):
#             return issubclass(c, test_scripts.BaseTest)
#         else:
#             False
#     all_files = inspect.getmembers(test_scripts, filter_)
#     for name, module in all_files:
#         yield name, module


# def get_config():

#     def filter_(c):
#         return inspect.isclass(c) and c is test_scripts.ConfigTab

#     cfg_cls = inspect.getmembers(test_scripts, filter_)[0][1]

#     return cfg_cls()
