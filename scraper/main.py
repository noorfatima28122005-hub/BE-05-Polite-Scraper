import time
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    price: str
    availability: str


BASE_URL = "https://books.toscrape.com/"
DELAY = 1


def scrape_page(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for item in soup.select("article.product_pod"):
        title = item.h3.a.get("title", "")

        price = item.select_one(".price_color").get_text(strip=True)
        price = price.replace("Â£", "£")

        availability = item.select_one(
            ".availability"
        ).get_text(" ", strip=True)

        book = Book(
            title=title,
            price=price,
            availability=availability
        )

        books.append(book)

    return books, soup


def scrape_all_books():
    all_books = []
    page_number = 1
    url = BASE_URL

    while url:
        print(f"Scraping page {page_number}...")

        try:
            books, soup = scrape_page(url)
            all_books.extend(books)

            next_button = soup.select_one("li.next a")

            if next_button:
                next_url = next_button.get("href")

                if next_url.startswith("catalogue/"):
                    url = BASE_URL + next_url
                else:
                    url = BASE_URL + "catalogue/" + next_url

                page_number += 1

                time.sleep(DELAY)

            else:
                url = None

        except requests.RequestException as error:
            print(f"Request error: {error}")
            break

    return all_books


if __name__ == "__main__":
    books = scrape_all_books()

    for book in books[:20]:
        print(book.model_dump())

    print(f"\nTotal books scraped: {len(books)}")