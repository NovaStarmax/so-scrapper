from pymongo import MongoClient
import json

# Connexion à MongoDB local
client = MongoClient("mongodb://localhost:27017")
db = client["so_scrapper_db"]
collection = db["api"]




# Charger les documents exportés
with open("handle_io/export.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Compteur
added_count = 0

# Récupérer tous les liens existants en base
existing_links = set(doc["link"] for doc in collection.find({}, {"link": 1}))

# Ajouter uniquement les nouveaux documents
for doc in data:
    if "link" not in doc:
        continue  # ignorer les documents sans champ "link"
    if doc["link"] not in existing_links:
        collection.insert_one(doc)
        added_count += 1
        existing_links.add(doc["link"])  # éviter les doublons dans la même session

print(f"{added_count} nouveaux documents insérés.")