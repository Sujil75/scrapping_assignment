import hashlib
import re


def make_fingerprint(rec):
    source = rec.get("source", "")

    if source == "Books to Scrape":
        key = f'{source} {rec.get("name_or_title", "")}'
    else:  # Quotes to Scrape
        key = f'{source} {rec.get("author", "")} {rec.get("name_or_title", "")[:50]}'

    # Normalize: lowercase, remove punctuation, collapse whitespace
    key = re.sub(r"[^\w\s]", "", key.lower())  # lowercase, drop punctuation
    key = " ".join(key.split())  # collapse spaces
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def find_duplicates(records):
    seen = set()
    unique = []
    duplicates = []

    for rec in records:
        fp = make_fingerprint(rec)
        if fp in seen:
            duplicates.append(rec)
        else:
            seen.add(fp)
            unique.append(rec)

    return unique, duplicates