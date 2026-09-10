from fastapi import FastAPI, Request
import os
import requests
import json

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

    raw_body = await request.body()

    try:
        body_text = raw_body.decode("utf-8").rstrip("\x00")
        data = json.loads(body_text)

    except Exception as e:
        send_message(f"ERRORE JSON MT5:\n{str(e)}")
        return {"status":"error"}

message = f"""
📊 {data.get('symbol','XTIUSD')}

Bias:
{data.get('bias','N/D')}

Trend H1:
{data.get('trend_h1','N/D')}

Trend M5:
{data.get('trend_m5','N/D')}

Trigger:
{data.get('trigger','N/D')}

Prezzo:
{data.get('price','N/D')}

Score:
{data.get('score','N/D')}/10

Commento:
{data.get('comment','N/D')}
"""
``
    send_message(message)

    return {"status":"ok"}
