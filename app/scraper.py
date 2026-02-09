import random
import asyncio
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup
from app.config import FLIPCART_PRICE_CLASS, FLIPCART_NAME_CLASS

# Note: curl_cffi handles User-Agents automatically with 'impersonate',
# but keeping these for manual header rotation if needed.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

async def get_flipkart_product(url: str):
    """
    Fetches Flipkart product details using curl_cffi to bypass bot detection.
    """
    headers = {
        "Accept-Language": "en-IN,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # Using AsyncSession for non-blocking I/O
        async with AsyncSession() as s:
            # impersonate='chrome110' mimics the TLS fingerprint and headers of a real browser
            response = await s.get(
                url, 
                headers=headers, 
                impersonate="chrome110", 
                timeout=15
            )
            
            # Check for successful response
            if response.status_code != 200:
                print(f"Failed to fetch. Status code: {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, "html.parser")
            
            price_tag = soup.find("div", class_=FLIPCART_PRICE_CLASS)
            title_tag = soup.find("span", class_=FLIPCART_NAME_CLASS)
            
            title = title_tag.text.strip() if title_tag else "Unknown Product"

            if price_tag:
                # Cleaning the price string (₹1,299 -> 1299)
                price_str = price_tag.text.strip().replace("₹", "").replace(",", "")
                # Flipkart sometimes has multiple prices in the tag, take the first one
                price = int(''.join(filter(str.isdigit, price_str)))
                
                return {
                    "title": title,
                    "price": price
                }
            else:
                print(f"Price not found for: {title}")
                return None

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return None