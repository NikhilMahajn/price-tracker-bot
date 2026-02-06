
source .venv/bin/activate
uvicorn app.main:app --reload --log-config logging.yaml

ngrok http 8000
curl -X POST \
https://api.telegram.org/bot8301858113:AAHRtzN6HkWaa1DRc9NXV2qlirtUM8it18I/setWebhook \
-d url=https://skintight-paraphrastically-marcene.ngrok-free.dev/webhook

https://api.telegram.org/bot8301858113:AAHRtzN6HkWaa1DRc9NXV2qlirtUM8it18I/getWebhookInfo
