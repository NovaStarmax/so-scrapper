import os
from dotenv import load_dotenv
from src.database import get_collection
from handle_io.sync_db import synchronize
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

load_dotenv()
COLLECTION_API = os.getenv("COLLECTION_API", "COLLECTION_API")
COLLECTION_SCRAPPER = os.getenv("COLLECTION_SCRAPPER", "COLLECTION_SCRAPPER")

if __name__ == "__main__":
    synchronize("api.json", get_collection(COLLECTION_API))
    synchronize("scrapper.json", get_collection(COLLECTION_SCRAPPER))