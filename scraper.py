"""
Fake Python Jobs Scraper
Scrapes job listings from https://realpython.github.io/fake-jobs/
and saves them to a CSV file.
"""

import csv
import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_FILE = "jobs.csv"
CSV_HEADERS = ["title", "company", "location", "url"]


def fetch_page(url: str) -> BeautifulSoup | None:
    """Fetch a webpage and return a BeautifulSoup object, or None on failure."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def parse_job_card(card) -> dict | None:
    """
    Extract job details from a single job card element.
    Returns a dict with title, company, location, and url,
    or None if any required field is missing.
    """
    try:
        title = card.find("h2", class_="title").get_text(strip=True)
        company = card.find("h3", class_="company").get_text(strip=True)
        location = card.find("p", class_="location").get_text(strip=True)

        # The "Apply" link leads to the full job detail page
        apply_link = card.find("a", string=lambda s: s and "apply" in s.lower())
        url = apply_link["href"] if apply_link else ""

        if not all([title, company, location]):
            return None

        return {"title": title, "company": company, "location": location, "url": url}

    except (AttributeError, KeyError, TypeError) as e:
        print(f"Warning: skipping malformed card — {e}", file=sys.stderr)
        return None


def scrape_jobs(url: str) -> list[dict]:
    """Scrape all job listings from the given URL."""
    soup = fetch_page(url)
    if soup is None:
        return []

    job_cards = soup.find_all("div", class_="card-content")
    print(f"Found {len(job_cards)} job cards on the page.")

    jobs = []
    for card in job_cards:
        job = parse_job_card(card)
        if job:
            jobs.append(job)

    skipped = len(job_cards) - len(jobs)
    if skipped:
        print(f"Skipped {skipped} card(s) due to missing fields.")

    return jobs


def save_to_csv(jobs: list[dict], filepath: str) -> None:
    """Write job listings to a CSV file."""
    if not jobs:
        print("No jobs to save.")
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Saved {len(jobs)} job(s) to '{filepath}'.")


def main():
    print(f"Scraping jobs from: {BASE_URL}")
    jobs = scrape_jobs(BASE_URL)

    if jobs:
        save_to_csv(jobs, OUTPUT_FILE)
        # Preview first 3 results in the terminal
        print("\nPreview (first 3 listings):")
        print("-" * 60)
        for job in jobs[:3]:
            print(f"  Title   : {job['title']}")
            print(f"  Company : {job['company']}")
            print(f"  Location: {job['location']}")
            print(f"  URL     : {job['url']}")
            print("-" * 60)
    else:
        print("No jobs were scraped. Check the URL or your network connection.")
        sys.exit(1)


if __name__ == "__main__":
    main()
