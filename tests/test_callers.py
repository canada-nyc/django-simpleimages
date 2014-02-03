from simpleimages.trackers import track_model

from .models import TestModel
from .conditions import rq_redis


@rq_redis
def test_rq(rq, image, instance):
    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)
    rq()
    disconnect()

    instance = instance.retrieve_from_database()
    assert instance.thumbnail
