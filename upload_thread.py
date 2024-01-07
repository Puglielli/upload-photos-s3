import upload

# if __name__ == "__main__":
upload.logging.info(
    f"""
    Starting service with properties:
        OS_NAME: {upload.os.name}
        OS_NODENAME: {upload.os.uname().nodename}
        OS_MACHINE: {upload.os.uname().machine}
        OS_SYSNAME: {upload.os.uname().sysname}
        OS_SEP: {upload.os.sep}
        LOGGER_LEVEL: {upload.LOGGER_LEVEL}
        FILES_SUPPORTED: {upload.FILES_SUPPORTED}
        DIRECTORY_PATH: {upload.DIRECTORY_PATH}
        ROOT_DIRECTORY: {upload.ROOT_DIRECTORY}
        AWS_KEY_ID: ***
        AWS_SECRET_KEY: ***
        S3_NAME: {upload.S3_NAME}
    """
)

upload.run(enable_threads=True)

while upload.num_threads > 0:
    pass
