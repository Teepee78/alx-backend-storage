#!/usr/bin/env python3
"""
Defines Cache class
"""
import uuid
from typing import Any, Callable, Union

import redis


class Cache:
    """Implements a Cache in Redis"""

    def __init__(self):
        """Initializes redis cache"""
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

    def get(self, key: str, fn: Callable = None) -> Any:
        """Gets an item from redis using the given key

        Args:
            key (str): key of the item
            fn (Callable, optional): function to convert item to desired type. Defaults to None.

        Returns:
            Any: Converted item or byte
        """

        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Gets an item from redis using given key

        Args:
            key (str): key of the item

        Returns:
            str: item converted to str
        """

        data = self._redis.get(key)
        if data is None:
            return None

        return str(data)

    def get_int(self, key: str) -> int:
        """Gets an item from redis using given key

        Args:
            key (str): key of the item

        Returns:
            int: item converted to int
        """

        data = self._redis.get(key)
        if data is None:
            return None

        return int(data)