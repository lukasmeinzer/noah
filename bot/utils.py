import os
import json

def create_message(angebot: dict) -> str:
    text = f"{angebot['Produkt']} (von {angebot['Hersteller']}) bei {angebot['Supermarkt'].upper()} " \
        f"von {angebot['von']} bis {angebot['bis']}. \n" \
        f"Preis: {angebot['max_preis']} statt {angebot['max_normaler_preis']}\n"
    if angebot['bedingungen']:
        text += f"Bedingungen: {angebot['bedingungen']}"
    return text



def check_for_new_Angebote(search_term: str, neue_angebote: list) -> bool: # type: ignore

    try:
        with open(f'angebote_json/alte_angebote_{search_term}.json', 'r', encoding='utf-8') as file:
            alte_angebote = json.load(file)
    except:
        alte_angebote = None
    with open(f'angebote_json/alte_angebote_{search_term}.json', 'w', encoding='utf-8') as file:
        json.dump(neue_angebote, file, ensure_ascii=False)
        
    if alte_angebote == neue_angebote:
        return False
    return True



def get_updates_easy():
    import requests
    import os
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    

    # Fetch updates
    response = requests.get(URL)
    updates = response.json()
