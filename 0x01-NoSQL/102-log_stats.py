#!/usr/bin/env python3
"""
Reads logs from mongodb
"""
from pymongo import MongoClient

if __name__ == '__main__':
    collection = MongoClient("mongodb://127.0.0.1:27017").logs.nginx

    log_count = collection.count_documents({})
    print(f'{log_count} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_check} status check')
    
    top_ips = collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs:")
    for top_ip in top_ips:
        ip = top_ip.get("ip")
        count = top_ip.get("count")
        print(f'\t{ip}: {count}')
