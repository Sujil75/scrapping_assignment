import logging
import time
import json
import csv
from pathlib import Path
from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes
from processing.cleaning import clean_text, clean_price, clean_rating, clean_tags, normalize_url
from processing.validation import validate_record
from processing.deduplication import make_fingerprint, find_duplicates

# Setup logging
def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/scraper.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def clean_book_record(raw_book, page_url):
    try:
        cleaned = {
            "source": "Books to Scrape",
            "source_url": normalize_url(raw_book.get("href")),
            "name_or_title": clean_text(raw_book.get("title")),
            "category": None,  # Not available on listing page
            "price": clean_price(raw_book.get("price_raw")),
            "rating": clean_rating(raw_book.get("rating_raw")),
            "author": None,
            "tags": None,
            "description": None,  # Not available on listing page
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
        return cleaned
    except Exception as e:
        logging.error(f"Error cleaning book record: {e}")
        return None

def clean_quote_record(raw_quote, page_url):
    try:
        cleaned = {
            "source": "Quotes to Scrape",
            "source_url": normalize_url(raw_quote.get("author_link") or page_url),
            "name_or_title": clean_text(raw_quote.get("text")),
            "category": "Quotes",  # Fixed label as discussed
            "price": None,
            "rating": None,
            "author": clean_text(raw_quote.get("author")),
            "tags": clean_tags(raw_quote.get("tags")),
            "description": None,
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
        return cleaned
    except Exception as e:
        logging.error(f"Error cleaning quote record: {e}")
        return None

def process_source(scrape_func, start_url, clean_func, source_name):
    logger = logging.getLogger(__name__)
    logger.info(f"Starting to scrape {source_name}")

    # Scrape raw records
    raw_records = scrape_func(start_url)
    logger.info(f"Scraped {len(raw_records)} raw records from {source_name}")

    # Clean records
    cleaned_records = []
    for i, raw_record in enumerate(raw_records):
        try:
            cleaned = clean_func(raw_record, start_url)
            if cleaned:
                cleaned_records.append(cleaned)
            else:
                logger.warning(f"Failed to clean record {i} from {source_name}")
        except Exception as e:
            logger.error(f"Error cleaning record {i} from {source_name}: {e}")

    logger.info(f"Cleaned {len(cleaned_records)} records from {source_name}")

    # Validate records
    valid_records = []
    validation_stats = {
        "unknown_source": 0,
        "missing_name": 0,
        "invalid_url": 0,
        "invalid_price": 0,
        "invalid_rating": 0
    }

    for i, cleaned_record in enumerate(cleaned_records):
        try:
            problems = validate_record(cleaned_record)
            if not problems:
                valid_records.append(cleaned_record)
            else:
                for problem in problems:
                    validation_stats[problem] = validation_stats.get(problem, 0) + 1
                logger.warning(f"Record {i} from {source_name} failed validation: {problems}")
        except Exception as e:
            logger.error(f"Error validating record {i} from {source_name}: {e}")
            validation_stats["unknown_source"] = validation_stats.get("unknown_source", 0) + 1

    logger.info(f"Validated {len(valid_records)} records from {source_name}")

    stats = {
        "raw_count": len(raw_records),
        "cleaned_count": len(cleaned_records),
        "valid_count": len(valid_records),
        "rejected_by_reason": validation_stats
    }

    return valid_records, stats

def write_csv(records, output_path):
    if not records:
        logging.warning("No records to write to CSV")
        return

    # Define column order
    fieldnames = [
        "source", "source_url", "name_or_title", "category",
        "price", "rating", "author", "tags", "description", "scraped_at"
    ]

    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            # Ensure all fields are present, fill missing with None
            row = {field: record.get(field) for field in fieldnames}
            writer.writerow(row)

    logging.info(f"Wrote {len(records)} records to {output_path}")

def write_summary_report(stats, output_path):
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(stats, jsonfile, indent=4)

    logging.info(f"Wrote summary report to {output_path}")

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    start_time = time.time()
    logger.info("Starting scraping assignment")

    # Import csv here to avoid issues if not needed
    import csv

    # Scrape books
    books_start_url = "https://books.toscrape.com/"
    books_records, books_stats = process_source(
        scrape_books, books_start_url, clean_book_record, "Books to Scrape"
    )

    # Scrape quotes
    quotes_start_url = "https://quotes.toscrape.com/"
    quotes_records, quotes_stats = process_source(
        scrape_quotes, quotes_start_url, clean_quote_record, "Quotes to Scrape"
    )

    # Combine records
    all_records = books_records + quotes_records
    logger.info(f"Total records before deduplication: {len(all_records)}")

    # Deduplicate
    unique_records, duplicate_records = find_duplicates(all_records)
    logger.info(f"Found {len(duplicate_records)} duplicates")
    logger.info(f"Unique records after deduplication: {len(unique_records)}")

    # Write outputs
    output_dir = Path("output")
    write_csv(unique_records, output_dir / "final_dataset.csv")

    # Prepare summary statistics
    end_time = time.time()
    duration = end_time - start_time

    summary_stats = {
        "scraped_per_source": {
            "Books to Scrape": books_stats["raw_count"],
            "Quotes to Scrape": quotes_stats["raw_count"]
        },
        "cleaned_per_source": {
            "Books to Scrape": books_stats["cleaned_count"],
            "Quotes to Scrape": quotes_stats["cleaned_count"]
        },
        "valid_per_source": {
            "Books to Scrape": books_stats["valid_count"],
            "Quotes to Scrape": quotes_stats["valid_count"]
        },
        "rejected_by_reason": {
            "Books to Scrape": books_stats["rejected_by_reason"],
            "Quotes to Scrape": quotes_stats["rejected_by_reason"]
        },
        "duplicates_detected": len(duplicate_records),
        "final_record_count": len(unique_records),
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(start_time)),
        "end_time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(end_time)),
        "duration_seconds": round(duration, 2)
    }

    write_summary_report(summary_stats, output_dir / "summary_report.json")

    logger.info("Scraping assignment completed successfully")

if __name__ == "__main__":
    main()