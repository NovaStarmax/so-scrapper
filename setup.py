import os
from dotenv import load_dotenv
from pymongo import MongoClient
from src.database import get_collection
from handle_io.sync_db import synchronize

load_dotenv()

MONGO_URI = os.getenv("CLIENT", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB", "so-scrapper")
COLLECTIONS = ["api", "scrapper"]
COLLECTION_API = os.getenv("COLLECTION_API")
COLLECTION_SCRAPPER = os.getenv("COLLECTION_SCRAPPER")

def init_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    for name in COLLECTIONS:
        if name not in db.list_collection_names():
            db.create_collection(name)
            print(f"[✓] Collection '{name}' created.")
        else:
            print(f"[✓] Collection '{name}' already exists.")
    print(f"[✓] Database '{DB_NAME}' ready.")

def setup_indexes():
    for name in [COLLECTION_API, COLLECTION_SCRAPPER]:
        collection = get_collection(name)
        collection.create_index("link", unique=True)
        print(f"[✓] Unique index on 'link' created for: {name}")

def sync_json_to_db():
    synchronize("api.json", get_collection(COLLECTION_API))
    synchronize("scrapper.json", get_collection(COLLECTION_SCRAPPER))
    print(f"[✓] JSON sync to MongoDB complete.")

if __name__ == "__main__":
    print("== Project setup started ==")
    init_db()
    setup_indexes()
    sync_json_to_db()
