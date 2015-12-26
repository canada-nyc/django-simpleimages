from __future__ import absolute_import

import dill


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
    Calls ``function`` asynchronously by creating a pickling it and
    calling it in a task.
    '''
    from .tasks import dill_callable

    dilled_function = dill.dumps(function)
    dill_callable.delay(dilled_function, *args, **kwargs)
