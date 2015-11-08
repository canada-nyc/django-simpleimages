import pytest
import django_rq
import simpleimages.callers
import simpleimages.utils

from .conditions import rq_redis

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.usefixtures("track_model"),
]


def test_setting_caller(settings):
    settings.SIMPLEIMAGES_TRANSFORM_CALLER = 'simpleimages.callers._no_action'
    assert simpleimages.utils.get_caller() == simpleimages.callers._no_action


def test_no_action(settings, image, instance_no_image):
    settings.SIMPLEIMAGES_TRANSFORM_CALLER = 'simpleimages.callers._no_action'

    instance_no_image.image.save(image.name, image.django_file)
    instance_no_image = instance_no_image.retrieve_from_database()
    assert not instance_no_image.thumbnail


@rq_redis
def test_rq(settings, image, instance_no_image):
    settings.SIMPLEIMAGES_TRANSFORM_CALLER = 'django_rq.enqueue'

    instance_no_image.image.save(image.name, image.django_file)

    django_rq.get_worker().work(burst=True)

    instance_no_image = instance_no_image.retrieve_from_database()
    assert instance_no_image.thumbnail


def test_celery(settings, image, instance_no_image):
    settings.SIMPLEIMAGES_TRANSFORM_CALLER = 'simpleimages.callers.celery'
    settings.CELERY_ALWAYS_EAGER = True

    instance_no_image.image.save(image.name, image.django_file)
    instance_no_image = instance_no_image.retrieve_from_database()
    assert instance_no_image.thumbnail
