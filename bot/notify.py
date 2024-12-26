import requests

from bot.scraping import new_offers_available, get_new_offers
from bot.user import User
from bot.utils import supermarkt_und_angebot_valide

def notify_single_user_with_current_offers(user: User, TOKEN: str):
    current_offers, _ = get_new_offers(users={user.id: user})
    
    
    url_sendText = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    url_sendPhoto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    for supermarkt, angebote in current_offers.items():
        supermarkt = angebote["supermarkt"]
        valide: bool = supermarkt_und_angebot_valide(user, angebote, supermarkt)
        if not valide:
            continue
        text_gesamt = create_newOffer_text(angebote) 
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
    for _, changes in diffs.items():
        case_oldOffer = changes["to"] is None
        case_newOffer = changes["to"] is not None # triggered auch bei Updates
        if case_newOffer:
            angebote = changes['to']
        else:
            angebote = changes['from']
        
        supermarkt = angebote["supermarkt"]
        user_id = angebote["user_id"]
        user = users[user_id]
        valide: bool = supermarkt_und_angebot_valide(user, angebote, supermarkt)
        if not valide:
            continue
        
        if case_oldOffer:
            text = f"Hinweis: {supermarkt.upper()} hat Produkt {angebote['gefundenes_produkt']} nicht mehr im Angebot."
            requests.post(
                url_sendText, 
                data={
                    "chat_id": user_id, 
                    "text": text
                },
            )
        if case_newOffer:
            text_gesamt = create_newOffer_text(changes["to"]) 
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
            

def create_newOffer_text(changes: dict) -> str:
    _, _, supermarkt, beschreibung, preis, alter_preis, _, requiresLoyaltyMembership, gültig_von, gültig_bis, produkt, _ = changes.values()

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

