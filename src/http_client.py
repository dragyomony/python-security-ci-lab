
"""Small HTTP helper used to demonstrate CI unit testing."""

from urllib.parse import urlsplit

import requests


def fetch_status_code(url: str) -> int:
    """Return an HTTPS endpoint's HTTP status without following redirects."""
    parsed_url = urlsplit(url)

    if parsed_url.scheme != "https" or not parsed_url.hostname:
        raise ValueError("A valid HTTPS URL is required")

    response = requests.get(
        url,
        timeout=5,
        allow_redirects=False
    )

    response.raise_for_status()

    return response.status_code
