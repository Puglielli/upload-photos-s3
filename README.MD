# Upload Photos to S3

# Running

## Export Environment Variables

### Powershell (Windows)
```
$env:AWS_KEY_ID='<AWS_KEY_ID>'
$env:AWS_SECRET_KEY='<AWS_SCRET_KEY>'
$env:DIRECTORY_PATH='<PHOTOS_DIRECTORY>'
$env:LOGGER_LEVEL='<LOGGER_LEVEL>'
```

### CMD (Windows)
```
set AWS_KEY_ID='<AWS_KEY_ID>'
set AWS_SECRET_KEY='<AWS_SCRET_KEY>'
set DIRECTORY_PATH='<PHOTOS_DIRECTORY>'
set LOGGER_LEVEL='<LOGGER_LEVEL>'
```

### Terminal (Mac/Linux)
```
export AWS_KEY_ID=<AWS_KEY_ID>
export AWS_SECRET_KEY=<AWS_SCRET_KEY>
export DIRECTORY_PATH='<PHOTOS_DIRECTORY>'
export LOGGER_LEVEL=<LOGGER_LEVEL>
```

## Run Script

### Upload
```
python exec_upload.py
```

### Percentage
```
python exec_percentage.py
```