def lambda_handler(event, context):
    bucket=event['Records'][0]['s3']['bucket']['name']
    file=event['Records'][0]['s3']['object']['key']
    print('bucket name:', bucket)
    print('downloaded file path:', file)
