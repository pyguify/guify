import sys
if sys.stdout is None or sys.stderr is None:
    # When running built app (and using --noconsole) stdout and stderr are not
    # available. This is a workaround to make sure that errors are logged.
    sys.stdout = sys.stderr = open(os.path.join(os.getcwd(), 'log.txt'), 'w')

from .constants import OK, CANCEL
from .TestWorker import WAITING_FOR_RUN, PENDING_USER_INPUT, DONE
import os
import eel
from .constants import OK, CANCEL, WAITING_FOR_RUN, PENDING_USER_INPUT, DONE
from .App import worker, GUIfy
import logging

'''
Author github: @MikeyDN
Author: Michael Druyan
'''

log = logging.getLogger("guify.__init__")

### Start eel functions ###


@eel.expose
def run_tests(tests, params):
    """
    The function that gets called when clicking "Run Tests" in the GUI.

    :param tests: A list of tests to run
    :param params: A dictionary of parameters to pass to the functions.
    :return: A dictionary containing the current state of the worker.
    :rtype: {state: str, currentJob: str, prompt: str}
    """
    log.debug(f"run_tests called with tests: {tests}, params: {params}")
    if worker.state != WAITING_FOR_RUN:
        return {"error": f"Worker is currenty busy, Status: {worker.state}"}
    else:
        try:
            worker.start()
        except Exception as exc:
            return {"error": f"Error: {exc}"}
        else:
            return {
                "state": worker.state,
                "currentJob": worker.current_job,
                "prompt": worker.prompt
            }


@eel.expose
def all_tests():
    """
    The function to call from the GUI to get a list of all tests.
    :return: A dictionary containing a list of all tests.
    :rtype: {tests: [ {name: str, requiredParams: [str], description: str} ]}
    """

    log.debug(f"all_tests called")

    retval = {
        "tests": [
            {
                "name": test._name,
                "requiredParams": test.required_params,
                "description": test.description,
                "verbose_name": test.name
            } for test in worker.pool
        ]
    }
    return retval


@eel.expose
def get_state():
    '''
    The function that gets called from the GUI to get the current state of the
    worker.

    :return: A dictionary containing the current state of the worker.
    :rtype: { workerState: str }
    '''
    return worker.state


@eel.expose
def get_current_job():
    '''
    The function that gets called from the GUI to get the current job of the
    worker.

    :return: A dictionary containing the current job of the worker.
    :rtype: { currentJob: str }
    '''
    return worker.current_job


@eel.expose
def set_param(key, value):
    '''
    The function that gets called from the GUI to set a parameter for the
    worker.

    :param key: The key of the parameter.
    :type key: str
    :param value: The value of the parameter.
    :type value: str
    :return: A dictionary containing the current state of the worker.
    :rtype: {status: {state: str, currentJob: str, prompt: str}}
    '''
    log.debug(f"set_param called with key: {key}, value: {value}")
    if worker.state == WAITING_FOR_RUN:
        worker.set_param(key, value)
        eel.update_params(worker.params)
        return worker.params
    else:
        return {"error": f"Worker is currenty busy, Status: {worker.state}"}


@eel.expose
def get_params():
    '''
    The function that gets called from the GUI to get the current parameters of
    the worker.

    :return: A dictionary containing the current parameters of the worker.
    :rtype: dict
    '''
    return worker.params


@eel.expose
def get_prompt():
    '''
    The function that gets called from the GUI to get the current prompt of the
    worker.

    :return: A dictionary containing the current prompt of the worker.
    :rtype: { title: str, 'message': str }
    '''
    return worker.prompt


@eel.expose
def get_queue():
    '''
    The function that gets called from the GUI to get the current queue of the
    worker.

    :return: A dictionary containing the current queue of the worker.
    :rtype: { queue: [str] }
    '''
    return worker.selected_tests


@eel.expose
def current_job_params():
    """
    The function that gets called from the GUI to get the current parameters

    :return: A dictionary containing the current parameters
    :rtype: {params: dict}
    """
    log.debug(f"current_job_params called")
    if worker.current_job is None:
        return {}  # No job is running
    return worker.params


@eel.expose
def all_params():
    """
    get all the arguments that are required by the functions

    :return: A dictionary containing all the arguments that are required by the
    :rtype: {params: [str]}
    """
    log.debug(f"all_params called")
    all_params = list(worker.pool.required_params)
    all_params.sort()
    return {"params": all_params}


@eel.expose
def answer_prompt(response):
    """
    The function that gets called from the GUI to answer a prompt.

    :param response: The response to the prompt.
    :type response: "OK" or "CANCEL"
    :return: A dictionary containing the current state of the worker.
    :rtype: {status: {state: str, currentJob: str, prompt: str}}
    """

    log.debug(f"answer_prompt called with response: {response}")
    if response not in [OK, CANCEL]:
        return {"error": f"Invalid response: {response}"}
    else:
        if worker.state == PENDING_USER_INPUT or worker.state == DONE:
            worker.answer_prompt(response)
            return {
                "status": {
                    "state": worker.state,
                    "currentJob": worker.current_job,
                    "prompt": worker.prompt
                }
            }
        else:
            return {"error": f"Worker is not waiting for user input"}


@eel.expose
def get_monitor_text():
    """
    The function that gets called from the GUI to get the current monitor text.

    :return: A dictionary containing the current monitor text.
    :rtype: strs
    """
    log.debug(f"get_monitor_text called")
    return worker.monitor.text


@eel.expose
def get_config():
    """
    The function that gets called from the GUI to get config.ini

    :return: A dictionary containing the current config.ini
    :rtype: {config: dict}
    """
    log.debug(f"get_config called")
    return {'config': worker.config_tab.load()}


@eel.expose
def save_config(config: dict):
    """
    The function that gets called from the GUI to save config.ini

    :param config: A dictionary containing the current config.ini
    :type config: {config: dict}
    :return: A dictionary containing the current config.ini
    :rtype: {config: dict}
    """

    log.debug(f"save_config called with config: {config}")
    worker.config_tab.save(config)
    return {'config': worker.config_tab.load()}


@eel.expose
def add_to_queue(tests: list[str]):
    """
    The function that gets called from the GUI to add tests to the queue

    :param tests: A list of tests to add to the queue
    :type tests: [str]
    :return: A dictionary containing the current queue of the worker.
    :rtype: { queue: [str] }
    """
    log.debug(f"add_to_queue called with tests: {tests}")
    worker.add_to_queue(tests)
    eel.set_queue(worker.selected_tests)


@eel.expose
def remove_from_queue(tests: list[str]):
    """
    The function that gets called from the GUI to remove tests from the queue

    :param tests: A list of tests to remove from the queue
    :type tests: [str]
    :return: A dictionary containing the current queue of the worker.
    :rtype: { queue: [str] }
    """
    log.debug(f"remove_from_queue called with tests: {tests}")
    worker.remove_from_queue(tests)
    eel.set_queue(worker.selected_tests)

### End eel functions ###
