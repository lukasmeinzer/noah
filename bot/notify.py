import requests

from bot.scraping import new_offers_available, get_new_offers
from bot.user import User
from bot.utils import supermarkt_und_angebot_valide

def notify_single_user_with_current_offers(user: User, TOKEN: str):
    current_offers, _ = get_new_offers(users={user.id: user})
    
    
    url_sendText = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    url_sendPhoto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    for supermarkt, angebote in current_offers.items():
        valide: bool = supermarkt_und_angebot_valide(user, angebote, supermarkt)
        if not valide:
            continue
        text_gesamt = create_newOffer_text(supermarkt, angebote) 
        requests.post(
            url_sendText, 
            data={
                "chat_id": user.id, 
                "text": text_gesamt
            },
        )
        requests.post(
            url_sendPhoto, 
            data={
                "chat_id": user.id, 
                "photo": angebote["image"]
            },
        )

def notify_users_with_new_offers(TOKEN: str):
    noa, diffs, users = new_offers_available()
    if not noa:
        # nothing to notify
        return
    
    # notify!
    url_sendText = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    url_sendPhoto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    
    # Die richtigen IDs müssen mit den entsprechenden Produkten benachrichtigt werden
    # Allerdings nur, wenn sich auch wirklich bei ihren eigenen Produkten was geändert hat.
    for supermarkt, changes in diffs.items():
        case_oldOffer = changes["to"] is None
        case_newOffer = changes["to"] is not None # triggered auch bei Updates
        
        if case_oldOffer:
            user_id = changes['from']["user_id"]
            user = users[user_id]
            angebote = changes['from']
            valide: bool = supermarkt_und_angebot_valide(user, angebote, supermarkt)
            if not valide:
                break
            text = f"Hinweis: {supermarkt.upper()} hat Produkt {changes['from']['gefundenes_produkt']} nicht mehr im Angebot."
            print("Nachricht an User", user_id, "gesendet.")
            requests.post(
                url_sendText, 
                data={
                    "chat_id": user_id, 
                    "text": text
                },
            )
        if case_newOffer:
            user_id = changes['to']["user_id"]
            user = users[user_id]
            angebote = changes['to']
            valide: bool = supermarkt_und_angebot_valide(user, angebote, supermarkt)
            if not valide:
                break
            text_gesamt = create_newOffer_text(supermarkt, changes["to"]) 
            requests.post(
                url_sendText, 
                data={
                    "chat_id": user_id, 
                    "text": text_gesamt
                },
            )
            requests.post(
                url_sendPhoto, 
                data={
                    "chat_id": user_id, 
                    "photo": changes["to"]["image"]
                },
            )
            

def create_newOffer_text(supermarkt: str, changes: dict) -> str:
    _, _, beschreibung, preis, alter_preis, _, requiresLoyaltyMembership, gültig_von, gültig_bis, produkt, _ = changes.values()

    text_header = f"{produkt} bei {supermarkt.upper()} im Angebot! \n" 
    text_preis = (
        f"Preis: {preis} " 
        + (f"statt {alter_preis} \n" if alter_preis else "\n")
    )
    text_gültig_von = f"Gültig von: {gültig_von}\n"
    text_gültig_bis = f"Gültig bis: {gültig_bis}\n"
    text_beschreibung = f"Beschreibung: {beschreibung} \n"
    text_loyaltyMember = (
        "ACHTUNG: Nur gültig mit zugehöriger Plus-Mitgliedschaft \n" 
        if requiresLoyaltyMembership else ""
    )

    text_gesamt = (
                "Es gibt Neuigkeiten! \n"
                + text_header
                + text_preis
                + text_gültig_von
                + text_gültig_bis
                + text_beschreibung
                + text_loyaltyMember
            )
    
    return text_gesamt

