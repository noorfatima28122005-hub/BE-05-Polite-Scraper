import time
from pathlib import Path

import requests


BASE_URL = "https://books.toscrape.com/"
CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "catalogue-page-1.html"

USER_AGENT = (
    "FlyRankInternshipA9/1.0 "
    "(https://github.com/noorfatima28122005-hub/BE-05-Polite-Scraper)"
)

TIMEOUT = 10


def fetch_catalogue_page():
    # Use cached HTML during development
    if CACHE_FILE.exists():
        content = CACHE_FILE.read_text(encoding="utf-8")

        print("CACHE HIT")
        print(f"Response size: {len(content)} bytes")

        return content

    print("FETCH")

    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        timeout=TIMEOUT
    )

    # Only HTTP 200 is accepted
    if response.status_code != 200:
        raise RuntimeError(
            f"Fetch failed with status code {response.status_code}"
        )

    content = response.text

    # Save the downloaded HTML as cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    CACHE_FILE.write_text(
        content,
        encoding="utf-8"
    )

    print(f"Response size: {len(content)} bytes")

    return content


if __name__ == "__main__":
    fetch_catalogue_page()