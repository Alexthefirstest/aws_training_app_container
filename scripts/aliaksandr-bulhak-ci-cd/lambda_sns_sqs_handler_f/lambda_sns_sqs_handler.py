import json
import os
import boto3


def lambda_handler(event, context):
    print('lambda start')
    initiator = event.get('detail-type', None)
    try:
        if not initiator:
            initiator = event['queryStringParameters']['detail-type']
    except KeyError:
        raise Exception("'?detail-type=something' should be specified in request url parameters")

    print('initiator:', initiator)

    res = sqs_to_sns_sender()

    return {
        'statusCode': 200,
        'body': json.dumps(res if res else 'sqs is empty')
    }


AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION_CUSTOM')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL')


def sqs_to_sns_sender():
    messages = sqs_receive_messages()
    all_messages = []
    while messages:
        all_messages.extend(messages)
        messages = sqs_receive_messages()
    to_publish = ''
    if all_messages:
        receipt_handlers = []
        for message in all_messages:
            to_publish += str(message['Body']) + ';\n\n'
            receipt_handlers.append(message['ReceiptHandle'])

        sns_publish(to_publish)
        sqs_delete_messages(receipt_handlers)
        return to_publish


def sqs_receive_messages():
    sqs = boto3.client("sqs", region_name=AWS_DEFAULT_REGION)

    return sqs.receive_message(QueueUrl=SQS_QUEUE_URL, MaxNumberOfMessages=10,
                               VisibilityTimeout=50, WaitTimeSeconds=5).get('Messages', None)


def sqs_delete_messages(receipt_handlers):
    sqs = boto3.client("sqs", region_name=AWS_DEFAULT_REGION)

    sqs.delete_message_batch(QueueUrl=SQS_QUEUE_URL,
                             Entries=[{'Id': str(rh_id), 'ReceiptHandle': receipt_handler}
                                      for rh_id, receipt_handler in enumerate(receipt_handlers)])


def sns_publish(message):
    sns = boto3.client("sns", region_name=AWS_DEFAULT_REGION)

    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message)
