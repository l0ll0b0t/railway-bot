from fastapi import FastAPI, Request
import os
import requests
import json
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("XTIUSD Advisor")

TOKEN = os.environ.get("8854597295:AAE3xYNsgQJVbCNr-rjnEy60hGwS2YmLkxg")
CHAT_ID = os.environ.get("525799659")


def send_message(text: str) -> bool:
    if not TOKEN:
        logger.error("Variabile TELEGRAM_TOKEN mancante")
        return False

    if not CHAT_ID:
        logger.error("Variabile CHAT_ID mancante")
        return False

    # Deve essere un URL normale, senza tag HTML
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=15
        )

        logger.info("Telegram HTTP status: %s", response.status_code)
        logger.info("Telegram response: %s", response.text)

        response.raise_for_status()

        result = response.json()

        if not result.get("ok", False):
            logger.error("Telegram ha rifiutato il messaggio: %s", result)
            return False

        logger.info("Messaggio Telegram inviato correttamente")
        return True

    except requests.RequestException as error:
        logger.exception("Errore HTTP durante invio Telegram: %s", error)
        return False

    except ValueError as error:
        logger.exception("Risposta Telegram non JSON: %s", error)
        return False


@app.get("/")
def root():
    return {
        "status": "running",
        "telegram_token_configured": bool(TOKEN),
        "chat_id_configured": bool(CHAT_ID)
    }


@app.get("/test-telegram")
def test_telegram():
    success = send_message(
        "✅ Test collegamento server → Telegram riuscito"
    )

    if success:
        return {
            "status": "ok",
            "message": "Messaggio Telegram inviato"
        }

    return {
        "status": "error",
        "message": "Invio Telegram fallito. Controlla i log."
    }


@app.post("/webhook")
async def webhook(request: Request):
    raw_body = await request.body()

    logger.info("Webhook MT5 ricevuto")
    logger.info("Raw body: %r", raw_body)

    try:
        body_text = raw_body.decode("utf-8").rstrip("\x00")
        data = json.loads(body_text)

    except Exception as error:
        logger.exception("Errore parsing JSON MT5")

        send_message(
            f"❌ ERRORE JSON MT5\n\n{str(error)}"
        )

        return {
            "status": "error",
            "message": str(error)
        }

    message = (
        f"📊 {data.get('symbol', 'XTIUSD')}\n\n"
        f"Bias:\n"
        f"{data.get('bias', 'N/D')}\n\n"
        f"Trend H1:\n"
        f"{data.get('trend_h1', 'N/D')}\n\n"
        f"Trend M5:\n"
        f"{data.get('trend_m5', 'N/D')}\n\n"
        f"Trigger:\n"
        f"{data.get('trigger', 'N/D')}\n\n"
        f"Prezzo:\n"
        f"{data.get('price', 'N/D')}\n\n"
        f"Score:\n"
        f"{data.get('score', 'N/D')}/10\n\n"
        f"Commento:\n"
        f"{data.get('comment', 'N/D')}"
    )

    success = send_message(message)

    if not success:
        return {
            "status": "error",
            "message": "Webhook ricevuto, ma invio Telegram fallito"
        }

    return {
        "status": "ok",
        "message": "Messaggio inoltrato a Telegram"
    }
