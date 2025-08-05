import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("CLIENT")
DB_NAME = os.getenv("DB")

def get_collection(collection: str):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[collection]

def insert_questions(questions, collection: str, append: bool = True):
    collection = get_collection(collection)
    if questions:
        result = collection.insert_many(questions)
        print(f"{len(result.inserted_ids)} Documents insert into Database {DB_NAME}.{collection}.")
        
        if not append:
            delete_questions(collection, result.inserted_ids)
            print(f"Données insérées mais supprimées immédiatement (mode test).")
            
        return True
    else:
        print("No Question to add.")
        return False
    

def get_last_data(collection: str, limit: int=15):
    collection = get_collection(collection)
    return collection.find().sort([("_id", -1)]).limit(limit)

def delete_questions(collection: str, ids):
    result = collection.delete_many({"_id": {"$in": ids}})
    print(f"{result.deleted_count} documents supprimés dans {collection}.")
    return result.deleted_count