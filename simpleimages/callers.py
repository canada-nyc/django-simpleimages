from django.db import DatabaseError


def default(function, *args, **kwargs):
    '''
    Calls ``function`` with any passed in ``args`` and ``kwargs.
    '''
    function(*args, **kwargs)


def _no_action(function, *args, **kwargs):
    pass


def pq(function, *args, **kwargs):
    '''
    Adds ``function`` to the `django-pq <https://github.com/bretth/django-pq>`_
    default queue, with any passed in
    ``args`` and ``kwargs`` It will create this queue if it doesn't exist.
    '''
    from pq.queue import Queue
    queue = Queue.create()
    # Try to create the queue table, but if the database isn't set up yet
    # then don't create it
    try:
        queue.save()
    except DatabaseError:
        pass

    queue.enqueue(function, *args, **kwargs)
