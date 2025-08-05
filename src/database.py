import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("CLIENT")
DB_NAME = os.getenv("DB")
COLLECTION_NAME = os.getenv("COLLECTION")

def get_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def insert_questions(questions):
    collection = get_collection()
    if questions:
        result = collection.insert_many(questions)
        print(f"{len(result.inserted_ids)} Documents insert into Database {DB_NAME}.{COLLECTION_NAME}.")
        return True
    else:
        print("No Question to add.")
        return False
    

def get_last_data(limit: int=15):
    collection = get_collection()
    return collection.find().sort([("_id", -1)]).limit(limit)

def delete_questions(questions):
    collection = get_collection()