import re
from scraper import get_wikipedia_pytest_title

def test_wikipedia_pytest_title():
    title = get_wikipedia_pytest_title()
    assert re.search(r"pytest", title, re.IGNORECASE), f"Le titre est incorrect : {title}"
