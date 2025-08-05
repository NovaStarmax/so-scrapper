from pymongo import MongoClient

def vider_collection_scraper():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["so_scrapper_db"]
    result = db.scrapper.delete_many({})
    print(f"{result.deleted_count} documents supprimés de la collection 'scrapper'.")

if __name__ == "__main__":
    vider_collection_scraper()