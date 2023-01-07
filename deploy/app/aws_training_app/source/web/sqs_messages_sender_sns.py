import requests

from source import custom_constants
from source.web import main_flask
from source.web import web_constants
from source.web.wrappers import exceptions_handler


@main_flask.route(web_constants.TRIGGER_SQS_SNS_SYNC)
@exceptions_handler
def push_messages_sqs_sns():
    response = requests.get(custom_constants.SNS_SQS_CONNECTOR_API_GATEWAY)
    return response.json()
