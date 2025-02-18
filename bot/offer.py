from database.models import OfferModel, Session

class Offer:
    def __init__(self, id, user_id, supermarkt, gesuchtes_produkt, beschreibung, preis, alter_preis, referenz_preis, requiresLoyaltyMembership, gültig_von, gültig_bis, gefundenes_produkt, image):
        self.id = id
        self.user_id = user_id
        self.supermarkt = supermarkt
        self.gesuchtes_produkt = gesuchtes_produkt
        self.beschreibung = beschreibung
        self.preis = preis
        self.alter_preis = alter_preis
        self.referenz_preis = referenz_preis
        self.requiresLoyaltyMembership = requiresLoyaltyMembership
        self.gültig_von = gültig_von
        self.gültig_bis = gültig_bis
        self.gefundenes_produkt = gefundenes_produkt
        self.image = image

    def __repr__(self):
        return f"<Offer(id={self.id}, user_id={self.user_id}, supermarkt={self.supermarkt}, gesuchtes_produkt={self.gesuchtes_produkt}, beschreibung={self.beschreibung}, preis={self.preis}, alter_preis={self.alter_preis}, referenz_preis={self.referenz_preis}, requiresLoyaltyMembership={self.requiresLoyaltyMembership}, gültig_von={self.gültig_von}, gültig_bis={self.gültig_bis}, gefundenes_produkt={self.gefundenes_produkt}, image={self.image})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "supermarkt": self.supermarkt,
            "gesuchtes_produkt": self.gesuchtes_produkt,
            "beschreibung": self.beschreibung,
            "preis": self.preis,
            "alter_preis": self.alter_preis,
            "referenz_preis": self.referenz_preis,
            "requiresLoyaltyMembership": self.requiresLoyaltyMembership,
            "gültig_von": self.gültig_von,
            "gültig_bis": self.gültig_bis,
            "gefundenes_produkt": self.gefundenes_produkt,
            "image": self.image
        }

# für flüchtige Tabelle
def replace_offers(dict_angebote: dict):
    with Session() as session:
        session.query(OfferModel).delete()
        save_offers(dict_angebote)
    

# für persistente Tabelle
def save_offers(dict_angebote: dict):
    with Session() as session:
        for _, offer_data in dict_angebote.items():
            offer = OfferModel(**offer_data)
            session.add(offer)
        session.commit()

def load_offers() -> dict:
    with Session() as session:
        offers = session.query(OfferModel).all()
        return {
            f"{offer.supermarkt}_{offer.gefundenes_produkt}_{offer.user_id}": {
                "user_id": offer.user_id,
                "supermarkt": offer.supermarkt,
                "gesuchtes_produkt": offer.gesuchtes_produkt,
                "beschreibung": offer.beschreibung,
                "preis": offer.preis,
                "alter_preis": offer.alter_preis,
                "referenz_preis": offer.referenz_preis,
                "requiresLoyaltyMembership": offer.requiresLoyaltyMembership,
                "gültig_von": offer.gültig_von,
                "gültig_bis": offer.gültig_bis,
                "gefundenes_produkt": offer.gefundenes_produkt,
                "image": offer.image
            } for offer in offers
        }