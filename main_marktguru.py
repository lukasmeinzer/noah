# In dieser Datei steht der Bot für sich.
# Der benachrichtigt nur dann, wenn M&Ms im Angebot sind und auch nur für zwei User
# Für den allgemeinen Schnäppchenjäger_Bot in bot/ schauen

from datetime import timedelta, datetime
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def main():
    zip_code = "04315"
    url = f"https://api.marktguru.de/api/v1/offers/search?as=web&limit=24&offset=0&q=mms&zipCode={zip_code}"

    payload = {}
    headers = {
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

    response = requests.get(url, headers=headers, data=payload)

    data = response.json()

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

    results = data["results"]

    dict_angebote_mundms= dict()
    for res in results:
        id_angebot = res["id"]
        supermarkt = res["advertisers"][0]["name"]
        beschreibung = res["description"]
        preis = res["price"]
        alter_preis = res["oldPrice"]
        referenz_preis = res["referencePrice"]
        requiresLoyalityMembership =  res["requiresLoyalityMembership"]
    
        date_string = res["validityDates"][0]["from"][:10]
        gültig_von_dateobj =  datetime.strptime(date_string, '%Y-%m-%d') + timedelta(days=1)
        gültig_von = gültig_von_dateobj.date().strftime('%d.%m.%Y')
    
        date_string = res["validityDates"][0]["to"][:10]
        gültig_bis_dateobj = datetime.strptime(date_string, '%Y-%m-%d')
        gültig_bis = gültig_bis_dateobj.date().strftime('%d.%m.%Y')
    
        produkt = res["product"]["name"]
        image = f"https://mg2de.b-cdn.net/api/v1/offers/{id_angebot}/images/default/0/small.webp"
    
        dict_angebote_mundms[supermarkt] = {
            "beschreibung": beschreibung,
            "preis": preis,
            "alter_preis": alter_preis,
            "referenz_preis": referenz_preis,
            "requiresLoyalityMembership": requiresLoyalityMembership,
            "gültig_von": gültig_von,
            "gültig_bis": gültig_bis,
            "produkt": produkt,
            "image": image,
        }


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------


    try:
        with open("angebote_json/mundm_angebote.json", "r") as file:
            dict_angebote_mundms_alt = json.load(file)
    except:
        dict_angebote_mundms_alt = ""

    neue_angebote_da = dict_angebote_mundms != dict_angebote_mundms_alt

    if not neue_angebote_da:
        return

    # für das nächste Mal abspeichern:
    with open("angebote_json/mundm_angebote.json", "w") as file:
        json.dump(dict_angebote_mundms, file, indent=4, ensure_ascii=False)


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------


    TOKEN = os.getenv("NOAHs_TOKEN")
    CHAT_ID_RAFI = os.getenv("RafiKleiner_CHAT_ID")
    CHAT_ID_LUKAS = os.getenv("LukasMeinzer_CHAT_ID")

    url_sendText = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    url_sendPhoto = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    for supermarkt, produkt_info in dict_angebote_mundms.items():
        beschreibung, preis, alter_preis, referenz_preis, requiresLoyalityMembership, gültig_von, gültig_bis, produkt, image = produkt_info.values()

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
            if requiresLoyalityMembership else ""
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
        
        for CHAT_ID in [CHAT_ID_RAFI, CHAT_ID_LUKAS]:
            requests.post(
                url_sendText, 
                data={"chat_id": CHAT_ID, "text": text_gesamt},
            )
            requests.post(
                url_sendPhoto, 
                data={"chat_id": CHAT_ID, "photo": image},
            )




# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

if __name__ == "__main__":
    main()