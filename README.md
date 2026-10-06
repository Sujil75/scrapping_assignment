# Web Scraping Assignment

A Python program that scrapes data from two practice websites (Books to Scrape and Quotes to Scrape), cleans and validates the data, removes duplicates, and outputs a consolidated CSV file with a summary report.

## Project Structure

```
scraping_assignment/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py      # Shared HTTP session, retries, timeout
│   ├── books_scraper.py     # Books to Scrape selectors + pagination
│   └── quotes_scraper.py    # Quotes to Scrape selectors + pagination
├── processing/
│   ├── __init__.py
│   ├── cleaning.py          # Text, price, rating, tag, URL cleaning
│   ├── validation.py        # Record validation
│   └── deduplication.py     # Fingerprint + duplicate detection
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
├── logs/
│   └── scraper.log
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

## Features

- **Dynamic Pagination**: Follows "next" links instead of hardcoding page numbers
- **Robust Error Handling**: Continues scraping even if individual pages or records fail
- **Data Cleaning**: Handles messy data like currency symbols, word ratings, extra whitespace
- **Validation**: Checks data integrity and logs rejection reasons
- **Duplicate Detection**: Uses fingerprinting to identify duplicates regardless of spacing/case
- **Logging**: Comprehensive logging to both console and file
- **Modular Design**: Separation of concerns (scraping, processing, main orchestrator)

## Setup

1. **Prerequisites**:
   - Python 3.10-3.12
   - Internet connection
   - Git (optional)

2. **Installation**:
   ```bash
   # Clone or create the project directory
   mkdir scraping_assignment
   cd scraping_assignment

   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

## Usage

Run the scraper with:
```bash
python main.py
```

The program will:
1. Scrape all pages from both sites by following "next" links
2. Clean and validate the data
3. Remove duplicates
4. Generate three output files:
   - `output/final_dataset.csv`: Consolidated dataset
   - `output/summary_report.json`: Statistics and metrics
   - `logs/scraper.log`: Detailed execution log

## Data Model

Both sources are mapped to a common schema:

| Column | Books to Scrape | Quotes to Scrape |
|--------|-----------------|------------------|
| `source` | "Books to Scrape" | "Quotes to Scrape" |
| `source_url` | Book detail page URL | Quote author page URL or page URL |
| `name_or_title` | Book title | Quote text |
| `category` | null (not available on listing page) | "Quotes" (fixed label) |
| `price` | Float (e.g., 51.77) | null |
| `rating` | Integer 1-5 | null |
| `author` | null | Author name |
| `tags` | null | Semicolon-separated tags (lowercase, sorted) |
| `description` | null (not available on listing page) | null |
| `scraped_at` | UTC timestamp | UTC timestamp |

## Implementation Details

### Pagination
- Uses `li.next > a` selector to find next page link
- Converts relative URLs to absolute using `urljoin`
- Continues until no next link is found

### Cleaning Functions
- `clean_text()`: Removes extra whitespace and non-breaking spaces
- `clean_price()`: Extracts numeric value from currency strings
- `clean_rating()`: Converts word ratings (One, Two, etc.) to integers
- `clean_tags()`: Normalizes tags to lowercase, sorted, semicolon-separated
- `normalize_url()`: Ensures URLs have proper protocol

### Validation
Checks:
- Source is one of the two allowed values
- Name/title is not empty
- URL starts with http:// or https://
- Price is non-negative number (if present)
- Rating is integer 1-5 (if present)

### Duplicate Detection
Creates fingerprints based on:
- **Books**: Source + title
- **Quotes**: Source + author + first 50 chars of quote text

Fingerprints are normalized (lowercase, no punctuation, collapsed whitespace) and hashed with SHA256.

## Error Handling
- Network failures are logged and stop that source (other source continues)
- Individual record failures are logged and skipped
- Program continues processing even if some data is invalid

## Testing
Unit tests for processing functions:
```bash
python -m pytest tests/
```

Test cover cleaning, validation, and deduplication logic without requiring internet access.

## Notes & Limitations
1. Book category and description are not available on listing pages (would require visiting each book's detail page)
2. Quote source_url uses author page URL when available, falls back to page URL
3. Real run finds 0 duplicates as source sites contain unique items
4. Delay of 0.5 seconds between requests to be respectful to servers

## AI Usage
See `AI_USAGE.md` for details on AI assistance during development.