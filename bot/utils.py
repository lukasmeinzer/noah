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


def dict_diff(dict1: dict, dict2: dict) -> dict: 
    """
    Compare two dicts and return a dict with the changes
    """
    diff = {}

    # Find keys present in dict1 but not in dict2
    for key in dict1.keys() - dict2.keys():
        diff[key] = {"from": dict1[key], "to": None}

    # Find keys present in dict2 but not in dict1
    for key in dict2.keys() - dict1.keys():
        diff[key] = {"from": None, "to": dict2[key]}

    # Find keys present in both but with different values
    for key in dict1.keys() & dict2.keys():
        if key == "image": # Skip image key as it is not relevant for the comparison
            continue
        dict1_value = dict1[key].lower() if isinstance(dict1[key], str) else dict1[key]
        dict2_value = dict2[key].lower() if isinstance(dict2[key], str) else dict2[key]
        if dict1_value != dict2_value:
            diff[key] = {"from": dict1[key], "to": dict2[key]}
            
    return diff

def supermarkt_und_angebot_valide(user: User, angebote: dict, supermarkt: str) -> bool:
    produkt_valide = angebote["gesuchtes_produkt"].lower() in user.products
    
    if (user.markets is None) or (len(user.markets) == 0):
        supermarkt_valide = True
    else:
        supermarkt_valide = any(m.lower() in [market.lower() for market in user.markets] for m in supermarkt.split(" "))
    
    return produkt_valide and supermarkt_valide