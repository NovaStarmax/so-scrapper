from dotenv import load_dotenv
from src.database import get_collection
import os

load_dotenv()
COLLECTION_API = os.getenv("COLLECTION_API")
COLLECTION_SCRAPPER = os.getenv("COLLECTION_SCRAPPER")

def setup_indexes(collection: str):
    collection = get_collection(collection)
    collection.create_index("link", unique=True)
    print("Unique index on 'link' created on : ", collection)

if __name__ == "__main__":
    setup_indexes(COLLECTION_API)
    setup_indexes(COLLECTION_SCRAPPER)
