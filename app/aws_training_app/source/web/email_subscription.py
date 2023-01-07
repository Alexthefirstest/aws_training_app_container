from flask import request

from source.web.aws_connectors import sns_connector
from source.web.main_data import main_flask
from source.web.wrappers import exceptions_handler


@main_flask.route('/email/subscription', methods=['POST'])
@exceptions_handler
def subscribe():
    params = request.get_json()
    if 'email' not in params.keys():
        raise Exception("email doesn't specified")

    email = params['email']

    sns_connector.subscribe(email)

    return {'email': email}


@main_flask.route('/email/subscription', methods=['DELETE'])
@exceptions_handler
def unsubscribe():
    params = request.get_json()
    if 'email' not in params.keys():
        raise Exception("email doesn't specified")

    email = params['email']

    sns_connector.unsubscribe(email)

    return {'email': email}
