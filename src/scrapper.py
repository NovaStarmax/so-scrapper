import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from database import insert_questions
import os
from dotenv import load_dotenv
import time

load_dotenv()
COLLECTION = os.getenv("COLLECTION_SCRAPPER")

def scrape_page(url: str) -> list:
    """
    Scrape une page Stack Overflow (Newest Questions).
    Retourne une liste de dictionnaires contenant titre, lien, résumé, tags, auteur et date.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    questions = []
    for question_div in soup.select(".s-post-summary"):
        title_tag = question_div.select_one(".s-post-summary--content-title a")
        summary_tag = question_div.select_one(".s-post-summary--content-excerpt")
        tags = [t.text for t in question_div.select(".s-post-summary--meta-tags a")]
        author_tag = question_div.select_one(".s-user-card--link")
        date_tag = question_div.select_one(".relativetime")

        questions.append({
            "title": title_tag.text.strip() if title_tag else None,
            "link": "https://stackoverflow.com" + title_tag["href"] if title_tag else None,
            "summary": summary_tag.text.strip() if summary_tag else None,
            "tags": tags,
            "author": author_tag.text.strip() if author_tag else None,
            "date": date_tag["title"] if date_tag and date_tag.has_attr("title") else None
        })
    return questions

def scrape_multiple_pages(pages: int = 5) -> list:
    """
    Scrape plusieurs pages en parallèle.
    """
    base_url = "https://stackoverflow.com/questions?tab=Newest&pagesize=50&page="
    urls = [f"{base_url}{i}" for i in range(1, pages + 1)]
    
    questions = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scrape_page, url): url for url in urls}
        for future in as_completed(futures):
            try:
                page_data = future.result()
                questions.extend(page_data)
            except Exception as e:
                print(f"Erreur sur {futures[future]}: {e}")
    return questions

def run_scraper(pages: int = 5, append: bool = False):
    """
    Scrape plusieurs pages et insère dans MongoDB.
    append=False permet de ne pas garder les données (mode test).
    """
    questions = scrape_multiple_pages(pages)
    print(f"{len(questions)} questions récupérées sur {pages} pages")
    insert_questions(questions, COLLECTION, append=append)

if __name__ == "__main__":
    start_time = time.time()
    run_scraper(pages=5, append=False)
    end_time = time.time()
    duration = end_time - start_time
    print(f"{duration:.2f} secondes de traitement.")
