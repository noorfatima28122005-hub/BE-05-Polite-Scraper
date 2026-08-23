import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError


BASE_URL = "https://books.toscrape.com/"
CACHE_DIR = Path("cache")
OUTPUT_DIR = Path("output")

USER_AGENT = (
    "FlyRankInternshipA9/1.0 "
    "(https://github.com/noorfatima28122005-hub/BE-05-Polite-Scraper)"
)

TIMEOUT = 10
DELAY = 1


class Book(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: str | None
    source_page: str
    fetched_at: str


def get_cache_file(page_number):
    return CACHE_DIR / f"catalogue-page-{page_number}.html"


def get_book_cache_file(url):
    book_name = url.rstrip("/").split("/")[-2]
    return CACHE_DIR / f"book-{book_name}.html"


def fetch_page(url, cache_file, label):
    if cache_file.exists():
        content = cache_file.read_text(encoding="utf-8")

        print(f"CACHE HIT: {label}")

        return content

    print(f"FETCH: {url}")

    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Fetch failed with status code {response.status_code}"
        )

    content = response.text

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cache_file.write_text(
        content,
        encoding="utf-8"
    )

    time.sleep(DELAY)

    return content


def discover_books():
    all_urls = []
    current_url = BASE_URL
    catalogue_pages = 0

    while current_url and catalogue_pages < 3:
        catalogue_pages += 1

        print(f"\nProcessing catalogue page {catalogue_pages}...")

        html = fetch_page(
            current_url,
            get_cache_file(catalogue_pages),
            f"catalogue-page-{catalogue_pages}.html"
        )

        soup = BeautifulSoup(html, "html.parser")

        for link in soup.select("article.product_pod h3 a"):
            href = link.get("href")

            if href:
                absolute_url = urljoin(current_url, href)
                all_urls.append(absolute_url)

        next_link = soup.select_one("li.next a")

        if next_link:
            next_href = next_link.get("href")

            if next_href:
                current_url = urljoin(current_url, next_href)
            else:
                current_url = None
        else:
            current_url = None

    unique_urls = list(dict.fromkeys(all_urls))

    print("\n--- Stage 2 Result ---")
    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(all_urls)}")
    print(f"unique_urls={len(unique_urls)}")

    return unique_urls


def normalize_price(price_text):
    clean_price = (
        price_text
        .replace("Â£", "")
        .replace("£", "")
        .strip()
    )

    return float(clean_price)


def extract_book(url, source_page):
    cache_file = get_book_cache_file(url)

    html = fetch_page(
        url,
        cache_file,
        f"book-{url.rstrip('/').split('/')[-2]}.html"
    )

    soup = BeautifulSoup(html, "html.parser")

    product_main = soup.select_one("article.product_page")

    if product_main is None:
        raise ValueError("Product area not found")

    title_element = product_main.select_one("div.product_main h1")
    price_element = product_main.select_one(".price_color")
    availability_element = product_main.select_one(".availability")
    rating_element = product_main.select_one("p.star-rating")

    if title_element is None:
        raise ValueError("Title not found")

    if price_element is None:
        raise ValueError("Price not found")

    if availability_element is None:
        raise ValueError("Availability not found")

    title = title_element.get_text(" ", strip=True)

    price_text = price_element.get_text(strip=True)

    availability_text = availability_element.get_text(
        " ",
        strip=True
    )

    rating_text = ""

    if rating_element:
        classes = rating_element.get("class", [])

        for rating in [
            "One",
            "Two",
            "Three",
            "Four",
            "Five"
        ]:
            if rating in classes:
                rating_text = rating
                break

    description = None

    description_heading = soup.find(
        "div",
        id="product_description"
    )

    if description_heading:
        description_paragraph = (
            description_heading.find_next_sibling("p")
        )

        if description_paragraph:
            description = description_paragraph.get_text(
                " ",
                strip=True
            )

    fetched_at = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime()
    )

    return {
        "title": title,
        "product_url": url,
        "price_text": price_text,
        "price_gbp": normalize_price(price_text),
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def main():
    urls = discover_books()

    valid_books = []
    errors = []

    source_page = BASE_URL

    print("\n--- Stage 4: Extract and Validate ---")

    for index, url in enumerate(urls, start=1):
        print(f"\nBook {index}/{len(urls)}")

        try:
            raw_book = extract_book(
                url,
                source_page
            )

            validated_book = Book.model_validate(
                raw_book
            )

            valid_books.append(
                validated_book.model_dump()
            )

        except ValidationError as error:
            errors.append(
                {
                    "product_url": url,
                    "error": str(error)
                }
            )

        except Exception as error:
            errors.append(
                {
                    "product_url": url,
                    "error": str(error)
                }
            )

    books_path = OUTPUT_DIR / "books.json"
    errors_path = OUTPUT_DIR / "errors.json"

    save_json(
        books_path,
        valid_books
    )

    save_json(
        errors_path,
        errors
    )

    print("\n--- Stage 4 Result ---")
    print(f"valid_records={len(valid_books)}")
    print(f"invalid_records={len(errors)}")
    print(f"books.json records={len(valid_books)}")
    print(f"errors.json records={len(errors)}")


if __name__ == "__main__":
    main()