from flask import Flask
from threading import Thread
from datetime import datetime, time
from zoneinfo import ZoneInfo
import asyncio
import os
import time as t

app = Flask('')
telegram_client = None

@app.route('/')
def home():
    return "Ubot attivo!", 200

def run_web():
    app.run(host='0.0.0.0', port=8080)

async def send_startup_shutdown_messages():
    """Invia i messaggi una volta che il client è attivo."""
    global telegram_client
    TZ = ZoneInfo("Europe/Rome")
    now = datetime.now(TZ)
    hour = now.hour

    try:
        if 7 <= hour <= 23:
            await telegram_client.send_message("me", f"🟢 Bot avviato alle {now.strftime('%H:%M')} (ora italiana)")
        else:
            await telegram_client.send_message("me", f"🔴 Bot spento (fuori orario: {now.strftime('%H:%M')})")
            await telegram_client.stop()
            os._exit(0)
    except Exception as e:
        print(f"[Errore invio messaggio]: {e}")

def scheduler():
    """Avvia coroutine per messaggi e shutdown"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_startup_shutdown_messages())

def keep_alive(client=None):
    global telegram_client
    telegram_client = client
    Thread(target=run_web).start()
    Thread(target=scheduler).start()
