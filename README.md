# BE-05 — Polite Web Scraper

A small Python web scraper built for the **FlyRank Internship — Backend Track, Week 5, Assignment A9**.

## Target Classification

### Target

**Books to Scrape**
https://books.toscrape.com/

Books to Scrape is a public practice sandbox created specifically for learning and practicing web scraping.

### Scope

This scraper processes only the first **3 catalogue pages**.

Expected result:

* 3 catalogue pages
* 60 unique book URLs
* 60 book detail pages

### Data Collected

For each book, the scraper collects:

* title
* product URL
* price
* availability
* rating
* description
* source catalogue page
* fetch timestamp

## Robots Check

I requested:

`https://books.toscrape.com/robots.txt`

The server returned:

`404 Not Found`

Therefore, no robots file was found.

A missing robots file is not treated as permission to scrape other websites. This assignment uses Books to Scrape because it is explicitly provided as a public practice sandbox.

## Responsible Scraping

The scraper:

* identifies itself with a custom User-Agent
* uses a request timeout
* waits between real requests
* caches downloaded pages during development
* checks HTTP status codes
* avoids unnecessary repeated requests
* validates scraped data before storing it
* records failures instead of stopping the entire run

I will not reuse this scraper on another website without checking that site's rules and terms first.

## Technology

* Python 3.10+
* Requests
* Beautiful Soup
* Pydantic

## Scraper Stages

### Stage 0 — Target Classification

Classified Books to Scrape as the assignment's permitted practice target.

### Stage 1 — Fetch and Cache HTML

Implemented:

* HTTP requests
* custom User-Agent
* timeout handling
* HTTP status validation
* local HTML caching

### Stage 2 — Catalogue Discovery

The scraper follows catalogue pagination and processes the first 3 pages.

Result:

* catalogue pages: **3**
* discovered URLs: **60**
* unique URLs: **60**

### Stage 3 — Book Detail Extraction

The scraper fetches and parses the 60 discovered book detail pages.

Result:

* detail pages processed: **60**

### Stage 4 — Validation and Normalization

Scraped records are normalized and validated before being written to the output files.

Result:

* valid records: **60**
* invalid records: **0**
* `books.json` records: **60**
* `errors.json` records: **0**

### Stage 5 — Failure Handling and Run Reporting

The scraper continues when an individual page fails and records the failure in the run report.

Latest run evidence:

* catalogue pages: **3**
* discovered URLs: **60**
* valid records: **60**
* invalid records: **1**
* failed pages: **1**
* pages fetched: **0**
* cache hits: **63**
* duration: **2.52 seconds**

The invalid record and failed page are intentionally reported rather than hidden.

## Output Files

The `output/` directory contains:

* `books.json` — normalized book records
* `errors.json` — recorded extraction/fetch errors
* `run-report.json` — execution statistics and failure information

The local `cache/` directory is excluded from Git using `.gitignore`.

## Verification

The final dataset was checked for duplicate product URLs.

Result:

```text
Total: 60
Unique: 60
```

The first record was also checked to confirm that `price_gbp` is stored as a numeric `float`.

```text
Price type: float
```

## Git History

The project was developed through staged commits:

```text
Stage 0: classify scraping target
Stage 1: fetch and cache HTML
Stage 2: discover three catalogue pages
Stage 3: extract book details
Stage 4: validate normalized records
Stage 5: survive failures, report the run
Stage 6: publish scraper evidence
```

## Assignment

**FlyRank Internship**
**Backend Track**
**Week 5**
**Assignment A9 — The Polite Scraper**
