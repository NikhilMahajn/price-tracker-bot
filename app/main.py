from fastapi import FastAPI, Request
import asyncio

from app.bot import handle_command, send_message
from app.utils.loging import getLogger
from app.exceptions import global_exception_handler

logger = getLogger(__name__)

# APP Configurations
app = FastAPI(title="Telegram Price Tracker)")
app.add_exception_handler(Exception, global_exception_handler)

# Helth Check
@app.get("/")
async def healthcheck():
    """Health check endpoint. Using GET here prevents Telegram from sending
    webhook POSTs to the root path when setWebhook URL omits a path."""
    print("Health")
    return {"status": "ok", "service": "price-tracker-bot"}

# Webhook Entry point for Telegram BOT
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    # Only handle message updates for now
    if "message" in data:
        chat = data["message"].get("chat", {})
        chat_id = chat.get("id")
        text = data["message"].get("text", "")

        reply = await handle_command(data)

        if chat_id is not None:
            asyncio.create_task(
                send_message(chat_id, reply)
                
            )

    return {"status": "ok"}
