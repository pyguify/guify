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
    log.debug(f"run_tests called with tests: {tests}, params: {params}")
    if worker.state != WAITING_FOR_RUN:
        return {"error": f"Worker is currenty busy, Status: {worker.state}"}
    else:
        try:
            worker.start(tests, params)
        except Exception as exc:
            return {"error": f"Error: {exc}"}
        else:
            return {
                "state": worker.state,
                "currentJob": worker.currently_running,
                "prompt": worker.prompt
            }


@eel.expose
def all_tests():
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
def worker_status():
    log.debug(f"worker_status called")
    return {
        "state": worker.state,
        "currentJob": worker.currently_running,
        "prompt": worker.prompt
    }


@eel.expose
def current_job_params():
    log.debug(f"current_job_params called")
    if worker.currently_running is None:
        return {"params": {}}  # No job is running
    return {"params": worker.params}


@eel.expose
def all_params():
    log.debug(f"all_params called")
    all_params = list(worker.pool.required_params)
    all_params.sort()
    return {"params": all_params}


@eel.expose
def answer_prompt(response):
    log.debug(f"answer_prompt called with response: {response}")
    if response not in [OK, CANCEL]:
        return {"error": f"Invalid response: {response}"}
    else:
        if worker.state == PENDING_USER_INPUT or worker.state == DONE:
            worker.answer_prompt(response)
            return {
                "status": {
                    "state": worker.state,
                    "currentJob": worker.currently_running,
                    "prompt": worker.prompt
                }
            }
        else:
            return {"error": f"Worker is not waiting for user input"}


@eel.expose
def get_monitor_text():
    log.debug(f"get_monitor_text called")
    return worker.monitor.text


@eel.expose
def get_config():
    log.debug(f"get_config called")
    return {'config': worker.config_tab.load()}


@eel.expose
def save_config(config: dict):
    log.debug(f"save_config called with config: {config}")
    worker.config_tab.save(config)
    return {'config': worker.config_tab.load()}

### End eel functions ###
