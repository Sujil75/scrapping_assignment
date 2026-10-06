import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'processing'))

from processing.cleaning import clean_text, clean_price, clean_rating, clean_tags, normalize_url


def test_clean_text():
    assert clean_text("  Hello \n World ") == "Hello World"
    assert clean_text("Hello\t\tWorld") == "Hello World"
    assert clean_text("Hello\u00a0World") == "Hello World"  # non-breaking space
    assert clean_text("") is None
    assert clean_text(None) is None
    assert clean_text("   ") is None


def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("$12.99") == 12.99
    assert clean_price("€ 10,50") == 1050.0  # comma treated as thousands separator
    assert clean_price("Free") is None
    assert clean_price("") is None
    assert clean_price(None) is None
    assert clean_price("£51,770.99") == 51770.99


def test_clean_rating():
    assert clean_rating("star-rating Three") == 3
    assert clean_rating("One") == 1
    assert clean_rating("FIVE") == 5
    assert clean_rating("three") == 3
    assert clean_rating("invalid") is None
    assert clean_rating("") is None
    assert clean_rating(None) is None
    assert clean_rating("star-rating") is None


def test_clean_tags():
    assert clean_tags(["Tag1", "tag2", "TAG1"]) == "tag1;tag2"
    assert clean_tags(["  Hello  ", "World"]) == "hello;world"
    assert clean_tags([]) is None
    assert clean_tags(None) is None
    assert clean_tags(["", "  ", None]) is None


def test_normalize_url():
    assert normalize_url("https://example.com") == "https://example.com"
    assert normalize_url("http://example.com") == "http://example.com"
    assert normalize_url("example.com") == "https://example.com"
    assert normalize_url("/relative/path") is None  # relative URLs should be handled by urljoin
    assert normalize_url("") is None
    assert normalize_url(None) is None


if __name__ == "__main__":
    test_clean_text()
    test_clean_price()
    test_clean_rating()
    test_clean_tags()
    test_normalize_url()
    print("All cleaning tests passed!")