import requests
from dotenv import load_dotenv
import os
from database import insert_questions

load_dotenv()
COLLECTION = os.getenv("COLLECTION_API")

def get_newest_datasciences(page_size: int = 100, nb_pages: int = 2):
    url = "https://api.stackexchange.com/2.3/questions"
    questions = []

    for page in range(1, nb_pages + 1):
        params = {
            "order": "desc",
            "sort": "creation",
            "site": "stackoverflow",
            "filter": "withbody",  # Important pour inclure 'body'
            "pagesize": page_size,
            "tagged": "data-science",
            "page": page
        }

        response = requests.get(url, params=params)
        print(f"Page {page} - Status: {response.status_code}")

        if response.status_code != 200:
            print(f"Erreur lors de l'appel API : {response.text}")
            continue

        data = response.json()
        for item in data.get("items", []):
            questions.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "tags": item.get("tags", []),
                "body": item.get("body"),
                "is_answered": item.get("is_answered"),
                "view_count": item.get("view_count"),
                "answer_count": item.get("answer_count")
            })

    return questions

if __name__ == "__main__":
    questions = get_newest_datasciences()
    for q in questions:
        print(q)
    insert_questions(questions, COLLECTION, append=True)
