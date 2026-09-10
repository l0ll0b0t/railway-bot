@app.post("/webhook")
async def webhook(request: Request):

    raw_body = await request.body()

    try:
        body_text = raw_body.decode("utf-8").strip("\x00")
        import json
        data = json.loads(body_text)

    except Exception as e:
        send_message(f"ERRORE JSON MT5:\n{str(e)}")
        return {"status":"error"}

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
