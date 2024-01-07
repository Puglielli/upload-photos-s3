import percentage

# if __name__ == "__main__":
percentage.logging.info(
    f"""
    Starting service with properties:
        OS_NAME: {percentage.os.name}
        OS_NODENAME: {percentage.os.uname().nodename}
        OS_MACHINE: {percentage.os.uname().machine}
        OS_SYSNAME: {percentage.os.uname().sysname}
        OS_SEP: {percentage.os.sep}
        LOGGER_LEVEL: {percentage.LOGGER_LEVEL}
        FILES_SUPPORTED: {percentage.FILES_SUPPORTED}
        DIRECTORY_PATH: {percentage.DIRECTORY_PATH}
        ROOT_DIRECTORY: {percentage.ROOT_DIRECTORY}
        AWS_KEY_ID: ***
        AWS_SECRET_KEY: ***
        S3_NAME: {percentage.S3_NAME}
    """
)

percentage.run(enable_threads=True)

while percentage.num_threads > 0:
    pass

percentage.logging.debug(f'Files: {percentage.FILES_COUNT}')
in_cloud = sum(list(map(lambda x: x['in_cloud'], list(percentage.FILES_COUNT.values()))))
total = sum(list(map(lambda x: x['total'], list(percentage.FILES_COUNT.values()))))
total_percentage = (in_cloud / total) * 100

percentage.logging.info(
    f"""
    Files Statistic:
        Percentage in aws sync: {total_percentage}%
        Total local files: {total}
        Total in AWS: {in_cloud}
    """
)
