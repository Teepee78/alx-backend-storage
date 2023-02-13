#!/usr/bin/env python3
"""
Defines the update_topics function
"""
from typing import List


def update_topics(mongo_collection, name: str, topics: List[str]):
    """Changes all topics of a school document based on the name

    Args:
        mongo_collection: mongodb collection
        name (str): school name
        topics (List[str]): list of topics
    """

    mongo_collection.update_many({
        "name": name
    }, {
        "$set": {
            "topics": topics
        }
    })
