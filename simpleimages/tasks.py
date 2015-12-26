from celery import shared_task
import dill


@shared_task
def dill_callable(dilled_callable, *args, **kwargs):
    callable = dill.loads(dilled_callable)
    return callable(*args, **kwargs)
