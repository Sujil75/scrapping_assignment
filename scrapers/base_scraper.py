import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import time


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "ScrapingAssignment/1.0 (learning project)"})
    retries = Retry(total=3, backoff_factor=1.0,
                    status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_page(session: requests.Session, url: str, delay: float = 0.5) -> requests.Response:
    time.sleep(delay)
    response = session.get(url, timeout=10)
    response.raise_for_status()  # raises on 404, 500, etc.
    response.encoding = "utf-8"  # keeps the £ symbol correct
    return response