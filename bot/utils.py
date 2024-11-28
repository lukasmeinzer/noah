import os
import json
import requests



def get_updates_easy():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    
    # Fetch updates
    response = requests.get(URL)
    updates = response.json()
