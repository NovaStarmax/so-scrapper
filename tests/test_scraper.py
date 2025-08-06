import asyncio
from scrapper import scrape_async
from database import insert_questions

def test_scraper_pipeline():
    questions = asyncio.run(scrape_async(pages=1))
    assert isinstance(questions, list), "Output is not a list"
    assert len(questions) > 0, "Question list is empty"
    print("1 | HTTP request successful.")

    first = questions[0]
    for key in ["title", "link", "summary", "tags", "author", "date"]:
        assert key in first, f"  Missing field '{key}' in the first question"
    print("2 | HTML analysis successful.")

    # append=False => Insert and delete
    result = insert_questions(questions, "test_collection", append=False)
    assert result is True, "Database insertion failed"
    print("3 | Extract data and 4 | Database insertion successful.")

    assert first["title"], "  Title is empty"
    assert first["link"].startswith("https://stackoverflow.com"), "Invalid link format"
    assert isinstance(first["tags"], list), "Tags is not a list"
    print("Additional data checks passed.")
