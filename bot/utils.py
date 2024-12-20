import os
import requests
from sqlalchemy.orm import sessionmaker

from database.models import Offer as OfferModel, engine

Session = sessionmaker(bind=engine)
session = Session()

def get_updates_easy():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    
    # Fetch updates
    response = requests.get(URL)
    updates = response.json()


def get_headers_marktguru():
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


def save_offers(dict_angebote: dict):
    for _, offer_data in dict_angebote.items():
        offer = OfferModel(**offer_data)
        session.add(offer)
    session.commit()

def load_offers() -> dict:
    offers = session.query(OfferModel).all()
    return {offer.supermarkt: offer.to_dict() for offer in offers}


def dict_diff(dict1: dict, dict2: dict) -> dict: 
    """
    Vergleiche zwei dicts und gib ein dict mit den Änderungen zurück
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
        if dict1[key] != dict2[key]:
            diff[key] = {"from": dict1[key], "to": dict2[key]}
            
    return diff