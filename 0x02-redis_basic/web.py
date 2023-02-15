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
        """Calls get_page and caches result"""

        cached_key = "cached:{}".format(url)
        cached_data = redis.get(cached_key)
        if cached_data:
            return cached_data

        count_key = "count:{}".format(url)
        redis.incr(count_key, 1)

        html = func(url)
        redis.set(cached_key, html)
        redis.expire(cached_key, 10)

        return html

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
