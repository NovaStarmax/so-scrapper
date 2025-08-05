import requests
from dotenv import load_dotenv
import os
from database import insert_questions

load_dotenv()
COLLECTION = os.getenv("COLLECTION_API")
PAGESIZE = 100

def get_questions(PAGESIZE):
    url = "https://api.stackexchange.com/2.3/questions"
    tags = "data-science"
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "stackoverflow",
        "pagesize": PAGESIZE,
        "tagged": tags,
        # # 01/01/2025
        # "fromdate": 1735686000,
        # # 05/08/2025
        # "todate": 1754344800
    }
    response = requests.get(url, params=params)
    data = response.json()
    questions = []
    for item in data.get("items", []):
        questions.append({
            "title": item["title"],
            "link": item["link"],
            "tags": item["tags"],
            "author": item["owner"].get("display_name"),
            "date": item["creation_date"]
        })
    return questions

def get_questions_paginated():
    """
    Récupère jusqu'à 1000 questions en utilisant la pagination (10 pages de 100 questions).
    """
    tags = "python;r;sql;julia;r-language;scala;java;matlab;excel;sas;tensorflow;pytorch;keras;pandas;numpy;scikit-learn;xgboost;lightgbm;nlp"
    url = "https://api.stackexchange.com/2.3/questions"
    questions = []
    for page in range(1, 11):
        params = {
        "order": "desc",
        "sort": "creation",
        "site": "datascience",
        "pagesize": PAGESIZE,
        "tagged": tags,
        # 01/01/2025
        "fromdate": 1735686000,
        # 05/08/2025
        "todate": 1754344800,
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
    test = get_questions(PAGESIZE)
    for q in test:
        print(q)
    insert_questions(test, COLLECTION, append=False)
