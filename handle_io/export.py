from pymongo import MongoClient
import json, os
from database import get_collection
from dotenv import load_dotenv

load_dotenv()

COLLECTION_API = os.getenv("COLLECTION_API")
COLLECTION_SCRAPPER = os.getenv("COLLECTION_SCRAPPER")





def append_new_documents_to_json(json, collection):
    json_path = "handle_io/" + json
    # Charger le fichier JSON s'il existe
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Extraire les liens déjà présents dans le fichier
    existing_links = set(doc.get("link") for doc in existing_data if "link" in doc)

    # Chercher les nouveaux documents depuis la base MongoDB
    new_docs = []
    for doc in collection.find():
        link = doc.get("link")
        if link and link not in existing_links:
            new_docs.append(doc)
            existing_links.add(link)

    if new_docs:
        print(f"{len(new_docs)} nouveaux documents ajoutés au fichier JSON.")
        # Ajouter les nouveaux documents
        existing_data.extend(new_docs)

        # Réécrire le fichier avec les anciens + nouveaux
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, default=str)
    else:
        print("Aucun nouveau document à ajouter.")

# Appel direct (optionnel)
# append_new_documents_to_json()
