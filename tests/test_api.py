import pytest
from api import get_newest_datasciences

@pytest.mark.api
def test_get_newest_datasciences():
    questions = get_newest_datasciences(page_size=5, nb_pages=1)
    assert isinstance(questions, list), "Output is not a list"
    assert len(questions) > 0, "Question list is empty"

    first = questions[0]
    expected_keys = [
        "title", "link", "tags",
        "body", "is_answered", "view_count", "answer_count"
    ]

    for key in expected_keys:
        assert key in first, f"Missing key '{key}' in the question result"

    assert isinstance(first["title"], str)
    assert first["link"].startswith("https://")
    assert isinstance(first["tags"], list)
    assert isinstance(first["body"], str)
    assert isinstance(first["is_answered"], bool)
    assert isinstance(first["view_count"], int)
    assert isinstance(first["answer_count"], int)
