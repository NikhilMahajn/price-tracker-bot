from app.utils.loging import getLogger
from fastapi import Request

logger = getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    print(exc)
    {"status": "ok"}
