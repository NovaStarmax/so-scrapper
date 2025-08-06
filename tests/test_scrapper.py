import asyncio
import pytest
from scrapper import scrape_async
from database import insert_questions, get_collection

TEST_COLLECTION = "scrapper_test"

def clean_collection(collection_name: str):
    coll = get_collection(collection_name)
    coll.drop()
    print(f"Collection '{collection_name}' dropped after test.")

@pytest.mark.scrapper
def test_scraper_pipeline():
    # --- 1. HTTP request + scraping ---
    questions = asyncio.run(scrape_async(pages=1))
    assert isinstance(questions, list), "Output is not a list"
    assert len(questions) > 0, "Question list is empty"
    print("1 | HTTP request successful.")

    # --- 2. Structure HTML analysis ---
    first = questions[0]
    for key in ["title", "link", "summary", "tags", "author", "date"]:
        assert key in first, f"Missing field '{key}' in the first question"
    print("2 | HTML analysis successful.")

    # --- 3. Insertion into test DB (append=True to keep it temporarily) ---
    result = insert_questions(questions, TEST_COLLECTION, append=True)
    assert result is True, "Database insertion failed"
    print("3 | Data extraction and DB insertion successful.")

    assert first["title"], "Title is empty"
    assert first["link"].startswith("https://stackoverflow.com"), "Invalid link format"
    assert isinstance(first["tags"], list), "Tags is not a list"
    print("4 | Additional data checks passed.")

    clean_collection(TEST_COLLECTION)
    print("5 | Test collection cleanup done.")
