

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, HTTPError


from app.config import FLIPCART_PRICE_CLASS

def get_flipkart_price(url: str):

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",
    }

    session = requests.Session()
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.find("div", class_=FLIPCART_PRICE_CLASS)

    if price_tag:
        price = price_tag.text.strip().replace("₹","").replace(",","")
        print("Price:", price)
        return price
    else:
        print("Price not found")
        return None

