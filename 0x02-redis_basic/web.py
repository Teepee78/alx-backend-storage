#!/usr/bin/env python3
"""Defines the get_page function"""
from functools import wraps
from typing import Callable

import redis
import requests

store = redis.Redis()


def tracker(func: Callable) -> Callable:
    """Tracks how many times get_page is called"""

    @wraps(func)
    def wrapper(url: str) -> str:
        """Calls get_page and caches result"""

        # Increment counter
        count_key = "count:{}".format(url)
        store.incr(count_key)

        # Check if cached result exists
        cached_key = "cached:{}".format(url)
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # Call url and cache result for 10 seconds
        html = func(url)
        # Cache result
        store.set(cached_key, html)
        store.expire(cached_key, 10)

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

    return response.text
