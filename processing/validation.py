VALID_SOURCES = {"Books to Scrape", "Quotes to Scrape"}


def validate_record(rec):
    problems = []

    # Known source
    if rec.get("source") not in VALID_SOURCES:
        problems.append("unknown_source")

    # Has a name
    if not rec.get("name_or_title"):
        problems.append("missing_name")

    # Valid URL
    source_url = rec.get("source_url")
    if not source_url or not str(source_url).startswith(("http://", "https://")):
        problems.append("invalid_url")

    # Valid price
    price = rec.get("price")
    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            problems.append("invalid_price")

    # Valid rating
    rating = rec.get("rating")
    if rating is not None:
        if rating not in (1, 2, 3, 4, 5):
            problems.append("invalid_rating")

    return problems  # empty list = valid