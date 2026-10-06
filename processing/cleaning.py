import re

RATING_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def clean_text(value):
    if value is None:
        return None
    text = " ".join(value.replace("\xa0", " ").split())  # collapse all whitespace
    return text or None  # empty string becomes None


def clean_price(raw):
    if not raw:
        return None
    # Remove commas (treat as thousands separators) and extract first number with optional decimal
    match = re.search(r"\d+(?:\.\d+)?", raw.replace(",", ""))
    return float(match.group()) if match else None


def clean_rating(raw):
    if not raw:
        return None
    for word in raw.lower().split():
        if word in RATING_MAP:
            return RATING_MAP[word]
    return None


def clean_tags(tags):
    if not tags:
        return None
    cleaned_tags = [clean_text(tag) for tag in tags if tag]
    cleaned_tags = [tag for tag in cleaned_tags if tag]  # Remove None values
    if not cleaned_tags:
        return None
    # Convert to lowercase and remove duplicates
    cleaned_tags = list(set([tag.lower() for tag in cleaned_tags]))
    cleaned_tags.sort()  # Sort alphabetically
    return ";".join(cleaned_tags)


def normalize_url(url):
    if not url:
        return None
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        # Handle relative URLs - this should ideally be handled by urljoin earlier
        if url.startswith("/"):
            # This is a relative path, but we don't have base URL here
            # In practice, urljoin should have been used in the scraper
            return None  # or we could return as-is and let validation catch it
        else:
            url = "https://" + url
    return url