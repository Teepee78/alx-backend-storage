#!/usr/bin/env python3
"""
Defines Cache class
"""
import uuid
from typing import Union

import redis


class Cache:
    """Implements a Cache in Redis"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key using uuid and stores the data in redis
        using the key

        Args:
            data: data to be stored in redis

        Returns:
            (str): the random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
