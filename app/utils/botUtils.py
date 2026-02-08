import re
import httpx
from app.config import TELEGRAM_API

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

async def send_message(chat_id: int, text: str):
    """Send a message to a chat using Telegram API without blocking the event loop.

    Uses asyncio.to_thread to run requests.post in a thread so the async event loop
    isn't blocked by the synchronous HTTP call.
    """
    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
                }
        )