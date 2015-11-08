import pytest
from django_rq.queues import get_connection
import redis

try:
    get_connection().ping()
except redis.exceptions.ConnectionError:
    cant_connect = True
else:
    cant_connect = False


rq_redis = pytest.mark.skipif(cant_connect, reason="can't connect to Redis")
