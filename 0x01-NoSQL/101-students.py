#!/usr/bin/env python3
"""
Defines the top_students function
"""


def top_students(mongo_collection):
	"""Returns all students sorted by average score

	Args:
		mongo_collection: collection object
	"""

	return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
