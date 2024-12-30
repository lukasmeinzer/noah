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
        if key == "image": # Skip image key as it is not relevant for the comparison
            continue
        # Convert all values to lowercase strings
        # This is necessary because the API sometimes returns floats as strings
        # float values are converted to strings with two decimal places
        from__value = {k: str(format(float(v), ".2f") if (isinstance(v, float) or ((type(v) == str) and v.isdigit())) else v).lower() for k, v in from_[key].items()}
        to_value = {k: str(format(float(v), ".2f") if (isinstance(v, float) or ((type(v) == str) and v.isdigit())) else v).lower() for k, v in to[key].items()}
        if from__value != to_value:
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