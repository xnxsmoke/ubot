import os
import time
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from pyrogram import Client
from pyrogram.errors import AuthKeyUnregistered, FloodWait

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    os.getenv('SESSION_NAME', 'userbot'),
    session_string=os.getenv('SESSION_STRING'),
    api_id=int(os.getenv('API_ID')),
    api_hash=os.getenv('API_HASH'),
    plugins=dict(root="plugins")
)

def is_in_orario():
    TZ = ZoneInfo("Europe/Rome")
    ora = datetime.now(TZ).hour
    return 7 <= ora <= 23  # acceso tra 7 e 23

def run_bot():
    try:
        app.start()
        if not is_in_orario():
            logger.info("🔴 Fuori orario all'avvio, mando messaggio e spengo...")
            app.send_message("me", "🔴 Bot fuori orario all'avvio, chiudo.")
            app.stop()
            return

        app.send_message("me", "🟢 Bot avviato correttamente.")

        # Loop principale: ogni 60 secondi controllo l'orario
        while True:
            time.sleep(60)
            if not is_in_orario():
                logger.info("🔴 Orario passato, mando messaggio e spengo...")
                app.send_message("me", "🔴 Orario di attività finito, spengo il bot.")
                app.stop()
                break

        logger.info("Bot spento correttamente.")
    except AuthKeyUnregistered:
        logger.error("❌ Session string non valida. Rigenera la session string.")
    except FloodWait as e:
        logger.warning(f"⏳ FloodWait: attesa di {e.value} secondi")
        time.sleep(e.value)
        run_bot()
    except Exception as e:
        logger.error(f"⚠️ Errore inaspettato: {e}")
        logger.info("🔁 Riavvio del bot tra 10 secondi...")
        time.sleep(10)
        run_bot()

if __name__ == "__main__":
    run_bot()
