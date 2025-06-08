from flask import Flask
from threading import Thread
from datetime import datetime, time
from zoneinfo import ZoneInfo
import asyncio
import os

app = Flask('')
telegram_client = None

@app.route('/')
def home():
    return "✅ Ubot attivo", 200

def run_web():
    app.run(host='0.0.0.0', port=8080)

async def check_orario_e_agisci():
    """Controlla l'orario e gestisce avvio/spegnimento con messaggi."""
    global telegram_client
    TZ = ZoneInfo("Europe/Rome")
    now = datetime.now(TZ)
    ora = now.hour

    try:
        if 7 <= ora <= 23:
            await telegram_client.send_message("me", f"🟢 Bot avviato alle {now.strftime('%H:%M')}")
        else:
            await telegram_client.send_message("me", f"🔴 Fuori orario ({now.strftime('%H:%M')}). Arresto del bot...")
            await telegram_client.stop()
            os._exit(0)
    except Exception as e:
        print(f"[Errore invio messaggio]: {e}")
        await telegram_client.stop()
        os._exit(0)

def run_checker():
    """Avvia il controllo orario in un event loop separato."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_orario_e_agisci())

def keep_alive(client=None):
    global telegram_client
    telegram_client = client
    Thread(target=run_web).start()
    Thread(target=run_checker).start()
