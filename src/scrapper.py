import asyncio
import aiohttp
from bs4 import BeautifulSoup
from database import insert_questions
import os
from dotenv import load_dotenv
import time

load_dotenv()
COLLECTION = os.getenv("COLLECTION_SCRAPPER")

def parse_questions(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
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

async def fetch_page(session, url):
    async with session.get(url) as response:
        html = await response.text()
        return parse_questions(html)

async def scrape_async(pages: int = 1) -> list:
    base_url = "https://stackoverflow.com/questions?tab=Newest&pagesize=50&page="
    urls = [f"{base_url}{i}" for i in range(1, pages + 1)]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return [q for page in results for q in page]

def run_scraper(pages: int = 5, append: bool = False):
    start = time.time()
    questions = asyncio.run(scrape_async(pages))
    print(f"{len(questions)} questions get in {time.time()-start:.2f} secondes")
    insert_questions(questions, COLLECTION, append=append)

if __name__ == "__main__":
    run_scraper(pages=5, append=False)
