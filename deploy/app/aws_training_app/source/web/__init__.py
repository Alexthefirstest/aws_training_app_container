from flask import Flask

main_flask = Flask(__name__)

from source.web import main_data
from source.web import region_zone_data
from source.web import images_handler
from source.web import email_subscription
from source.web import sqs_messages_sender_sns