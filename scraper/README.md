# BE-05 — Polite Web Scraper

A small Python web scraper built for the **FlyRank Internship — Backend Track, Week 5, Assignment A9**.

The scraper processes the first three catalogue pages of **Books to Scrape**, discovers 60 unique books, visits their detail pages, extracts structured data, validates the records, handles a deliberately broken page without crashing, and produces an honest run report.

## Target Classification

### Target

**Books to Scrape**

https://books.toscrape.com/

Books to Scrape is a public practice sandbox created specifically for learning and practicing web scraping.

### Scope

This scraper processes **only the first 3 catalogue pages**.

Expected result:

* 3 catalogue pages
* 60 discovered book URLs
* 60 unique book URLs
* 60 book detail pages

### Robots Check

I requested:

`https://books.toscrape.com/robots.txt`

The server returned:

`404 Not Found`

Therefore, **no robots file was found**.

A missing robots file is not treated as permission to scrape other websites. This assignment uses Books to Scrape because it is explicitly provided as a public practice sandbox.

### Data Collected

For every book, the scraper collects:

* `title`
* `product_url`
* `price_text`
* `price_gbp`
* `availability_text`
* `rating_text`
* `description`
* `source_page`
* `fetched_at`

## Technology

**Language:** Python 3.10+

**Libraries:**

* Requests
* Beautiful Soup
* Pydantic

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install requests beautifulsoup4 pydantic
```

## How to Run

From the repository root:

```powershell
python scraper\main.py
```

The scraper will:

1. Read cached catalogue pages when available.
2. Discover the first 3 catalogue pages.
3. Discover 60 unique book URLs.
4. Fetch/cache book detail pages.
5. Extract raw book information.
6. Normalize the price into numeric `price_gbp`.
7. Validate records with Pydantic.
8. Store valid records in `output/books.json`.
9. Store invalid records in `output/errors.json`.
10. Write the final run information to `output/run-report.json`.

## Project Structure

```text
BE-05-Polite-Scraper/
│
├── scraper/
│   ├── main.py
│   ├── README.md
│   └── .gitignore
│
├── output/
│   ├── books.json
│   ├── errors.json
│   └── run-report.json
│
└── .gitignore
```

The `cache/` directory is intentionally ignored by Git because cached HTML files are development artifacts and should not be published.

## Record Schema

A validated record contains:

```json
{
  "title": "A Light in the Attic",
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "price_text": "£51.77",
  "price_gbp": 51.77,
  "availability_text": "In stock (22 available)",
  "rating_text": "Three",
  "description": "...",
  "source_page": "https://books.toscrape.com/",
  "fetched_at": "2026-08-23T16:46:53Z"
}
```

`price_gbp` is stored as a numeric value so that another program can sort, compare, or calculate with the price.

Records are validated before they are written to `books.json`.

Invalid records are stored separately in `errors.json` with their validation/fetch error.

## Politeness Rules

The scraper follows these rules:

* Uses an identifying User-Agent:
  `FlyRankInternshipA9/1.0`
* Includes a link to the public GitHub repository in the User-Agent.
* Uses a 10-second request timeout.
* Checks HTTP status codes.
* Waits at least 1 second between real requests.
* Does not wait when reading from local cache.
* Caches downloaded HTML during development.
* Avoids unnecessary repeated requests.
* Handles individual page failures without stopping the entire run.
* Does not retry 403 or 404 responses.
* Keeps scraped data limited to the assignment scope.

## Caching

The scraper caches downloaded catalogue and book pages locally.

On the first request, the program prints:

```text
FETCH
```

On later development runs, cached files produce:

```text
CACHE HIT
```

This prevents repeated requests to the practice website while developing and testing the scraper.

The cache directory is excluded from Git.

## Stage Results

### Stage 0 — Classify Scraping Target

Completed.

* Target: Books to Scrape
* Scope: first 3 catalogue pages
* Robots check: `404 Not Found`
* Responsible scraping rules documented

### Stage 1 — Fetch and Cache HTML

Completed.

The scraper successfully fetched the first catalogue page and cached the HTML.

Example:

```text
FETCH
Response size: 51294 bytes
```

A second run successfully used the cache:

```text
CACHE HIT
Response size: 51294 bytes
```

### Stage 2 — Discover Three Catalogue Pages

Completed.

```text
catalogue_pages=3
discovered=60
unique_urls=60
```

### Stage 3 — Extract Book Details

Completed.

```text
detail_pages=60
```

The scraper produced raw records containing the required provenance fields:

* `source_page`
* `fetched_at`

### Stage 4 — Validate and Store

Completed.

```text
valid_records=60
invalid_records=0
books.json records=60
errors.json records=0
```

A validation check confirmed:

```text
Total: 60
Unique: 60
```

All stored product URLs are absolute HTTPS URLs and `price_gbp` is numeric.

### Stage 5 — Survive Failures and Report

Completed.

The scraper was tested with one deliberately broken URL.

The run completed successfully while preserving the 60 valid records.

Final report:

```json
{
  "started_at": "2026-08-23T16:56:16.881065+00:00",
  "finished_at": "2026-08-23T16:56:19.401860+00:00",
  "duration_seconds": 2.52,
  "catalogue_pages": 3,
  "discovered_urls": 60,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 1,
  "failed_pages": 1
}
```

The `pages_fetched` value is `0` in this particular final run because the catalogue and book pages were already cached. The `cache_hits` value shows that the scraper reused those local copies.

The important failure-handling result is:

```text
valid_records=60
invalid_records=1
failed_pages=1
```

The deliberately broken page did not stop the scraper.

## Idempotency

Running the scraper again does not create duplicate records.

The validated output contains:

```text
Total: 60
Unique: 60
```

Therefore, the same 60 books remain represented by unique canonical product URLs after reruns.

## Why No Browser Was Needed

The core assignment does not require a browser because the required book data is already present in the HTML returned by the server.

A normal HTTP request is therefore sufficient for this website. Using a browser would add unnecessary startup time, memory usage, and complexity without providing additional value for the core scraping task.

## Honest Limitation

This scraper is intentionally designed for the Books to Scrape practice sandbox and the first three catalogue pages required by this assignment.

It should **not** automatically be reused against another website.

Different websites may have different robots rules, terms, authentication requirements, rate limits, page structures, or technical restrictions.

## Ethics Note

Responsible scraping means respecting the website and collecting only what is necessary.

This project follows these principles:

* Use an official API when one exists.
* Check a site's rules and terms before scraping.
* Do not bypass logins, paywalls, CAPTCHAs, or access blocks.
* Identify the scraper honestly.
* Limit request frequency.
* Cache data during development.
* Collect only the fields required for the task.
* Handle failures without repeatedly hammering the server.

I will not reuse this code on another site without checking its rules and terms first.

## Git History

The repository contains meaningful commits for the assignment stages:

```text
Stage 0: classify scraping target
Stage 1: fetch and cache HTML
Stage 2: discover three catalogue pages
Stage 3: extract book details
Stage 4: validate normalized records
Stage 5: survive failures, report the run
```

The repository also contains the initial implementation commit, giving the project **7 meaningful commits in total**.

## Final Result

The completed scraper produces:

* 3 catalogue pages processed
* 60 unique book URLs discovered
* 60 detail pages processed
* 60 validated book records
* 1 deliberately failed page handled safely
* 1 invalid/failure record reported
* 0 duplicate product URLs
* `books.json`
* `errors.json`
* `run-report.json`

The project is published as a public GitHub repository and can be run with a single documented command.
