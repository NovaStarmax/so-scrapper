from pymongo import MongoClient
import json, os
from src.database import get_collection
from dotenv import load_dotenv


def append_new_documents_to_json(json_file, collection):
    json_path = "handle_io/" + json_file
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


def import_data(json_file, collection):
    json_path = "handle_io/" + json_file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

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


def synchronize(json_file: str, collection):
    append_new_documents_to_json(json_file, collection)
    import_data(json_file, collection)
