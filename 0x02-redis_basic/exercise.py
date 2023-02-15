#!/usr/bin/env python3
"""
Defines Cache class
"""
import uuid
from functools import wraps
from typing import Any, Callable, Union

import redis


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to Cache methods

    Args:
        method (Callable): method

    Returns:
        Callable: Callable
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, data):
        """Increments the counter and calls the method"""
        self._redis.incr(key, 1)
        return method(self, data)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a particular function.

    Everytime the original function will be called, we will add its input parameters to one list in redis,
    and store its output into another list

    Args:
        method (Callable): method to wrap

    Returns:
        Callable: Callable
    """

    input = method.__qualname__ + ":inputs"
    output = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args):
        """Wrapper function"""

        self._redis.rpush(input, str(args))

        ret = method(self, *args)
        self._redis.rpush(output, ret)
        return ret

    return wrapper


def replay(method: Callable):
    """Replays the history of a cached function

    Args:
        method (Callable): method
    """
    redis = redis.Redis()
    redis.flushdb()

    key = method.__qualname__

    # Print how many times method was called
    count = redis.get(key)
    try:
        count = int(c.decode("utf-8"))
    except Exception:
        count = 0
    print("{} was called {} times".format(key, count.decode("utf8")))

    # Get inputs and outputs
    inputs = redis.lrange("{}:inputs".format(key), 0, -1)
    outputs = redis.lrange("{}:outputs".format(key), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(key, inp, outp))


class Cache:
    """Implements a Cache in Redis"""

    def __init__(self):
        """Initializes redis cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
