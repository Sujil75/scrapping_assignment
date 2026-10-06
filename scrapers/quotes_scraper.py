from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from .base_scraper import fetch_page

logger = logging.getLogger(__name__)


def parse_quote(quote, page_url):
    try:
        text_elem = quote.select_one("span.text")
        author_elem = quote.select_one("small.author")
        tag_elems = quote.select("a.tag")
        link_elem = quote.select_one("a[href^='/author/']")

        tags = [tag.get_text() for tag in tag_elems] if tag_elems else []

        return {
            "text": text_elem.get_text() if text_elem else None,
            "author": author_elem.get_text() if author_elem else None,
            "tags": tags,
            "author_link": urljoin(page_url, link_elem["href"]) if link_elem and link_elem.get("href") else None,
        }
    except Exception as e:
        logger.error(f"Error parsing quote: {e}")
        return None


def parse_page(soup, page_url):
    quotes = []
    quote_elements = soup.select("div.quote")
    for quote in quote_elements:
        quote_data = parse_quote(quote, page_url)
        if quote_data:
            quotes.append(quote_data)
    return quotes


def scrape_quotes(start_url):
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