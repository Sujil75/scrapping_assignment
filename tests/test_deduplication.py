import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'processing'))

from processing.deduplication import make_fingerprint, find_duplicates


def test_make_fingerprint():
    # Book record
    book_rec = {
        "source": "Books to Scrape",
        "name_or_title": "Test Book"
    }
    fp1 = make_fingerprint(book_rec)

    # Same book with different spacing
    book_rec_spaced = {
        "source": "Books to Scrape",
        "name_or_title": "  Test Book  "
    }
    fp2 = make_fingerprint(book_rec_spaced)

    # Should be same fingerprint
    assert fp1 == fp2

    # Different book
    book_rec_diff = {
        "source": "Books to Scrape",
        "name_or_title": "Different Book"
    }
    fp3 = make_fingerprint(book_rec_diff)
    assert fp1 != fp3

    # Quote record
    quote_rec = {
        "source": "Quotes to Scrape",
        "author": "Test Author",
        "name_or_title": "Test quote text for testing"
    }
    fp4 = make_fingerprint(quote_rec)

    # Same quote with different spacing
    quote_rec_spaced = {
        "source": "Quotes to Scrape",
        "author": "  Test Author  ",
        "name_or_title": "  Test quote text for testing  "
    }
    fp5 = make_fingerprint(quote_rec_spaced)
    assert fp4 == fp5


def test_find_duplicates():
    base_book = {"source": "Books to Scrape", "author": None}
    base_quote = {"source": "Quotes to Scrape", "author": "Test Author"}

    records = [
        # Unique book
        {**base_book, "name_or_title": "Unique Book"},
        # Duplicate book (different spacing)
        {**base_book, "name_or_title": "  Unique Book  "},
        # Another unique book
        {**base_book, "name_or_title": "Another Book"},
        # Unique quote
        {**base_quote, "name_or_title": "Unique quote text"},
        # Duplicate quote (different case and spacing)
        {**base_quote, "name_or_title": "  UNIQUE QUOTE TEXT  "},
    ]

    unique, duplicates = find_duplicates(records)

    # Should have 3 unique records (2 books, 1 quote)
    assert len(unique) == 3
    # Should have 2 duplicates
    assert len(duplicates) == 2

    # Check that the duplicates are the ones we expect
    unique_titles = [r.get("name_or_title", "") for r in unique]
    assert "Unique Book" in unique_titles or "  Unique Book  " in unique_titles
    assert "Another Book" in unique_titles
    assert "Unique quote text" in [r.get("name_or_title", "") for r in unique] or \
           "  UNIQUE QUOTE TEXT  " in [r.get("name_or_title", "") for r in unique]


def test_duplicates_ignore_case_and_spaces():
    base = {"source": "Books to Scrape", "author": None}
    records = [
        {**base, "name_or_title": "Example Book Title"},
        {**base, "name_or_title": "  Example Book Title "},
        {**base, "name_or_title": "EXAMPLE BOOK TITLE"},
    ]
    unique, dupes = find_duplicates(records)
    assert len(unique) == 1 and len(dupes) == 2


if __name__ == "__main__":
    test_make_fingerprint()
    test_find_duplicates()
    test_duplicates_ignore_case_and_spaces()
    print("All deduplication tests passed!")