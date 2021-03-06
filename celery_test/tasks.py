import magic
import os

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
        return TASK_MESSAGES['file_not_found']
    file_header = magic.from_file(filepath)
    file_mimetype = magic.from_file(filepath, mime=True)

    if file_mimetype not in VALID_FILE_TYPE_HEADERS:
        os.unlink(filepath)
        return TASK_MESSAGES['file_invalid']

    if not _file_valid(file_header, file_mimetype):
        os.unlink(filepath)
        return TASK_MESSAGES['file_invalid']

    scanner = ACTIVE_SCANNER(filepath)

    if not scanner.evaluate_result():
        os.unlink(filepath)
        return TASK_MESSAGES['file_infected']

    return TASK_MESSAGES['file_valid']


def _file_valid(file_header, file_mimetype):
    '''Checks whether the file's mimetype fits with our allowed signatures.'''

    for header in VALID_FILE_TYPE_HEADERS[file_mimetype]:
        if file_header.startswith(header):
            return True
    return False
