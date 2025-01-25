import os
import requests

from bot.user import User


def get_updates_easy():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    
    # Fetch updates
    response = requests.get(URL)
    updates = response.json()


def get_headers_marktguru() -> dict:
    return {
        'X-ClientKey': 'hHASZX6oiDywTGnEUxx4PAdU0nWbyHi+0hkaVivc4aM=',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'X-ApiKey': '8Kk+pmbf7TgJ9nVj2cXeA7P5zBGv8iuutVVMRfOfvNE=',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Referer': 'https://www.marktguru.de/',
        'sec-ch-ua-platform': '"Windows"'
    }


def dict_diff(from_: dict, to: dict) -> dict: 
    """
    Compare two dicts and return a dict with the changes
    """
    diff = {}

    # Find keys present in from_ but not in to
    for key in from_.keys() - to.keys():
        diff[key] = {"from": from_[key], "to": None}

    # Find keys present in to but not in from_
    for key in to.keys() - from_.keys():
        diff[key] = {"from": None, "to": to[key]}

    # Find keys present in both but with different values
    for key in from_.keys() & to.keys():
        if key == "ALDI SÜD_Peanut Chocolate_7192930706":
            break
        
        user_id_new = from_[key]["user_id"] != to[key]["user_id"]
        supermarkt_new = from_[key]["supermarkt"] != to[key]["supermarkt"]
        gesuchtes_produkt_new = from_[key]["gesuchtes_produkt"] != to[key]["gesuchtes_produkt"]
        gefundenes_produkt_new = from_[key]["gefundenes_produkt"] != to[key]["gefundenes_produkt"]
        gültig_von_new = from_[key]["gültig_von"] != to[key]["gültig_von"]
        gültig_bis_new = from_[key]["gültig_bis"] != to[key]["gültig_bis"]
        
        neues_angebot = any([user_id_new, supermarkt_new, gesuchtes_produkt_new, gefundenes_produkt_new, gültig_von_new, gültig_bis_new])
        
        if neues_angebot:
            diff[key] = {"from": from_[key], "to": to[key]}
            
    return diff

def supermarkt_und_angebot_valide(user: User, angebote: dict, supermarkt: str) -> bool:
    produkt_valide = angebote["gesuchtes_produkt"].lower() in user.products
    
    if (user.markets is None) or (len(user.markets) == 0):
        supermarkt_valide = True
    else:
        supermarkt_valide = any(m.lower() in [market.lower() for market in user.markets] for m in supermarkt.split(" "))
    
    return produkt_valide and supermarkt_valide

def set_no_context(context):
    """context aufräumen, um Konflike in der Eingabe ohne Command zu vermeiden"""
    context.user_data.clear()