import logging

from common.utils import slack

logger = logging.getLogger("airflow.task")


def success_callback(context):
    logger.info("Success callback")
    slack.send(context)


def failure_callback(context):
    logger.info("Failure callback")
    logger.info(context)
    logger.info(context.get("conf"))
    logger.info(context.get("dag"))
    logger.info(context.get("dag_run"))
    logger.info(context.get("task"))
    message = context.get("exception", "No exception")
    slack.send(message)
