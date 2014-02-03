import pytest
import redis.connection

try:
    redis.connection.Connection().connect()
except redis.connection.ConnectionError:
    cant_connect = True
else:
    cant_connect = False


rq_redis = pytest.mark.skipif(cant_connect, reason="can't connect to Redis")
