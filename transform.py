import pandas as pd

def transform_current_Angebote(angebote: list) -> dict:
    
    dict_angebote_clean = []
    for angebot in angebote:
      supermarkt = angebot["publisherName"].lower()
      # if supermarkt not in interessante_supermärkte:
      #   continue # Dann interessiert uns dieses Angebot nicht
      beginn = angebot["publicationProfiles"][0]["validity"]["startDate"][:10]
      ende = angebot["publicationProfiles"][0]["validity"]["endDate"][:10]
      foto_url = angebot["image"]["url"]
      
      produkt = angebot["products"][0]
      produkt_name = produkt["name"]
      try:
        hersteller = produkt["brand"]["name"]
      except:
        hersteller = ""
  
      bedingungen = angebot["deals"][0]["conditions"]
      bedingungen = ", ".join([value  for item in bedingungen for value in item.values()])
      min_preis = angebot["deals"][0]["min"]
      max_preis = angebot["deals"][0]["max"]
      match len(angebot["deals"]):
        case 2:
          min_normaler_preis = angebot["deals"][1]["min"]
          max_normaler_preis = angebot["deals"][1]["max"]
        case _:
          min_normaler_preis = ""
          max_normaler_preis = ""
      
      item = {
          "Produkt": produkt_name,
          "Hersteller": hersteller,
          "Supermarkt": supermarkt,
          "von": beginn,
          "bis": ende,
          "bedingungen": bedingungen,
          "max_preis": max_preis,
          "max_normaler_preis": max_normaler_preis,
          "foto": foto_url
      }
      
      dict_angebote_clean.append(item) 
      
    
    # Work around, um Duplicates zu droppen
    df = pd.DataFrame(dict_angebote_clean).sort_values("foto")
    df = df.drop_duplicates(subset=[col for col in df.columns if col != "foto"])
    dict_angebote_clean = df.to_dict(orient="records")
    return dict_angebote_clean