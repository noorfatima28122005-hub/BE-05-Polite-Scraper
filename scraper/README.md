# BE-05 — Polite Web Scraper

A small Python web scraper built for FlyRank Internship — Backend Track, Week 5, Assignment A9.

## Target Classification

### Target
Books to Scrape  
https://books.toscrape.com/

Books to Scrape is a public practice sandbox created specifically for learning and practicing web scraping.

### Scope

This scraper will process only the first **3 catalogue pages** of Books to Scrape.

The expected result is:

- 3 catalogue pages
- 60 unique book URLs
- 60 book detail pages

### Data Collected

For each book, the scraper will collect:

- title
- product URL
- price
- availability
- rating
- description
- source catalogue page
- fetch timestamp

### Robots Check

I requested:

`https://books.toscrape.com/robots.txt`

The server returned:

`404 Not Found`

Therefore, no robots file was found.

A missing robots file is not treated as permission to scrape other websites. This assignment uses Books to Scrape because it is explicitly provided as a public practice sandbox.

### Responsible Scraping

The scraper will:

- identify itself with a user-agent
- use a request timeout
- wait between real requests
- cache downloaded pages during development
- check HTTP status codes
- avoid unnecessary repeated requests
- validate scraped data before storing it

I will not reuse this code on another site without checking its rules and terms first.

## Technology

Python 3.10+

Libraries:

- Requests
- Beautiful Soup
- Pydantic

## Assignment

FlyRank Internship  
Backend Track  
Week 5  
Assignment A9 — The Polite Scraper