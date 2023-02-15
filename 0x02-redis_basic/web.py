#!/usr/bin/env python3
"""Defines the get_page function"""
from functools import wraps
from typing import Callable

import redis
import requests


def tracker(func: Callable) -> Callable:
    """Tracks how many times get_page is called"""

    redis = redis.Redis()

    @wraps(func)
    def wrapper(url):
        """Calls get_page and caches url"""

        key = "count:{}".format(url)
        redis.incr(key, 1)
        redis.expire(key, 10)

        return func(url)

    return wrapper


@tracker
def get_page(url: str) -> str:
    """Uses requests module to obtain the html content of a URL

    Args:
        url (str): url of the page

    Returns:
        str: returns html content
    """

    response = requests.get(url)

    return response.content
