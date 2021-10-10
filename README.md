
# flask-celery-test
A project for learning Flask, Celery, and a refresher on decorators and other Python concepts.

## System requirements:
1. Redis Server
2. ClamAV
3. libmagic and related Python bindings
4. Python 3.8 and above

## Setting up
1. run "freshclam" to update ClamAV's viruses database
2. create a virtual environment for the project
3. activate and run "pip install -r requirements.txt"

## Running the application
1. on one terminal (while virtual env is active), run "python -m celery_test.app" for the Flask development server; points to 127.0.0.1:5000
2. on another terminal (also having the virutal env active), run "celery -A celery_test.tasks worker --loglevel=INFO"

## Notes
1. the Celery app is configured to have a backend so the Flask app decorators can fetch the results from it
2. the Celery broker and backend are defined as "redis://localhost"
3. file validation happens in 3 stages: a) the mimetype must be defined as a key in settings.VALID_FILE_TYPE_HEADERS; b) the file header/signature must start with one of the strings defined in the matching settings.VALID_FILE_TYPE_HEADERS item list values; c) virus scanning is made specifically for ClamAV but that is based on a class that can be overridden for other scanners in scanners.py
4. files that don't pass all 3 stages are deleted via os.unlink; valid files are kept in the specified UPLOAD_FOLDER in settings
5. the file description, as of this writing, goes nowhere; no databases are used in this application

## Ideas
1. when saving the temporary file, it might be a good idea to put it in a subfolder with a unique name or to suffix the file with the session ID to prevent clashes in case multiple users upload files with the same name
2. after a file passes validation, move it to somewhere permanent
3. add a simple DB to store more information about the file
4. try doing this in Django ;)
