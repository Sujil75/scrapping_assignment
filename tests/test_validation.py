import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'processing'))

from processing.validation import validate_record


def test_validate_record():
    # Valid book record
    valid_book = {
        "source": "Books to Scrape",
        "name_or_title": "Test Book",
        "source_url": "https://books.toscrape.com/catalogue/test-book_1.html",
        "price": 10.99,
        "rating": 3
    }
    assert validate_record(valid_book) == []

    # Valid quote record
    valid_quote = {
        "source": "Quotes to Scrape",
        "name_or_title": "Test quote",
        "source_url": "https://quotes.toscrape.com/author/test-author/",
        "author": "Test Author",
        "tags": "test;quote"
    }
    assert validate_record(valid_quote) == []

    # Unknown source
    invalid_source = {
        "source": "Invalid Source",
        "name_or_title": "Test",
        "source_url": "https://example.com"
    }
    assert "unknown_source" in validate_record(invalid_source)

    # Missing name
    missing_name = {
        "source": "Books to Scrape",
        "name_or_title": "",
        "source_url": "https://books.toscrape.com/catalogue/test-book_1.html"
    }
    assert "missing_name" in validate_record(missing_name)

    # Invalid URL
    invalid_url = {
        "source": "Books to Scrape",
        "name_or_title": "Test Book",
        "source_url": "not-a-url"
    }
    assert "invalid_url" in validate_record(invalid_url)

    # Invalid price
    invalid_price = {
        "source": "Books to Scrape",
        "name_or_title": "Test Book",
        "source_url": "https://books.toscrape.com/catalogue/test-book_1.html",
        "price": -5.0
    }
    assert "invalid_price" in validate_record(invalid_price)

    # Invalid rating
    invalid_rating = {
        "source": "Books to Scrape",
        "name_or_title": "Test Book",
        "source_url": "https://books.toscrape.com/catalogue/test-book_1.html",
        "rating": 6
    }
    assert "invalid_rating" in validate_record(invalid_rating)

    # Multiple issues
    multiple_issues = {
        "source": "Invalid Source",
        "name_or_title": "",
        "source_url": "not-a-url",
        "price": -10.0,
        "rating": 0
    }
    problems = validate_record(multiple_issues)
    assert "unknown_source" in problems
    assert "missing_name" in problems
    assert "invalid_url" in problems
    assert "invalid_price" in problems
    assert "invalid_rating" in problems

    print("All validation tests passed!")


if __name__ == "__main__":
    test_validate_record()