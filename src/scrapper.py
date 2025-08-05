from selenium import webdriver
from bs4 import BeautifulSoup
import time
from database import insert_questions
import os
from dotenv import load_dotenv

load_dotenv()
COLLECTION = os.getenv("COLLECTION_SCRAPPER")

def get_lasted_questions_page() -> list:
    driver = webdriver.Chrome()
    driver.get("https://stackoverflow.com/questions?tab=Newest")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    questions = []
    for question_div in soup.select(".s-post-summary"):
        title_tag = question_div.select_one(".s-post-summary--content-title a")
        summary_tag = question_div.select_one(".s-post-summary--content-excerpt")
        tags = [t.text for t in question_div.select(".s-post-summary--meta-tags a")]
        author_tag = question_div.select_one(".s-user-card--link")
        date_tag = question_div.select_one(".relativetime")

        question = {
            "title": title_tag.text.strip() if title_tag else None,
            "link": "https://stackoverflow.com" + title_tag["href"] if title_tag else None,
            "summary": summary_tag.text.strip() if summary_tag else None,
            "tags": tags,
            "author": author_tag.text.strip() if author_tag else None,
            "date": date_tag["title"] if date_tag and date_tag.has_attr("title") else None
        }
        questions.append(question)

    return questions

if __name__ == "__main__":
    lasted_questions = get_lasted_questions_page()
    for q in lasted_questions:
        print(q)
    insert_questions(lasted_questions, COLLECTION, append=True)
