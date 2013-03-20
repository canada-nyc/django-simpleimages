import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from . import utils


logger = logging.getLogger(__name__)


def track_model(model):
    logger.debug('Tracking images on model {}'.format(model))

    @receiver(pre_save, sender=model, weak=False, dispatch_uid='simpleimages')
    def transform_signal(sender, **kwargs):
        logger.debug('Retransforming image fields on model {}'.format(kwargs['instance']))
        utils.perform_transformation(
            [kwargs['instance']],
            kwargs['update_fields']
        )

    def disconnect():
        pre_save.disconnect(sender=model, dispatch_uid='simpleimages')
    return disconnect
