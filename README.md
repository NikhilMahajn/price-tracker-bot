# 🛍️ Price Tracker Bot

A **Telegram bot** that helps you track product prices on e-commerce platforms and notifies you when prices drop. Never miss a good deal again! 💰

## ✨ Features

- **🔍 Multi-Platform Support**: Track prices on Flipkart and Amazon
- **📱 Telegram Bot Integration**: Get notifications directly in Telegram
- **💾 MongoDB Database**: Persistent storage for products and tracking data
- **⚡ Async Processing**: Fast, non-blocking webhook handling with FastAPI
- **📊 Price History**: Track price changes over time
- **🎯 Target Price Alerts**: Set target prices and get notified when prices drop below them
- **👤 User Plans**: Support for free and premium user tiers
- **🔄 Real-time Updates**: Webhook-based architecture for instant message handling

## 🏗️ Project Structure

```
price-tracker-bot/
├── app/
│   ├── bot.py                 # Telegram command handlers
│   ├── config.py              # Configuration & environment variables
│   ├── main.py                # FastAPI application & webhooks
│   ├── scraper.py             # Price scraping logic
│   ├── dao/
│   │   ├── db_config.py       # Database connection setup
│   │   ├── schemas.py         # Pydantic models & DB schemas
│   │   ├── users.py           # User operations
│   │   └── products.py        # Product tracking operations
│   ├── utils/
│   │   └── loging.py          # Logging configuration
│   └── exceptions.py          # Custom exceptions
├── .env                        # Environment variables (not in repo)
├── db_schema.md               # Database schema documentation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🗄️ Database Schema

### Collections

#### 1. **users**

```javascript
{
  _id: ObjectId,
  telegram_id: number,
  username: string,
  first_name: string,
  plan: "free" | "premium",
  is_active: boolean,
  created_at: datetime
}
```

#### 2. **product**

```javascript
{
  _id: ObjectId,
  platform: "amazon" | "flipkart",
  url: string,
  created_at: datetime
}
```

#### 3. **user_product**

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  product_id: ObjectId,
  initial_price: number,
  target_price: number | null,
  is_tracking: boolean,
  created_at: datetime
}
```

#### 4. **price_history**

```javascript
{
  _id: ObjectId,
  product_id: ObjectId,
  price: number,
  checked_at: datetime
}
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- MongoDB (Atlas or local)
- Telegram Bot Token (@BotFather)
- ngrok (for webhook tunneling)

### Installation

```bash
# 1. Clone & setup
git clone https://github.com/NikhilMahajn/price-tracker-bot.git
cd price-tracker-bot

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cat > .env << EOF
BOT_TOKEN=your_token_here
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net
DB_NAME=price_tracker
TELEGRAM_API=https://api.telegram.org/bot{BOT_TOKEN}
FLIPCART_PRICE_CLASS=.price-selector
FLIPCART_NAME_CLASS=.name-selector
EOF
```

### Running Locally

**Terminal 1: Start FastAPI**

```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2: Start ngrok**

```bash
ngrok http 8000
```

**Terminal 3: Set webhook**

```bash
# Get your ngrok URL and set it
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
  -d url=https://<YOUR_NGROK_DOMAIN>.ngrok-free.dev/webhook
```

**Verify:**

```bash
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

## 📝 Commands

| Command        | Description                |
| -------------- | -------------------------- |
| `/start`       | Register & start using bot |
| `/help`        | Show available commands    |
| `/track <url>` | Track a product            |
| `/list`        | View tracked products      |
| `/stop <id>`   | Stop tracking              |

## 🔧 Configuration

**Environment Variables:**

| Variable               | Description                      |
| ---------------------- | -------------------------------- |
| `BOT_TOKEN`            | Telegram Bot token               |
| `DATABASE_URL`         | MongoDB connection string        |
| `DB_NAME`              | Database name                    |
| `FLIPCART_PRICE_CLASS` | CSS selector for Flipkart prices |
| `FLIPCART_NAME_CLASS`  | CSS selector for product names   |

## 🏗️ API Endpoints

**POST `/webhook`** - Receives Telegram updates

**GET `/`** - Health check

## 📦 Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: MongoDB (motor async driver)
- **Bot**: python-telegram-bot
- **Scraping**: BeautifulSoup4
- **Tunneling**: ngrok
- **Validation**: Pydantic

## ⚠️ Common Issues

### 405 Method Not Allowed

→ Ensure webhook URL ends with `/webhook`

### Price is Null

→ Update CSS selectors in `.env` (websites change HTML frequently)

### MongoDB Connection Refused

→ Check MongoDB Atlas IP whitelist & connection string

### Bot Not Responding

→ Check: BOT_TOKEN, ngrok tunnel, webhook status, logs

## 🛠️ Development

### Add New Command

```python
# app/bot.py
async def my_command(user, *args):
    return "Response"

# In handle_command()
if command == "/mycommand":
    return await my_command(user, *args)
```

### Add New Platform

```python
# app/scraper.py
def get_amazon_price(url: str) -> int:
    # Scraping logic
    return price

# app/bot.py
if platform == "amazon":
    initial_price = get_amazon_price(link)
```

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/name`
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/name`
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/NikhilMahajn/price-tracker-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NikhilMahajn/price-tracker-bot/discussions)

---

**Built with ❤️ by [NikhilMahajn](https://github.com/NikhilMahajn)**

**Happy price tracking! 🎉**
