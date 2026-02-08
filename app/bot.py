import httpx
import datetime
from app.config import TELEGRAM_API
from app.dao.users import create_user
from app.dao.products import createProduct,track_product,getUserProducts,untrack_product
from app.dao.schemas import UserModel
from app.utils.botUtils import detect_platform,is_url
from app.utils.loging import getLogger
logger = getLogger(__name__)

from app.scheduler import fetch_products_prices

async def start_command(user: dict):
    print(user)
    user_data = UserModel(
        telegram_id=user["id"],
        username=user.get("username"),
        first_name=user.get("first_name")
        )

    response = await create_user(user_data)
    logger.info(response)
    print(response)
    return help_command(user)

def help_command(user):
    name = ""
    if user and user.get("first_name"):
        name = f", {user['first_name']}"

    return (
        f"👋 Hello{name}!\n\n"
        "Welcome to Price Tracker Bot\n\n"
        "I help you track product prices and notify you when they drop "
        "so you never miss a good deal 💸\n\n"
        "🚀 *How to get started:*\n"
        "1️⃣ Send prodcut link to start tracking a product\n"
        "2️⃣ Use /list to see your tracked products\n"
        "3️⃣ Use /stop <id> to stop tracking\n\n"
        "ℹ️ Need help? Type `/help` anytime.\n\n"
        "Happy saving! 😊"
    )
async def track_command(user,link):
    if not link or link == "":
        return f"please provide product link as /track https://example"
    
    try:
        platform = detect_platform(link)
    except:
        return (
            "We only support Following platforms\n"
            "1️⃣ Flipkarn\n"
        )
    product_id = await createProduct(link,platform)

    response = await track_product(user,product_id,link)
    if "success" in response["status"]:
        return  "Product tracking started"
    if "failed" in response["status"]:
        return  response ["message"]
    return  "Product tracking failed"

    
async def list_command(user):
    
    products = await getUserProducts(user)
    if not products:
        return  "\nHey, You dont have any active trackings\nShare product link to start tracking\n"
    prodcut_str = "\nHere are the prodcuts list I am currently tracking for you\n"
    idx = 1
    for product in products:
        prodcut_str += f"\n{idx}) {product["product_name"]}\nprice : {product["initial_price"]}\nclick here /untrack_{product["product_id"]} to remove tracking\n"
        idx += 1
    return prodcut_str

async def untrack_command(user,product_id):
    
    response = await untrack_product(user,product_id)
    if "success" in response["status"]:
        return  f"I will not track {response["product_name"]}"
    if "failed" in response["status"]:
        return  response ["message"]
    return  "Product tracking failed"

    
    
    
async def handle_command(data) -> str:
    """Simple command handler for webhook payloads.

    Input: raw text (e.g. '/start' or '/help'). Returns a string reply.
    This keeps webhook handling synchronous and avoids calling async handlers
    directly.
    """
    try:
        if not data:
            return "Send a command like /help"
        
        chat = data["message"].get("chat", {})
        user = data["message"].get("from", {})
        chat_id = chat.get("id")
        text = data["message"].get("text", "")

        parts = text.split()
        command = parts[0]

        if is_url(text):
            return await track_command(user,text)
        elif command == "/start":
            return await start_command(user)
        elif command == "/help":
            return help_command(user)
        elif command == "/list":
            return await list_command(user)
        elif command == "/test":
            await fetch_products_prices()
            return "test"
        elif command.split("_")[0] == "/untrack":
            return await untrack_command(user,command.split("_")[1])

        else: 
            return help_command(user)
    except Exception as e:
        print(str(e))
        return "Send a command like /help"
        
