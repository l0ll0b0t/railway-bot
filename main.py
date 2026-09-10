from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

@app.get("/")
def root():
    return {"status":"running"}

@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    message = f"""
📊 {data.get('symbol','XTIUSD')}

Trend H1:
{data.get('trend_h1','N/D')}

Trend M15:
{data.get('trend_m15','N/D')}

Setup:
{data.get('setup','N/D')}

Prezzo:
{data.get('price','N/D')}

Forza Setup:
{data.get('score','N/D')}/10

Volatilità:
{data.get('volatility','N/D')}
"""

    send_message(message)

    return {"status":"ok"}
