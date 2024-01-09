import main_percentage as exec

# if __name__ == "__main__":
exec.logging.info(
    f"""
    Starting service with properties:
        OS_NAME: {exec.os.name}
        OS_SEP: {exec.os.sep}
        LOGGER_LEVEL: {exec.LOGGER_LEVEL}
        FILES_SUPPORTED: {exec.FILES_SUPPORTED}
        DIRECTORY_PATH: {exec.DIRECTORY_PATH}
        ROOT_DIRECTORY: {exec.ROOT_DIRECTORY}
        AWS_KEY_ID: ***
        AWS_SECRET_KEY: ***
        S3_NAME: {exec.S3_NAME}
    """
)

exec.run(enable_threads=True)

while exec.num_threads > 0:
    pass

exec.logging.debug(f'Files: {exec.FILES_COUNT}')
in_cloud = sum(list(map(lambda x: x['in_cloud'], list(exec.FILES_COUNT.values()))))
total = sum(list(map(lambda x: x['total'], list(exec.FILES_COUNT.values()))))
total_percentage = (in_cloud / total) * 100

exec.logging.info(
    f"""
    Files Statistic:
        Percentage in aws sync: {total_percentage}%
        Total local files: {total}
        Total in AWS: {in_cloud}
    """
)
