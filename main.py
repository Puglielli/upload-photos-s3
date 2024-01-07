import os
import re

import boto3
from botocore.errorfactory import ClientError

FILES_SUPPORTED = 'JPG|PNG|JPEG'
LOGGER_ENABLED = os.getenv('LOGGER_ENABLED', True)
DIRECTORY_PATH = os.getenv('DIRECTORY_PATH', './photos')
S3_NAME = os.getenv('BUCKET_NAME', 'elocs-backend-331514516496')


def log(enabled: bool = LOGGER_ENABLED, text: any = ''):
    if enabled:
        print(text)


def upload(client, path, bucket):
    global num_thread
    num_thread += 1

    folders = DIRECTORY_PATH.split('\\')
    last_folder = folders[len(folders) - 1]
    remaining = path.replace(DIRECTORY_PATH, "").removeprefix('\\')
    key = f'{last_folder}/{remaining}'
    print(f'rem: {remaining}')

    try:
        # client.head_object(Bucket=bucket, Key=key)
        log(text=f'File {key} already exists')
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            log(text=f'File not founded: {key}')
            # client.upload_file(path, bucket, key)
        elif e.response['Error']['Code'] == 403:
            print(f'Not authorized to upload file: {key}; Error: {e}')
        else:
            print(f'Error: {e}')
            raise
    num_thread -= 1


def create_key(path):
    pass


def run(root_path, bucket_name):
    s3 = boto3.client(
        service='s3',
        aws_access_key_id='AKIAU2L6OCQIKQ2GGEVT',
        aws_secret_access_key='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'
    )

    for root, dirs, files in os.walk(root_path):
        for file in files:
            if re.match(pattern=f".*({FILES_SUPPORTED})$", string=file.upper()):
                path_full = os.path.join(root, file).removeprefix('./')
                folders = root_path.split('/')
                last_folder = folders[len(folders) - 1]
                remaining = path_full.replace(path, "").removeprefix('/')
                key = f'{last_folder}/{remaining}'
                print(f'rem: {remaining}')

                try:
                    # s3.head_object(Bucket=bucket_name, Key=key)
                    log(text=f'File {key} already exists')
                except ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        log(text=f'File not founded: {key}')
                        # s3.upload_file(key, bucket_name, key)
                    elif e.response['Error']['Code'] == 403:
                        log(enabled=True, text=f'Not authorized to upload file: {key}; Error: {e}')
                    else:
                        log(enabled=True, text=f'Error: {e}')
                        raise
                except Exception as e:
                    print('')


if __name__ == "__main__":
    run(root_path=DIRECTORY_PATH, bucket_name=S3_NAME)
