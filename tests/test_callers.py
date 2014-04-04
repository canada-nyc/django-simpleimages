import pytest

from .conditions import rq_redis

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.usefixtures("track_model"),
]


@rq_redis
def test_rq(rq_caller, image, instance):
    instance.image.save(image.name, image.django_file)
    rq_caller()

    instance = instance.retrieve_from_database()
    assert instance.thumbnail


def test_pq(pq_caller, image, instance):
    instance.image.save(image.name, image.django_file)
    pq_caller()

    instance = instance.retrieve_from_database()
    assert instance.thumbnail
