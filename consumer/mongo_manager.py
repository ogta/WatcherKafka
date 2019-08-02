from pymongo import MongoClient
import uuid
import os

def db_manager():
    MONGO_IP = os.environ.get("MONGO_IP")
    MONGO_PORT = int(os.environ.get("MONGO_PORT"))
    MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    MONGO_DATABASE = os.environ.get("MONGO_DATABASE")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")
    client = MongoClient(MONGO_IP, MONGO_PORT,username=MONGO_USERNAME, password=MONGO_PASSWORD)
    return client[MONGO_DATABASE][MONGO_COLLECTION]


def insert(log):
    try:
        data = str(log).split()
        date = data[0]
        time = data[1]
        log_level = data[2]
        message = data[3]
        original_data = log

        service_data = {
            "_id" : str(uuid.uuid4()),
            "date" : date,
            "time" : time,
            "log_level" : log_level,
            "message" : message,
            "original_data" : original_data
        }

        db_manager().insert_one(service_data)
        return 1
    except():

        return 0