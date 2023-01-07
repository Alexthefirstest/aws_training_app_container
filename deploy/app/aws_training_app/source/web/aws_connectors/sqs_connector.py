import json

import boto3

from source import custom_constants


def send_message(message):
    sqs = boto3.client("sqs", region_name=custom_constants.AWS_DEFAULT_REGION)

    sqs.send_message(QueueUrl=custom_constants.SQS_QUEUE_URL, MessageBody=json.dumps(message))


def receive_message():
    sqs = boto3.client("sqs", region_name=custom_constants.AWS_DEFAULT_REGION)

    return sqs.receive_message(QueueUrl=custom_constants.SQS_QUEUE_URL, WaitTimeSeconds=20).get('Messages', [None])[0]


def delete_message(receipt_handle):
    sqs = boto3.client("sqs", region_name=custom_constants.AWS_DEFAULT_REGION)

    return sqs.delete_message(QueueUrl=custom_constants.SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
