# Test for A.P.I
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")

# Liste des bases de données
print(client.list_database_names())
db = client["so_scrapper_db"]
collection = db["api"]
# Liste des collections
print(db.list_collection_names())


print("Nombre de documents :", collection.count_documents({}))
for doc in collection.find().limit(5):
    print(doc)
