import re

def detect_platform(url: str) -> str:
    if "amazon." in url:
        return "amazon"
    if "flipkart." in url:
        return "flipkart"
    raise ValueError("Unsupported platform")

def is_url(text: str) -> bool:
    url_pattern = re.compile(
        r'https?://[^\s]+'
    )
    return bool(url_pattern.match(text))
