from flask import Flask
from threading import Thread
from datetime import datetime, time
from zoneinfo import ZoneInfo
import time as t
import os

app = Flask('')
telegram_client = None

@app.route('/')
def home():
    return "Ubot attivo!", 200

def run_web():
    app.run(host='0.0.0.0', port=8080)

def scheduler():
    """Thread che controlla l'orario e invia messaggi a 'me'"""
    TZ = ZoneInfo("Europe/Rome")
    global telegram_client

    if telegram_client:
        try:
            telegram_client.send_message("me", "🟢 Bot avviato alle 07:00 (ora italiana)")
        except Exception as e:
            print(f"[Errore invio messaggio di avvio]: {e}")

    while True:
        now = datetime.now(TZ).time()
        if not (time(7, 0) <= now <= time(23, 59)):
            print("🛑 Fuori orario, sto spegnendo il bot...")
            if telegram_client:
                try:
                    telegram_client.send_message("me", "🔴 Bot spento alle 00:00 (ora italiana)")
                except Exception as e:
                    print(f"[Errore invio messaggio di spegnimento]: {e}")
            t.sleep(2)
            os._exit(0)
        t.sleep(300)  # Controllo ogni 5 minuti

def keep_alive(client=None):
    global telegram_client
    telegram_client = client
    Thread(target=run_web).start()
    Thread(target=scheduler).start()
