from typing import Literal
import json


class User():
    def __init__(self, id: int, first_name: str, last_name: str | None, zip_code : str | None, markets: list | None, products: list | None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.zip_code = zip_code if zip_code is not None else None
        self.markets = markets if markets is not None else []
        self.products = products if products is not None else []
        
        
    def update_markets(self, update_method: Literal["add", "delete"], update_markets: list):
        match update_method:
            case "add":
                self.markets.extend(update_markets)
            case "delete":
                self.markets = [m for m in self.markets if m not in update_markets]
            case _:
                raise KeyError("Invalid 'update_method' value")
    
    
    def update_products(self, update_method: Literal["add", "delete"], update_products: list):
        match update_method:
            case "add":
                self.products.extend(update_products)
            case "delete":
                self.products = [m for m in self.products if m not in update_products]
            case _:
                raise KeyError("Invalid 'update_method' value")
        
        
        with open("bot/known_users.json", "r") as f:
            known_users = json.load(f)
        
        known_users[str(self.id)]["products"] = self.products
        
        with open("bot/known_users.json", "w") as f:
            json.dump(known_users, f, indent=4)
            
            
    def update_zip_code(self, zip_code: str):
        self.zip_code = zip_code

        with open("bot/known_users.json", "r") as f:
            known_users = json.load(f)
        
        known_users[str(self.id)]["zip_code"] = self.zip_code
        
        with open("bot/known_users.json", "w") as f:
            json.dump(known_users, f, indent=4)
            
            
    def to_dict(self):
        return self.__dict__
