def default(function, *args, **kwargs):
    '''
    Calls ``function`` with any passed in ``args`` and ``kwargs.
    '''
    function(*args, **kwargs)


def _no_action(function, *args, **kwargs):
    '''
    Does nothing. For testing.
    '''
    pass


def celery(function, *args, **kwargs):
    '''
    Calls ``function`` asynchronously by creating a
    `shared-task <http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-the-shared-task-decorator>`_
    with celery.
    '''
    from celery import shared_task
    shared_task(function).delay(*args, **kwargs)
