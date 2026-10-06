from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from .base_scraper import fetch_page

logger = logging.getLogger(__name__)


def parse_book(article, page_url):
    try:
        link = article.select_one("h3 > a")
        price = article.select_one("p.price_color")
        rating = article.select_one("p.star-rating")

        return {
            "title": link.get("title") if link else None,
            "href": urljoin(page_url, link["href"]) if link and link.get("href") else None,
            "price_raw": price.get_text() if price else None,
            "rating_raw": " ".join(rating.get("class", [])) if rating else None,
        }
    except Exception as e:
        logger.error(f"Error parsing book: {e}")
        return None


def parse_page(soup, page_url):
    books = []
    articles = soup.select("article.product_pod")
    for article in articles:
        book_data = parse_book(article, page_url)
        if book_data:
            books.append(book_data)
    return books


def scrape_books(start_url):
    from .base_scraper import create_session

    session = create_session()
    url, page, records = start_url, 1, []

    while url:
        logger.info(f"Page {page}: {url}")
        try:
            response = fetch_page(session, url)
            soup = BeautifulSoup(response.text, "lxml")
            records.extend(parse_page(soup, url))

            next_link = soup.select_one("li.next > a")
            url = urljoin(url, next_link["href"]) if next_link else None
            page += 1
        except Exception as exc:
            logger.error(f"Failed to fetch {url}: {exc}")
            break  # stop this source, keep the program alive

    return records