import os
import json
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    symbol = data.get("ticker", "UNKNOWN")
    message = data.get("message", "🚨 Торговый сигнал получен")

    tv_url = f"https://www.tradingview.com/chart/?symbol={symbol.upper()}"
    bingx_url = f"https://bingx.com/ru/trade/{symbol.upper()}"
    bybit_url = f"https://www.bybit.com/trade/usdt/{symbol.upper()}"
    mexc_url = f"https://www.mexc.com/exchange/{symbol.upper()}_USDT"

    buttons = [
        [{"text": "📊 Открыть график", "url": tv_url}],
        [{"text": "🟢 BingX", "url": bingx_url},
         {"text": "🟡 Bybit", "url": bybit_url},
         {"text": "🔵 MEXC", "url": mexc_url}]
    ]

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "reply_markup": json.dumps({"inline_keyboard": buttons}),
        "parse_mode": "HTML"
    }

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=payload)
    return {"status": "ok"}

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
