import requests

from bot.scraping import new_offers_available, get_new_offers
from bot.user import User

def notify_single_user_with_current_offers(user: User, TOKEN: str):
    current_offers, _ = get_new_offers(users={user.id: user})
    
    
    url_sendText = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    url_sendPhoto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    for supermarkt, angebote in current_offers.items():
        old_product = angebote["gesuchtes_produkt"].lower()
        produkt_noch_valide = old_product in user.products
        supermarkt_valide = any(m.lower() in [market.lower() for market in user.markets] for m in supermarkt.split(" "))
        if not produkt_noch_valide:
            continue
        if not supermarkt_valide:
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
            old_product = changes['from']["gesuchtes_produkt"].lower()
            produkt_noch_valide = old_product in users[user_id].products
            supermarkt_valide = any(m.lower() in [market.lower() for market in users[user_id].markets] for m in supermarkt.split(" "))
            if not produkt_noch_valide:
                break
            if not supermarkt_valide:
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
            new_product = changes['to']["gesuchtes_produkt"].lower()
            produkt_noch_valide = new_product in users[user_id].products
            supermarkt_valide = any(m.lower() in [market.lower() for market in users[user_id].markets] for m in supermarkt.split(" "))
            if not produkt_noch_valide:
                break
            if not supermarkt_valide:
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

