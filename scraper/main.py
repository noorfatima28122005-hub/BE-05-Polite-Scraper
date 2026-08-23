import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
CACHE_DIR = Path("cache")

USER_AGENT = (
    "FlyRankInternshipA9/1.0 "
    "(https://github.com/noorfatima28122005-hub/BE-05-Polite-Scraper)"
)

TIMEOUT = 10
DELAY = 1


def get_cache_file(name):
    return CACHE_DIR / name


def fetch_page(url, cache_file):
    cache_path = get_cache_file(cache_file)

    # Use cached HTML during development
    if cache_path.exists():
        content = cache_path.read_text(encoding="utf-8")
        print(f"CACHE HIT: {cache_file}")
        return content

    print(f"FETCH: {url}")

    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=TIMEOUT
    )

    # Only HTTP 200 is accepted
    if response.status_code != 200:
        raise RuntimeError(
            f"Fetch failed with status code {response.status_code}"
        )

    content = response.text

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cache_path.write_text(
        content,
        encoding="utf-8"
    )

    print(f"Response size: {len(content)} bytes")

    return content


def discover_books():
    all_urls = []
    current_url = BASE_URL
    catalogue_pages = 0

    while current_url and catalogue_pages < 3:
        catalogue_pages += 1

        print(f"\nProcessing catalogue page {catalogue_pages}...")

        cache_file = f"catalogue-page-{catalogue_pages}.html"

        html = fetch_page(
            current_url,
            cache_file
        )

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # Find every book link on this catalogue page
        for link in soup.select(
            "article.product_pod h3 a"
        ):
            href = link.get("href")

            if href:
                absolute_url = urljoin(
                    current_url,
                    href
                )

                all_urls.append(
                    absolute_url
                )

        # Find catalogue's next link
        next_link = soup.select_one(
            "li.next a"
        )

        if next_link:
            next_href = next_link.get("href")

            if next_href:
                current_url = urljoin(
                    current_url,
                    next_href
                )

                # Wait before a real request
                next_cache = get_cache_file(
                    f"catalogue-page-{catalogue_pages + 1}.html"
                )

                if not next_cache.exists():
                    time.sleep(DELAY)
            else:
                current_url = None
        else:
            current_url = None

    # Remove duplicate URLs
    unique_urls = list(
        dict.fromkeys(all_urls)
    )

    print("\n--- Stage 2 Result ---")
    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(all_urls)}")
    print(f"unique_urls={len(unique_urls)}")

    return unique_urls


def extract_book_details(
    product_url,
    source_page
):
    # Create a safe cache filename from the book URL
    book_slug = product_url.rstrip("/").split("/")[-2]

    cache_file = (
        f"book-{book_slug}.html"
    )

    html = fetch_page(
        product_url,
        cache_file
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    product_main = soup.select_one(
        "article.product_page"
    )

    if product_main is None:
        raise ValueError(
            "Product area not found"
        )

    # Title
    title_element = product_main.select_one(
        "div.product_main h1"
    )

    title = (
        title_element.get_text(
            " ",
            strip=True
        )
        if title_element
        else ""
    )

    # Price
    price_element = product_main.select_one(
        "p.price_color"
    )

    price_text = (
        price_element.get_text(
            " ",
            strip=True
        )
        if price_element
        else ""
    )

    # Availability
    availability_element = (
        product_main.select_one(
            "p.instock.availability"
        )
    )

    availability_text = (
        availability_element.get_text(
            " ",
            strip=True
        )
        if availability_element
        else ""
    )

    # Rating
    rating_element = product_main.select_one(
        "p.star-rating"
    )

    rating_text = ""

    if rating_element:
        classes = rating_element.get(
            "class",
            []
        )

        rating_classes = [
            item
            for item in classes
            if item != "star-rating"
        ]

        if rating_classes:
            rating_text = rating_classes[0]

    # Description
    description_element = soup.select_one(
        "#product_description + p"
    )

    if description_element:
        description = description_element.get_text(
            " ",
            strip=True
        )
    else:
        description = None

    # Fetch timestamp
    fetched_at = datetime.now(
        timezone.utc
    ).isoformat()

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }


def scrape_book_details():
    unique_urls = discover_books()

    records = []

    for index, product_url in enumerate(
        unique_urls,
        start=1
    ):
        print(
            f"\nBook {index}/{len(unique_urls)}"
        )

        try:
            record = extract_book_details(
                product_url=product_url,
                source_page=BASE_URL
            )

            records.append(record)

            # Wait before next real request
            if index < len(unique_urls):
                next_cache = get_cache_file(
                    f"book-{unique_urls[index].rstrip('/').split('/')[-2]}.html"
                )

                if not next_cache.exists():
                    time.sleep(DELAY)

        except requests.RequestException as error:
            print(
                f"Request error: {error}"
            )

        except Exception as error:
            print(
                f"Extraction error: {error}"
            )

    print("\n--- Stage 3 Result ---")
    print(
        f"detail_pages={len(records)}"
    )

    if records:
        print("\n--- Sample Raw Record ---")
        print(records[0])

    return records


if __name__ == "__main__":
    scrape_book_details()