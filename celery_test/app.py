import os

from flask import Flask, Response, flash, redirect, render_template, request
from werkzeug.utils import secure_filename

from celery_test.decorators import (
    check_task_blocked,
    check_task_status
)
from celery_test.settings import *
from celery_test.tasks import validate_file


app = Flask(
    APP_LABEL,
    static_folder=STATIC_FOLDER,
    template_folder=TEMPLATE_FOLDER
)
app.secret_key = SECRET_KEY
app.config['upload_folder'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
@check_task_status
def index():
    context = {'page_title': 'My Celery Test App'}
    return Response(render_template('base.html', **context))


@app.route('/upload', methods=['POST'])
@check_task_blocked
def upload():
    uploaded_file = request.files.get('uploaded-file')
    uploaded_description = request.form.get('uploaded-description')
    response = redirect('/')

    if not uploaded_file or not uploaded_description:
        flash('A file and description are required.', 'error')
        return response

    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(app.config['upload_folder'], filename)
    uploaded_file.save(filepath)

    task = validate_file.delay(filepath)
    response.set_cookie(CELERY_TASK_CHECK_COOKIE, task.task_id)

    return response


if __name__ == '__main__':
    app.run(debug=DEBUG)
