import os
from time import sleep
from pyrogram import Client

try:
    os.remove("my.session")
except Exception:
    pass
try:
    os.remove("bot.session")
except Exception:
    pass
try:
    os.remove("session.session")
except Exception:
    pass

def clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")
    else:
        pass

def impostaapi():
    clear()
    
    # Prova a leggere dalle variabili d'ambiente
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    
    if not api_id:
        while True:
            api_id = input("API_ID: ")
            if str(api_id).isdigit():
                break
            clear()
            print("API_ID non valido!")
            sleep(2)
            clear()
    
    if not api_hash:
        api_hash = input("API_HASH: ")
    
    if api_id and api_hash:
        creasess(api_id, api_hash)

def creasess(api_id, app_hash):
    app = Client("session", int(api_id), app_hash)
    try:
        clear()
        app.start()
    except Exception:
        clear()
        input("app_id/api_hash/numero di telefono non validi")
        impostaapi()
    session = app.export_session_string()
    print(f"String:\n\n{session}")
    app.stop()



clear()
impostaapi()