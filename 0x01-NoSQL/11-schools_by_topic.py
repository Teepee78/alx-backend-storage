#!/usr/bin/env python3
"""
Defines the schools_by_topic function
"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of schools having a specific topic

    Args:
        mongo_collection: mongodb collection
        topic: topic
    """

    return mongo_collection.find({"topics": {"$in": [topic]}})
