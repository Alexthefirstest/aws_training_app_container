BASE_DATABASE_NAME = 'images_handler_db'
DB_HOST = r'aliaksandr-bulhak-rds.c4dotvhilt7y.us-west-2.rds.amazonaws.com'
# DB_HOST = r'localhost'
DB_USERNAME = r'python_user'
DB_PASSWORD = r'aa_paRnasdfliweh#52k'

AWS_DEFAULT_REGION = 'us-west-2'

S3_BUCKET_NAME = r'aliaksandr-bulhak-for-ec2'
S3_BASE_FILE_PATH = r'images/'

SNS_TOPIC_ARN = r'arn:aws:sns:us-west-2:763233212644:aliaksandr-bulhak-sns'

SQS_QUEUE_URL = r'https://sqs.us-west-2.amazonaws.com/763233212644/aliaksandr-bulhak-sqs'

SNS_SQS_CONNECTOR_API_GATEWAY = r'https://0057rnw1zi.execute-api.us-west-2.amazonaws.com/ab-batch-notifier?detail-type=application'
