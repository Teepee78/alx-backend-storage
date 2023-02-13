#!/usr/bin/env python3
"""
Defines the insert_school function
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into a collection

    Args:
        mongo_collection: collection
    """

    return mongo_collection.insert_one(kwargs).inserted_id
