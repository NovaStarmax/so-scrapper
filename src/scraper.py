from selenium import webdriver
from bs4 import BeautifulSoup

def get_wikipedia_pytest_title():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/Pytest")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    page_title = soup.find("h1").text
    driver.quit()
    return page_title


if __name__ == "__main__":
    print("Page title of Wikipédia from scraper :", get_wikipedia_pytest_title())
