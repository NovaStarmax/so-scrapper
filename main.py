import sys
import os
# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
# sys.path.append(os.path.join(os.path.dirname(__file__), "handle_io"))
from dotenv import load_dotenv
from src.database import get_collection
from handle_io.sync_db import synchronize

load_dotenv()
COLLECTION_API = os.getenv("COLLECTION_API")
COLLECTION_SCRAPPER = os.getenv("COLLECTION_SCRAPPER")

def setup_indexes(collection: str):
    collection = get_collection(collection)
    collection.create_index("link", unique=True)
    print("Unique index on 'link' created on : ", collection)

if __name__ == "__main__":
    # setup_indexes(COLLECTION_API)
    # setup_indexes(COLLECTION_SCRAPPER)
    synchronize("api.json", get_collection(COLLECTION_API))
    synchronize("scrapper.json", get_collection(COLLECTION_SCRAPPER))
    # append_new_documents_to_json("scrapper.json", get_collection(COLLECTION_SCRAPPER))