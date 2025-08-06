import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError

load_dotenv()
MONGO_URI = os.getenv("CLIENT")
DB_NAME = os.getenv("DB")

def get_collection(collection: str):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[collection]

def insert_questions(questions: list, collection: str, append: bool = True):
    collection_obj = get_collection(collection)
    inserted_ids = []

    if not questions:
        print("No Question to add.")
        return False

    for q in questions:
        try:
            result = collection_obj.insert_one(q)
            inserted_ids.append(result.inserted_id)
        except DuplicateKeyError:
            pass

    print(f"{len(inserted_ids)} new documents inserted into Database {DB_NAME}.{collection} (duplicates ignored).")

    if not append and inserted_ids:
        delete_result = collection_obj.delete_many({"_id": {"$in": inserted_ids}})
        print(f"{delete_result.deleted_count} documents deleted (test mode).")

    return True

## Eda

def get_last_data(collection: str, limit: int=15):
    collection = get_collection(collection)
    return collection.find()
