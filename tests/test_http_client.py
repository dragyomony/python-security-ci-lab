
"""Unit tests for the HTTP status helper; no network calls are made."""

from unittest.mock import Mock, patch

import pytest
import requests

from src.http_client import fetch_status_code


def test_successful_https_request():
    response = Mock(status_code=200)

    with patch(
        "src.http_client.requests.get",
        return_value=response
    ) as get:
        assert fetch_status_code("https://example.com") == 200

    get.assert_called_once_with(
        "https://example.com",
        timeout=5,
        allow_redirects=False
    )

    response.raise_for_status.assert_called_once_with()


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://",
        "example.com"
    ]
)
def test_invalid_url_rejected(url):
    with pytest.raises(ValueError, match="HTTPS"):
        fetch_status_code(url)


def test_http_error_propagates():
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError(
        "404 Not Found"
    )

    with patch(
        "src.http_client.requests.get",
        return_value=response
    ):
        with pytest.raises(requests.HTTPError):
            fetch_status_code("https://example.com/missing")
