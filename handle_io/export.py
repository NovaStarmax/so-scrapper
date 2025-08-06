from pymongo import MongoClient
import json

# Connexion à MongoDB local
client = MongoClient("mongodb://localhost:27017")
db = client["so_scrapper_db"]
collection = db["api"]

# Récupération des documents
data = list(collection.find())

# Export vers un fichier JSON (liste d'objets)
with open("handle_io/export.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, default=str)

print(f"{len(data)} documents exportés dans export_api.json")

