from celery_test.scanners import ClamScan


ACTIVE_SCANNER = ClamScan
APP_LABEL = 'celery_test_app'
BACKEND_URL = 'redis://localhost'
BROKER_URL = 'redis://localhost'
CELERY_TASK_CHECK_COOKIE = 'celery-task-id'
DEBUG = True
SECRET_KEY = 'fl4Sk!t3st1nG'
STATIC_FOLDER = 'celery_test/static'
TASK_MESSAGES = {
    'file_infected': ('File may be infected with a virus.', 'error'),
    'file_invalid': ('Invalid file type.', 'error'),
    'file_not_found': ('File not found.', 'error'),
    'file_valid': ('File validation was successful.', 'success'),
    'task_pending': ('You still have a pending task, try again later.', 'error'),
    'task_running': ('Your background task is running.', 'info'),
}
TEMPLATE_FOLDER = 'celery_test/templates'
UPLOAD_FOLDER = '/tmp'
VALID_FILE_TYPE_HEADERS = {
    'application/pdf': ['PDF document'],
    'image/jpeg': ['JPEG image data'],
    'image/png': ['PNG image data'],
    'text/plain': ['ASCII text'],
    # add more here
}
