import magic
import os
import subprocess

from celery import Celery
from celery_test.settings import *


app = Celery(
    APP_LABEL,
    broker=BROKER_URL,
    backend=BACKEND_URL
)


@app.task
def validate_file(filepath):
    if not os.path.isfile(filepath):
        return 'File not found.', 'error'
    file_header = magic.from_file(filepath)
    file_mimetype = magic.from_file(filepath, mime=True)

    if file_mimetype not in VALID_FILE_TYPE_HEADERS:
        os.unlink(filepath)
        return 'Invalid file type.', 'error'

    if not _file_valid(file_header, file_mimetype):
        os.unlink(filepath)
        return 'Invalid file type.', 'error'

    if not _file_infected(filepath):
        os.unlink(filepath)
        return 'File may be infected with a virus.', 'error'

    return 'File validation was successful.', 'success'


def _file_valid(file_header, file_mimetype):
    '''Checks whether the file's mimetype fits with our allowed signatures.'''

    for header in VALID_FILE_TYPE_HEADERS[file_mimetype]:
        if file_header.startswith(header):
            return True
    return False


def _file_infected(filepath):
    '''Call ClamScan on the file and see if it passes.'''

    try:
        proc = subprocess.run(['clamscan', filepath], capture_output=True)
    except FileNotFoundError:
        print('Antivirus is not installed.')
        return False

    result = proc.stdout
    if type(result) is bytes:
        result = result.decode('utf-8')

    if DEBUG:
        print(filepath)
        print(result)

    if not result.startswith(f'{filepath}: OK'):
        return False

    return True
