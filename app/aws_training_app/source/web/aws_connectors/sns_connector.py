import boto3

from source import custom_constants


def subscribe(email):
    sns = boto3.client("sns", region_name=custom_constants.AWS_DEFAULT_REGION)

    sns.subscribe(TopicArn=custom_constants.SNS_TOPIC_ARN, Protocol="email", Endpoint=email.lower())


def unsubscribe(email=''):
    email = email.lower()
    sns = boto3.client("sns", region_name=custom_constants.AWS_DEFAULT_REGION)

    response = sns.list_subscriptions_by_topic(TopicArn=custom_constants.SNS_TOPIC_ARN)

    for subscription in response["Subscriptions"]:
        if subscription['Endpoint'] == email:
            sns.unsubscribe(SubscriptionArn=subscription['SubscriptionArn'])
            return
    raise Exception("email isn't subscribed")


def publish(message):
    sns = boto3.client("sns", region_name=custom_constants.AWS_DEFAULT_REGION)

    sns.publish(TopicArn=custom_constants.SNS_TOPIC_ARN, Message=message)
