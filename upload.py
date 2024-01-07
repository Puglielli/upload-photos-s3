import _thread
import logging
import os
import re

import boto3
from botocore.errorfactory import ClientError

LOGGER_LEVEL = os.getenv('LOGGER_LEVEL', logging.INFO)
logging.basicConfig(encoding='utf-8', level=LOGGER_LEVEL, format='%(asctime)s %(message)s')

FILES_SUPPORTED = os.getenv('FILES_SUPPORTED', 'JPG|PNG|JPEG')
DIRECTORY_PATH = os.getenv('DIRECTORY_PATH')
ROOT_DIRECTORY = os.getenv('ROOT_DIRECTORY', None)
AWS_KEY_ID = os.getenv('AWS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_NAME = os.getenv('BUCKET_NAME', 'elocs-backend-331514516496')

# Threads
num_threads = 0


def build_client():
    return boto3.client(
        service_name='s3',
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
    )


def create_key(path):
    remaining = path.replace(DIRECTORY_PATH, '').replace(os.sep, '/')
    root_directory = ROOT_DIRECTORY if ROOT_DIRECTORY is not None else DIRECTORY_PATH.split(os.sep).pop()

    return f'{root_directory}{remaining}'


def upload(client, bucket, path, key):
    global num_threads
    num_threads += 1

    try:
        client.head_object(Bucket=bucket, Key=key)
        logging.debug(f'File {key} already exists')
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.debug(f'File not founded: {key}')
            client.upload_file(path, bucket, key)
        elif e.response['Error']['Code'] == 403:
            logging.error(f'Not authorized to upload file;\n {key}; Error: {e}', stack_info=True)
        else:
            logging.error(f'S3 Error: {e}', stack_info=True)
            raise
    except Exception as e:
        logging.error(f'Exception Error: {e}')

    num_threads -= 1


def run(root_path=DIRECTORY_PATH, bucket_name=S3_NAME, enable_threads=False):
    try:
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if re.match(pattern=f".*({FILES_SUPPORTED})$", string=file.upper()):
                    path = os.path.join(root, file)
                    key = create_key(path=path)

                    logging.debug(f'Path: {path}; Key: {key}')

                    if enable_threads:
                        _thread.start_new_thread(upload, (build_client(), bucket_name, path, key))
                    else:
                        upload(client=build_client(), bucket=bucket_name, path=path, key=key)
    except Exception as e:
        logging.error(f"Error: {e}", stack_info=True)
