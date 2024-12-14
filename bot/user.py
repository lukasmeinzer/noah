from typing import Literal
import json
from telegram import Update


class User():
    def __init__(self, id: int, first_name: str, last_name: str | None, zip_code : str | None, markets: list | None, products: list | None):
        self.id = id # entspricht auch der chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.zip_code = zip_code if zip_code is not None else None
        self.markets = markets if markets is not None else []
        self.products = products if products is not None else []
        
        
    def update(self, to_update: Literal["markets", "products"], update_method: Literal["add", "delete"], updates: list):
        updates = [item.lower() for item in updates]
        match to_update:
            case "markets": updating = [item.lower() for item in self.markets]
            case "products": updating = [item.lower() for item in self.products]
            case _: raise KeyError("Invalid 'to_update' value")
        
        match update_method:
            case "add": updating.extend(updates)
            case "delete": updating = [m for m in updating if m not in updates]
            case _: raise KeyError("Invalid 'update_method' value")
            
        save_updates(self.id, to_update, updating)
    
    
    def update_zip_code(self, zip_code: str):
        self.zip_code = zip_code
        save_updates(self.id, "zip_code", self.zip_code)

            
    def to_dict(self):
        return self.__dict__


def save_updates(id, to_update: str, updating):
    known_users = load_users()
    
    known_users[str(id)][to_update] = updating
    
    save_users(known_users)


def load_users() -> dict:
    try:
        with open("users.json", "r") as f:
            known_users = json.load(f)
    except KeyError as e:
        print("Keine users.json vorhanden.")
    return known_users


def save_users(known_users: dict):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(known_users, f, ensure_ascii=False, indent=4)
        
        
async def check_for_user(update: Update) -> User | None:
    known_users = load_users()

    try:
        user_data = known_users[str(update.effective_user.id)]
        user = User(**user_data) 
        return user
    except:
        await update.message.reply_text("Du bist noch nicht registriert. Bitte führe /start aus.")
        return 
