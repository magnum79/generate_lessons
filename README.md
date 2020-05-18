# generate_lessons

## After cloning install dependecies using virtualenv:

```console
ls -la /opt/python/*/bin/python
/opt/python/python-3.7.6/bin/python -m venv googleenv
source googleenv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt --upgrade
deactivate
```

## credentials.json
To run script generate **credentials.json**, as described in [dependency docs](https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md)

## config.ini
Rename **config.ini.example** and specify your **your_spreadsheet_id**, sheet range and destination folder

```
# The ID and range of a spreadsheet.
SPREADSHEET_ID = your_spreadsheet_id
RANGE_NAME = 'Sheet1'!A1:F

# Destination folder
lesson_dir = /var/www/html/some_dir/
```