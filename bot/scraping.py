import requests
from datetime import timedelta, datetime
import re
from typing import Tuple

from bot.utils import get_headers_marktguru, dict_diff
from bot.user import load_users, User
from bot.offer import load_offers, save_offers


# Für welche Users muss ich welche Urls scrapen?
def gather_urls(known_users: dict) -> list:
    urls_to_scrape = list()
    dict_replace = {
        "&": "%26",
        " ": "%20",
    }
    for id, user in known_users.items():
        zip_code = user.zip_code
        products = user.products
        for product in products:
            translation_table = str.maketrans(dict_replace)
            search_term_product = product.translate(translation_table).lower()
            url = f"https://api.marktguru.de/api/v1/offers/search?as=web&limit=24&offset=0&q={search_term_product}&zipCode={zip_code}"
            urls_to_scrape.append((id, product, url))
    return urls_to_scrape
    

# Welche Daten muss ich mir mit den URLs anschauen?
def gather_data_from_urls(urls_to_scrape: list) -> list:
    headers = get_headers_marktguru()
    extracted_data = list()
    for id, product, url in urls_to_scrape:
        response = requests.get(url, headers=headers, data={})
        data = response.json()["results"]
        extracted_data.append((id, product, data))
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
            requiresLoyaltyMembership =  market["requiresLoyalityMembership"] # typo in API

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


def get_new_offers(users: dict[int, User] | None = None) -> Tuple[bool, dict, dict]:
    if not users:
        users = load_users()
    urls_to_scrape = gather_urls(users)
    extracted_data = gather_data_from_urls(urls_to_scrape)
    dict_angebote = gather_info_from_data(extracted_data)
    return dict_angebote, users


def new_offers_available() -> Tuple[bool, dict, dict]:
    current_offers, users = get_new_offers()
    old_offers = load_offers()
    if old_offers[None]:
        del old_offers[None]

    changed_offers = dict_diff(dict1=current_offers, dict2=old_offers)
    if not changed_offers:
        return False, changed_offers, users
    save_offers(current_offers)
    return True, changed_offers, users



