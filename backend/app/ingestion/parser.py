"""Content parsing and cleaning utilities."""

import re
from html import unescape


def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return text


def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into single spaces."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_content(raw_html: str) -> str:
    """Full cleaning pipeline: strip HTML, normalize whitespace."""
    text = strip_html(raw_html)
    text = normalize_whitespace(text)
    return text
