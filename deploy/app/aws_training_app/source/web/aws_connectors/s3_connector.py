import boto3

from source import custom_constants


def upload_to_s3(file):
    s3client = boto3.client('s3')
    s3client.upload_fileobj(file, custom_constants.S3_BUCKET_NAME, custom_constants.S3_BASE_FILE_PATH + file.filename)


def download_from_s3(filename, file_ext):
    s3client = boto3.client('s3')
    return s3client.get_object(Bucket=custom_constants.S3_BUCKET_NAME,
                               Key=f'{custom_constants.S3_BASE_FILE_PATH}{filename}.{file_ext}')['Body'].read()


def delete_from_s3(filename, file_ext):
    s3client = boto3.client('s3')
    s3client.delete_object(Bucket=custom_constants.S3_BUCKET_NAME,
                           Key=f'{custom_constants.S3_BASE_FILE_PATH}{filename}.{file_ext}')
