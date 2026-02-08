

import requests
import random
from bs4 import BeautifulSoup
from app.config import FLIPCART_PRICE_CLASS,FLIPCART_NAME_CLASS

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]


def get_flipkart_product(url: str):

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-IN,en;q=0.9",
    }

    session = requests.Session()
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    
    price_tag = soup.find("div", class_=FLIPCART_PRICE_CLASS)
    title_tag = soup.find("span", class_=FLIPCART_NAME_CLASS)
    title = None
    if title_tag:
        title = title_tag.text.strip()


    if price_tag:
        price = price_tag.text.strip().replace("₹","").replace(",","")
        price = int(price)
        return {
            "title": title,
            "price": price
        }
        
    else:
        print("Price not found")
        return None
