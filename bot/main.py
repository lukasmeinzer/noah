import requests
import os
from dotenv import load_dotenv
load_dotenv()

from extract import extract_current_Angebote
from utils import create_message, check_for_new_Angebote

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("LukasMeinzer_CHAT_ID")

def find_angebote(search_term: str):
    angebote = extract_current_Angebote(search_term)
    if len(angebote) == 0:
        return 
    dict_angebote_clean = transform_current_Angebote(angebote)
    if len(dict_angebote_clean) == 0:
        return
    
    return dict_angebote_clean

def send_message(search_term: str):
    neue_angebote = find_angebote(search_term)
    if not neue_angebote:
        return
    
    # check, ob Angebote wirklich neu sind...
    neue_angebote_vorhanden = check_for_new_Angebote(search_term, neue_angebote)
    
    if not neue_angebote_vorhanden:
        return
    
    url_sendText = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    url_sendPhoto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    for angebot in neue_angebote:
        text = create_message(angebot)
        requests.post(
            url_sendText, 
            data={"chat_id": CHAT_ID, "text": text},
        )
        requests.post(
            url_sendPhoto, 
            data={"chat_id": CHAT_ID, "photo": angebot["foto"]},
        )



if __name__ == "__main__":
    
    search_terms = [
        "barilla nudeln",
        "M und Ms",
        "maultaschen",
        "doppio passo rotwein",
    ]
    
    try:
        for search_term in search_terms:
            send_message(search_term)
    
    except Exception as e:
        # schick mir eine Nachricht.
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
            data={
                "chat_id": os.getenv("LukasMeinzer_CHAT_ID"), 
                "text": f"yo, wir hatten beim Suchen nach {search_term} ein Fehlerchen: \n{str(e)}"
            },
        )
