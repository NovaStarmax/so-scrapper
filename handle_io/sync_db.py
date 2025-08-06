import json, os
from src.database import get_collection

def append_new_documents_to_json(json_file: str, collection):
    json_path = os.path.join("handle_io", json_file)

    # Charger le fichier JSON existant (sinon liste vide)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_links = {doc.get("link") for doc in existing_data if "link" in doc}

    new_docs = []
    for doc in collection.find():
        link = doc.get("link")
        if link and link not in existing_links:
            doc.pop("_id", None)  # Enlever champ interne Mongo
            new_docs.append(doc)
            existing_links.add(link)

    if new_docs:
        print(f"{len(new_docs)} nouveaux documents ajoutés au fichier JSON.")
        existing_data.extend(new_docs)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, default=str)
    else:
        print("Aucun nouveau document à ajouter.")

def import_data(json_file: str, collection):
    json_path = os.path.join("handle_io", json_file)
    if not os.path.exists(json_path):
        print("Aucun fichier JSON trouvé, import annulé.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("Le fichier JSON est vide, rien à importer.")
        return

    existing_links = {doc.get("link") for doc in collection.find({}, {"link": 1}) if doc.get("link")}

    # Filtrer les documents à insérer
    docs_to_insert = []
    for doc in data:
        link = doc.get("link")
        if not link or link in existing_links:
            continue
        doc.pop("_id", None)  # Retirer l'ancien ID Mongo
        docs_to_insert.append(doc)

    if docs_to_insert:
        collection.insert_many(docs_to_insert, ordered=False)
        print(f"{len(docs_to_insert)} nouveaux documents insérés.")
    else:
        print("Aucun nouveau document à insérer.")

def synchronize(json_file: str, collection):
    append_new_documents_to_json(json_file, collection)
    import_data(json_file, collection)
