import json
from typing import Literal
from telegram import Update
from sqlalchemy.orm import sessionmaker

from database.models import UserModel, engine

Session = sessionmaker(bind=engine)
session = Session()

class User():
    def __init__(self, id: int, first_name: str, last_name: str | None, zip_code : str | None, markets: list | None, products: list | None):
        self.id = id  # entspricht auch der chat_id
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

        setattr(self, to_update, updating)
        save_updates(self.id, to_update, updating)

    def update_zip_code(self, zip_code: str):
        self.zip_code = zip_code
        save_updates(self.id, "zip_code", self.zip_code)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'zip_code': self.zip_code,
            'markets': self.markets,
            'products': self.products
        }

def save_updates(id: int, to_update: str, updating):
    user = session.query(UserModel).filter_by(id=id).first()
    if user:
        setattr(user, to_update, json.dumps(updating, ensure_ascii=False) if isinstance(updating, list) else updating)
        session.commit() 

def load_users() -> dict[int, User]:
    try:
        users = session.query(UserModel).all()
        return {user.id: User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            zip_code=user.zip_code,
            markets=json.loads(user.markets),
            products=json.loads(user.products)
        ) for user in users}
    except:
        session.rollback()
        print("Error loading users")
        raise
    
def load_user(id: int) -> User | None:
    try:
        user = session.query(UserModel).filter_by(id=id).first()
        return User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            zip_code=user.zip_code,
            markets=json.loads(user.markets),
            products=json.loads(user.products)
        )
    except:
        session.rollback()
        print("Error loading user")
        return None

def save_user(user: User):
    user_data = user.to_dict()
    new_user = UserModel(
        id=user_data['id'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        zip_code=user_data['zip_code'],
        markets=json.dumps(user_data["markets"], ensure_ascii=False),
        products=json.dumps(user_data["products"], ensure_ascii=False)
    )
    session.add(new_user)
    session.commit()

async def check_for_user(update: Update) -> User | None:
    user = load_user(id=update.effective_user.id)
    if user:
        return user
    else:
        await update.message.reply_text("Du bist noch nicht registriert. Bitte führe /start aus.")
        return None
