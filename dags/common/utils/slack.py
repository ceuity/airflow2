import logging
import os

import requests

logger = logging.getLogger("airflow.task")

TOKEN = os.environ.get("SLACK_API_TOKEN")
CHANNEL = os.environ.get("SLACK_CHANNEL")


def send(message):
    try:
        token = TOKEN
        channel = CHANNEL
        text = f"{message}"
        data = {
            "Content-Type": "application/x-www-form-urlencoded",
            "token": token,
            "channel": channel,
            "text": text,
        }

        response = requests.post("https://slack.com/api/chat.postMessage", data=data)
        if response is None:
            raise Exception("None response")
        if response.status_code != requests.codes.ok:
            raise Exception(f"{response.status_code} response")
        if response.content is None:
            raise Exception("None Content response")

        logger.info(f"slack.send() : info = {response.json()}")

    except Exception as e:
        logger.error(f"slack.send() : e = {e}")

    return response
