import os
import time
import logging
from pyrogram import Client
from pyrogram.errors import AuthKeyUnregistered, SessionPasswordNeeded, FloodWait
from keep_alive import keep_alive

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crea il client
app = Client(
    os.getenv('SESSION_NAME', 'userbot'),
    session_string=os.getenv('SESSION_STRING'),
    api_id=int(os.getenv('API_ID')),
    api_hash=os.getenv('API_HASH'),
    plugins=dict(root="plugins")
)

def run_bot():
    while True:
        try:
            logger.info("🔄 Avvio del bot...")
            app.run()
        except AuthKeyUnregistered:
            logger.error("❌ Session string non valida. Rigenera la session string.")
            break
        except FloodWait as e:
            logger.warning(f"⏳ FloodWait: attesa di {e.value} secondi")
            time.sleep(e.value)
        except Exception as e:
            logger.error(f"⚠️ Errore inaspettato: {e}")
            logger.info("🔁 Riavvio del bot tra 10 secondi...")
            time.sleep(10)

if __name__ == "__main__":
    keep_alive()
    run_bot()
    
