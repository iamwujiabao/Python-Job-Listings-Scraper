# Python Job Listings Scraper

A beginner-friendly web scraper that collects job listings from the [Fake Python Jobs](https://realpython.github.io/fake-jobs/) website and exports them to a CSV file.

---

## Features

- Scrapes 100 job listings in a single run
- Extracts job title, company name, location, and detail page URL
- Exports results to a clean CSV file
- Handles missing fields and network errors gracefully

---

## Requirements

- Python 3.10+
- [Requests](https://pypi.org/project/requests/)
- [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/job-scraper.git
   cd job-scraper
   ```

2. **Install dependencies**

   ```bash
   pip install requests beautifulsoup4
   ```

---

## Usage

Run the scraper from the project directory:

```bash
python scraper.py
```

On success, you will see output like:

```
Scraping jobs from: https://realpython.github.io/fake-jobs/
Found 100 job cards on the page.
Saved 100 job(s) to 'jobs.csv'.

Preview (first 3 listings):
------------------------------------------------------------
  Title   : Senior Python Developer
  Company : Payne, Roberts and Davis
  Location: Stewartbury, AA
  URL     : https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html
------------------------------------------------------------
  ...
```

The results are saved to `jobs.csv` in the same directory.

---

## Output Format

| Column     | Description                          |
|------------|--------------------------------------|
| `title`    | Job title                            |
| `company`  | Hiring company name                  |
| `location` | City and state of the position       |
| `url`      | Link to the full job detail page     |

Example rows:

```
title,company,location,url
Senior Python Developer,"Payne, Roberts and Davis","Stewartbury, AA",https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html
Energy engineer,Vasquez-Davidson,"Christopherville, AA",https://realpython.github.io/fake-jobs/jobs/energy-engineer-1.html
```

---

## Project Structure

```
job-scraper/
├── scraper.py   # Main scraper script
├── jobs.csv     # Output file (generated on run)
└── README.md
```

---

## How It Works

1. `fetch_page()` sends an HTTP GET request to the target URL and parses the HTML with Beautiful Soup.
2. `parse_job_card()` extracts the four fields from each `<div class="card-content">` element. Cards with missing required fields are skipped rather than crashing the run.
3. `scrape_jobs()` coordinates fetching and parsing, and reports how many cards were skipped.
4. `save_to_csv()` writes all valid listings to `jobs.csv` using Python's built-in `csv` module.

---

## Learning Goals

This project is designed to help you practice:

- Inspecting HTML structure with browser DevTools
- Fetching web pages with the `requests` library
- Navigating and selecting elements with Beautiful Soup
- Handling real-world edge cases like missing fields
- Exporting structured data to CSV for later analysis

---

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).
