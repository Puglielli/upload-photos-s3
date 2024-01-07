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

FILES_COUNT = {}


def build_client():
    return boto3.client(
        service_name='s3',
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
    )


def get_paths(path):
    remaining = path.replace(DIRECTORY_PATH, '').replace(os.sep, '/')
    root_directory = ROOT_DIRECTORY if ROOT_DIRECTORY is not None else DIRECTORY_PATH.split(os.sep).pop()

    return {
        'root': root_directory,
        'remaining': remaining,
        'key': f'{root_directory}{remaining}',
    }


def count_files(client, bucket, file_name, paths, size):
    key = paths['key']
    directory = f"{paths['root']}{paths['remaining'].replace(file_name, '')}"
    files_directory = FILES_COUNT.get(directory, {'total': size})
    try:
        client.head_object(Bucket=bucket, Key=key)
        in_cloud = files_directory.get('in_cloud', 0)
        in_cloud += 1
        files_directory['in_cloud'] = in_cloud
        FILES_COUNT[directory] = files_directory

    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.debug(f'File not founded: {key}')
        elif e.response['Error']['Code'] == 403:
            logging.error(f'Not authorized to upload file;\n {key}; Error: {e}', stack_info=True)
        else:
            logging.error(f'S3 Error: {e}', stack_info=True)
            raise
    except Exception as e:
        logging.error(f'Exception Error: {e}')


def run(root_path, bucket_name):
    try:
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if re.match(pattern=f".*({FILES_SUPPORTED})$", string=file.upper()):
                    path = os.path.join(root, file)
                    paths = get_paths(path=path)
                    only_photos = list(
                        filter(lambda x: re.match(pattern=f".*({FILES_SUPPORTED})$", string=x.upper()), files))

                    logging.debug(f'Paths: {paths}')

                    count_files(
                        client=build_client(),
                        bucket=bucket_name,
                        file_name=file,
                        paths=paths,
                        size=len(only_photos)
                    )
    except Exception as e:
        logging.error(f"Error: {e}", stack_info=True)


if __name__ == "__main__":
    logging.info(
        f"""
        Starting service with properties:
            OS_NAME: {os.name}
            OS_NODENAME: {os.uname().nodename}
            OS_MACHINE: {os.uname().machine}
            OS_SYSNAME: {os.uname().sysname}
            OS_SEP: {os.sep}
            LOGGER_LEVEL: {LOGGER_LEVEL}
            FILES_SUPPORTED: {FILES_SUPPORTED}
            DIRECTORY_PATH: {DIRECTORY_PATH}
            ROOT_DIRECTORY: {ROOT_DIRECTORY}
            AWS_KEY_ID: ***
            AWS_SECRET_KEY: ***
            S3_NAME: {S3_NAME}
        """
    )
    run(root_path=DIRECTORY_PATH, bucket_name=S3_NAME)
    logging.debug(f'Files: {FILES_COUNT}')
    in_cloud = sum(list(map(lambda x: x['in_cloud'], list(FILES_COUNT.values()))))
    total = sum(list(map(lambda x: x['total'], list(FILES_COUNT.values()))))
    percentage = (in_cloud / total) * 100
    logging.info(
        f"""
        Files Statistic:
            Percentage in aws sync: {percentage}%
            Total local files: {total}
            Total in AWS: {in_cloud}
        """
    )
