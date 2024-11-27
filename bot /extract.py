import requests

def extract_current_Angebote(search_term: str) -> list:
    url = f"https://www.kaufda.de/webapp/api/slots/offerSearch?searchQuery={search_term}&lat=48.1391&lng=11.5802&size=25"

    payload = {}
    headers = {
        "authority": "www.kaufda.de",
        "accept": "application/json",
        "accept-language": "en-UM,en;q=0.9,es-ES;q=0.8,es;q=0.7,de-DE;q=0.6,de;q=0.5,en-US;q=0.4",
        "bonial_account_id": "ef3a4060-0e96-4a1a-8a59-ec09620033be",
        "content-type": "application/json",
        "cookie": "DisplayAppInstallBanner=true; onBoarding=%7B%22tooltip%22%3Afalse%7D; location=%7B%22lat%22%3A48.1391%2C%22lng%22%3A11.5802%2C%22city%22%3A%22%22%2C%22cityUrlRep%22%3A%22%22%2C%22zip%22%3A%2280539%22%7D; ab.storage.deviceId.f5fe4cdd-2574-49df-aacb-fe07e41025ea=g%3Ae197e2ee-831d-4d1c-597c-30775632c318%7Ce%3Aundefined%7Cc%3A1729925568682%7Cl%3A1729925568682; _pk_ref.227.8a5d=%5B%22%22%2C%22%22%2C1729925569%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.227.8a5d=1; sessionToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzZXNzaW9uIjoiNTJkM2NmZGEtNWFhMC00OTNhLTljMDUtZDU1MDBkYzQ2ZGEwIiwiaXNzIjoidXNlci1tYW5hZ2VtZW50Iiwib3B0ZWRfb3V0IjpmYWxzZSwiZXhwIjoxNzI5OTI3NDA2LCJpYXQiOjE3Mjk5MjU2MDYsInVzZXIiOiI5NDNmMjI1Yy1kZTRkLTRkYTItOWVlNC02MGNiNWRiZDY0MjUifQ.Nor9q4bos5jAHp6ZeWVhuKRxTI_cTgOwgXW9G9uJFJyFa1kI-vYEBgdjhfeUwDLB5SAhA9TiOxNOYrPunHPsZkyeC3HKG5R56O2JTyJ7jTJqDPTARO-izQeqiL9y_-K1jgZlpLBM_Tz9CS6O0AiX6X8LcOPI5MrlELM0F3Bfa4KVh-2LLewicJK3UyrFr6IlmQKdERT3vYV4Pqw0vnpa29h9Pgk7Syjd66-Ntwk9Wl5Eep4YgLO3zaOARMctydbRYKHojDsJfnAz6n7IwvMGSUcbrLRT2a-TyDWlBnhLIrgb0R9MISodUdFdZ5HzOQFb_Z0OLS31DGtPCzzmjUe01w; _pk_id.227.8a5d=ad4b67ac46a22cfa.1729326833.4.1729925595.1729925569.; ab.storage.sessionId.f5fe4cdd-2574-49df-aacb-fe07e41025ea=g%3A098d5ede-4e03-5000-7a24-227bece041b1%7Ce%3A1729927394907%7Cc%3A1729925568681%7Cl%3A1729925594907",
        "delivery_channel": "dest.kaufda",
        "referer": f"https://www.kaufda.de/webapp/?query={search_term}&lat=48.1391&lng=11.5802",
        "sec-ch-ua": "'Chromium';v='122', 'Not(A:Brand';v='24', 'Google Chrome';v='122'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'Windows'",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "user_platform_category": "desktop.web.browser",
        "user_platform_os": "windows"
    }

    response = requests.get(url, headers=headers, data=payload)

    data = response.json()["_embedded"]["contents"]

    angebote = [angebot["content"] for angebot in data]
    return angebote