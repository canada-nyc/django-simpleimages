from django.db.models.signals import post_save
from django.dispatch import receiver

from . import utils


def track_model(model):
    @receiver(post_save, sender=model, weak=False, dispatch_uid='simpleimages')
    def transform_signal(sender, **kwargs):
        utils.perform_transformation(
            [kwargs['instance']],
            kwargs['update_fields']
        )

    def disconnect():
        post_save.disconnect(sender=model, dispatch_uid='simpleimages')
    return disconnect
