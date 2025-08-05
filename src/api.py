import requests
from dotenv import load_dotenv
import os
from database import insert_questions

load_dotenv()
COLLECTION = os.getenv("COLLECTION_API")
PAGESIZE = 100

def get_questions_paginated(nb_pages: int = 2):
    url = "https://api.stackexchange.com/2.3/questions"
    questions = []
    for page in range(1, nb_pages + 1):
        params = {
        "order": "desc",
        "sort": "creation",
        "site": "stackoverflow",
        "pagesize": PAGESIZE,
        "tagged": "data-science",
        "page": page
        }
        response = requests.get(url, params=params)
        print(response)
        data = response.json()
        for item in data.get("items", []):
            questions.append({
                "title": item["title"],
                "link": item["link"],
                "tags": item["tags"],
                "author": item["owner"].get("display_name"),
                "date": item["creation_date"]
            })
    return questions


if __name__ == "__main__":
    test = get_questions_paginated()
    for q in test:
        print(q)
    insert_questions(test, COLLECTION, append=True)
