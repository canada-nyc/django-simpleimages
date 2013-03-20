from django.db.models.signals import pre_save
from django.dispatch import receiver

from . import utils


def track_model(model):
    @receiver(pre_save, sender=model, weak=False, dispatch_uid='simpleimages')
    def transform_signal(sender, **kwargs):
        utils.perform_transformation(
            [kwargs['instance']],
            kwargs['update_fields']
        )

    def disconnect():
        pre_save.disconnect(sender=model, dispatch_uid='simpleimages')
    return disconnect
