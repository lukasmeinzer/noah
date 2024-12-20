import requests
from datetime import timedelta, datetime
import re
from typing import Tuple

from bot.utils import get_headers_marktguru, save_offers, dict_diff, load_offers
from bot.user import load_users


# Für welche Users muss ich welche Urls scrapen?
def gather_urls(known_users: dict) -> list:
    urls_to_scrape = list()
    for id, user in known_users.items():
        zip_code = user["zip_code"]
        products = user["products"]
        for product in products:
            search_term_product = re.sub("[^A-Za-z0-9 ]+", "", product)
            search_term_product = search_term_product.replace(" ", "%20").lower()
            url = f"https://api.marktguru.de/api/v1/offers/search?as=web&limit=24&offset=0&q={search_term_product}&zipCode={zip_code}"
            urls_to_scrape.append((id, product, url))
    return urls_to_scrape
    

# Welche Daten muss ich mir mit den URLs anschauen?
def gather_data_from_urls(urls_to_scrape: list) -> list:
    extracted_data = list()
    for id, product, url in urls_to_scrape:
        payload = {}
        headers = get_headers_marktguru()
        response = requests.get(url, headers=headers, data=payload)
    
        data = response.json()
        results = data["results"]
        extracted_data.append((id, product, results))
    return extracted_data



# richtige Infos raussuchen und Angebote in json speichern
def gather_info_from_data(extracted_data: list) -> dict:
    dict_angebote = dict()
    for id, product, data in extracted_data:
        for market in data:
            supermarkt = market["advertisers"][0]["name"]
            beschreibung = market["description"]
            preis = market["price"]
            alter_preis = market["oldPrice"]
            referenz_preis = market["referencePrice"]
            requiresLoyaltyMembership =  market["requiresLoyaltyMembership"]

            date_string = market["validityDates"][0]["from"][:10]
            gültig_von_dateobj =  datetime.strptime(date_string, '%Y-%m-%d') + timedelta(days=1)
            gültig_von = gültig_von_dateobj.date().strftime('%d.%m.%Y')

            date_string = market["validityDates"][0]["to"][:10]
            gültig_bis_dateobj = datetime.strptime(date_string, '%Y-%m-%d')
            gültig_bis = gültig_bis_dateobj.date().strftime('%d.%m.%Y')

            gefundenes_produkt = market["product"]["name"]
            image = f"https://mg2de.b-cdn.net/api/v1/offers/{market['id']}/images/default/0/small.webp"

            dict_angebote[supermarkt] = {
            "gesuchtes_produkt": product,
            "user_id": id,
            "beschreibung": beschreibung,
            "preis": preis,
            "alter_preis": alter_preis,
            "referenz_preis": referenz_preis,
            "requiresLoyaltyMembership": requiresLoyaltyMembership,
            "gültig_von": gültig_von,
            "gültig_bis": gültig_bis,
            "gefundenes_produkt": gefundenes_produkt,
            "image": image,
        }
            
    return dict_angebote



def new_offers_available() -> Tuple[bool, dict, dict]:
    known_users = load_users()
    urls_to_scrape = gather_urls(known_users)
    extracted_data = gather_data_from_urls(urls_to_scrape)
    dict_angebote = gather_info_from_data(extracted_data)
    # new offers available?
    dict_angebote_ALT = load_offers()

    diffs = dict_diff(dict1=dict_angebote_ALT, dict2=dict_angebote)

    new_offers_available = bool(diffs)

    if not new_offers_available:
        # no new offers. dont do anything
        return False, diffs, known_users
    
    # new offers!
    save_offers(dict_angebote)
    return True, diffs, known_users


