import httpx
from app.config import TELEGRAM_API
from app.dao.users import create_user
from app.dao.schemas import UserCreate
from app.utils.loging import getLogger

logger = getLogger(__name__)

async def start_command(user: dict):
    user_data = UserCreate(
        telegram_id=user["id"],
        username=user.get("username"),
        first_name=user.get("first_name")
    )

    response = await create_user(user_data)
    logger.info(response)
    return help_command(user)

def help_command(user):
    name = ""
    if user and user.get("first_name"):
        name = f", {user['first_name']}"

    return (
        f"👋 Hello{name}!\n\n"
        "Welcome to *Price Tracker Bot* 📊\n\n"
        "I help you track product prices and notify you when they drop "
        "so you never miss a good deal 💸\n\n"
        "🚀 *How to get started:*\n"
        "1️⃣ Send `/track <product_link>` to start tracking a product\n"
        "2️⃣ Use `/list` to see your tracked products\n"
        "3️⃣ Use `/stop <id>` to stop tracking\n\n"
        "ℹ️ Need help? Type `/help` anytime.\n\n"
        "Happy saving! 😊"
    )
def track_command(user,link):
    if not link or link == "":
        return f"please provide product link as /track https://example"
    
    
    
    



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

    
    
    
async def handle_command(data) -> str:
    """Simple command handler for webhook payloads.

    Input: raw text (e.g. '/start' or '/help'). Returns a string reply.
    This keeps webhook handling synchronous and avoids calling async handlers
    directly.
    """
    if not data:
        return "Send a command like /help"
    
    chat = data["message"].get("chat", {})
    user = data["message"].get("from", {})
    chat_id = chat.get("id")
    text = data["message"].get("text", "")

    parts = text.split()
    command = parts[0]

    if command == "/start":
        return await start_command(user)
    elif command == "/help":
        return help_command(user)
    elif command == "/track":
        return track_command(user,parts[1])

    else: 
        return help_command(user)
    
