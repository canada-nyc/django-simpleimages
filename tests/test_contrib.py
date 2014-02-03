from django.db import transaction

from django_rq import get_worker

from simpleimages.trackers import track_model

from .models import TestModel
from .conditions import rq_redis


@rq_redis
def test_rq(transactional_db, image, instance, settings):
    settings.SIMPLEIMAGES_TRANSFORM_CALLER = 'django_rq.enqueue'

    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)
    transaction.commit()
    get_worker().work(burst=True)
    disconnect()

    instance = instance.retrieve_from_database()
    assert instance.thumbnail
