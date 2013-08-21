from django.db.models.signals import post_save
from django.dispatch import receiver

import simpleimages.utils


def track_model(model):
    '''
    Perform designated transformations on model, when it saves.

    Calls :py:func:`~simpleimages.utils.perform_transformation`
    on every model saves using
    :py:data:`django.db.models.signals.post_save`.

    It uses the ``update_fields`` kwarg to tell what fields it should
    transform.
    '''
    @receiver(post_save, sender=model, weak=False, dispatch_uid='simpleimages')
    def transform_signal(sender, **kwargs):
        simpleimages.utils.perform_transformation(
            kwargs['instance'],
            kwargs['update_fields']
        )

    def disconnect():
        post_save.disconnect(sender=model, dispatch_uid='simpleimages')
    return disconnect
