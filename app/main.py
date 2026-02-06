from fastapi import FastAPI, Request
import asyncio

from app.bot import handle_command, send_message

app = FastAPI(title="Telegram Price Tracker (MongoDB)")


@app.get("/")
async def healthcheck():
    """Health check endpoint. Using GET here prevents Telegram from sending
    webhook POSTs to the root path when setWebhook URL omits a path."""
    return {"status": "ok", "service": "price-tracker-bot"}


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

