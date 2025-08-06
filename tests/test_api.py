import pytest
from api import get_newest_datasciences 

@pytest.mark.api
def test_get_newest_datasciences():
    questions = get_newest_datasciences(page_size=5, nb_pages=1)
    assert isinstance(questions, list), "Output is not a list"
    assert len(questions) > 0, "Question list is empty"

    first = questions[0]
    for key in ["title", "link", "tags", "author", "date"]:
        assert key in first, f"Missing key '{key}' in the question result"

    assert isinstance(first["title"], str), "Title is not a string"
    assert first["link"].startswith("https://"), "Invalid link format"
    assert isinstance(first["tags"], list), "Tags should be a list"
    assert isinstance(first["author"], str) or first["author"] is None, "Author is invalid"
    assert isinstance(first["date"], int), "Date is not a timestamp"
