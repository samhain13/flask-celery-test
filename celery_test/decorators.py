from flask import flash, redirect, request

from celery_test.settings import CELERY_TASK_CHECK_COOKIE
from celery_test.tasks import app as celery_app


def check_task_status(func):
    '''
    Check if the user has a celery task ongoing and if so, see if it is done
    and clean up. Otherwise, let the user continue with what he is doing.
    '''
    def check_task_status_wrapper(*args, **kwargs):
        task_id = request.cookies.get(CELERY_TASK_CHECK_COOKIE)
        if task_id is not None:
            task = celery_app.AsyncResult(task_id)
            if task.ready():
                flash(*task.get())
                task.forget()
                response = func(*args, **kwargs)
                response.set_cookie(CELERY_TASK_CHECK_COOKIE, expires=0)
                return response
            else:
                flash('Your background task is running.', 'info')
        return func(*args, **kwargs)
    return check_task_status_wrapper


def check_task_blocked(func):
    '''
    Prevent the user from initiating a new task by uploading a new file if
    there is still a pending task in the background.
    '''
    def check_task_blocked_wrapper(*args, **kwargs):
        task_id = request.cookies.get(CELERY_TASK_CHECK_COOKIE)
        if task_id is not None:
            flash('You still have a pending task, try again later.', 'error')
            return redirect('/')
        return func(*args, **kwargs)
    return check_task_blocked_wrapper
