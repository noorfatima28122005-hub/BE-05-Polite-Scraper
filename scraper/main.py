import time
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


def get_cache_file(page_number):
    return CACHE_DIR / f"catalogue-page-{page_number}.html"


def fetch_page(url, page_number):
    cache_file = get_cache_file(page_number)

    # Use cached HTML during development
    if cache_file.exists():
        content = cache_file.read_text(encoding="utf-8")

        print(f"CACHE HIT: page {page_number}")
        print(f"Response size: {len(content)} bytes")

        return content

    print(f"FETCH: page {page_number}")

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

    # Save downloaded HTML as cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cache_file.write_text(
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

        html = fetch_page(current_url, catalogue_pages)

        soup = BeautifulSoup(html, "html.parser")

        # Find every book link on this catalogue page
        for link in soup.select("article.product_pod h3 a"):
            href = link.get("href")

            if href:
                absolute_url = urljoin(current_url, href)
                all_urls.append(absolute_url)

        # Find the catalogue's own next link
        next_link = soup.select_one("li.next a")

        if next_link:
            next_href = next_link.get("href")

            if next_href:
                current_url = urljoin(current_url, next_href)

                # Delay only before the next real request.
                # Cached pages do not contact the website.
                if not get_cache_file(catalogue_pages + 1).exists():
                    time.sleep(DELAY)
            else:
                current_url = None
        else:
            current_url = None

    # Remove duplicates while preserving order
    unique_urls = list(dict.fromkeys(all_urls))

    print("\n--- Stage 2 Result ---")
    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(all_urls)}")
    print(f"unique_urls={len(unique_urls)}")

    return unique_urls


if __name__ == "__main__":
    discover_books()