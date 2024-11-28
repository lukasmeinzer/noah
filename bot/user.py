from typing import Literal
import json


class User():
    def __init__(self, id: int, first_name: str, last_name: str | None, zip_code : str | None, markets: list | None, products: list | None):
        self.id = id # entspricht auch der chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.zip_code = zip_code if zip_code is not None else None
        self.markets = markets if markets is not None else []
        self.products = products if products is not None else []
        
        
    def update(self, to_update: Literal["markets", "products"], update_method: Literal["add", "delete"], updates: list):
        match to_update:
            case "markets": updating = self.markets
            case "products": updating = self.products
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
    with open("bot/known_users.json", "r") as f:
        known_users = json.load(f)
    
    known_users[str(id)][to_update] = updating
    
    with open("bot/known_users.json", "w") as f:
        json.dump(known_users, f, indent=4)
        