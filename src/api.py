import requests
from dotenv import load_dotenv
import os

load_dotenv()
COLLECTION = os.getenv("COLLECTION_API")

def get_questions(tag, max_questions):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "creation",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": max_questions
    }
    response = requests.get(url, params=params)
    data = response.json()
    questions = []
    for item in data["items"]:
        questions.append({
            "title": item["title"],
            "link": item["link"],
            "tags": item["tags"],
            "author": item["owner"].get("display_name"),
            "date": item["creation_date"]
        })
    return questions

if __name__ == "__main__":
    for q in get_questions("random-forest", 5):
        print(q)
    # insert_questions(lasted_questions, COLLECTION)
