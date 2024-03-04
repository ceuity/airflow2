import json
import logging

from common.utils import slack


logger = logging.getLogger("airflow.task")


def success_callback(context):
    logger.info("Success callback")
    dag_id = context.get("dag").dag_id
    run_id = context.get("run_id")
    task_id = context.get("task_instance").task_id
    params = context.get("params")
    message = {
        "dag_id": dag_id,
        "run_id": run_id,
        "task_id": task_id,
        "params": params,
        "status": "success",
    }
    slack.send(json.dumps(message, indent=4))


def failure_callback(context):
    logger.info("Failure callback")
    dag_id = context.get("dag").dag_id
    run_id = context.get("run_id")
    task_id = context.get("task_instance").task_id
    params = context.get("params")
    exception = context.get("exception", "No exception")
    message = {
        "dag_id": dag_id,
        "run_id": run_id,
        "task_id": task_id,
        "params": params,
        "exception": exception,
        "status": "failure",
    }
    slack.send(json.dumps(message, indent=4))
