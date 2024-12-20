from telegram import Update
from telegram.ext import ContextTypes
from typing import Literal
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from bot.user import User
from database.models import Feedback, engine

Session = sessionmaker(bind=engine)
session = Session()


async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    input_feedback = update.message.text.strip()
    
    str_now = datetime.today().strftime("%Y-%m-%d_%H:%M:%S_UTC")
    
    feedback_entry = Feedback(timestamp=str_now, feedback=input_feedback)
    session.add(feedback_entry)
    session.commit()
    
    context.user_data["giving_feedback"] = False
    
    await update.message.reply_text(f"Merci. :)")
        

async def handle_zip_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = context.user_data["user"]
    
    zip_code_input = update.message.text.strip()
    # check if zip is valid
    
    user.update_zip_code(zip_code_input)
    
    context.user_data["setting_zip_code"] = False
    
    await update.message.reply_text(f"PLZ erfolgreich hinterlegt.")
        
        
async def handle_product_input(update_method: Literal["add", "delete"], update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = context.user_data["user"]
    
    products_input = update.message.text
    products = [product.strip() for product in products_input.split(",") if product != ""]
    # Check, if product is valid

    user.update("products", update_method, products)

    context.user_data["adding_products"] = False
    context.user_data["deleting_products"] = False

    await update.message.reply_text(
        f"Folgende Produkte wurden {'hinzugefügt' if update_method == 'add' else 'gelöscht'}: {', '.join(products)}")


async def handle_market_input(update_method: Literal["add", "delete"], update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = context.user_data["user"]
    
    markets_input = update.message.text
    markets = [market.strip().lower() for market in markets_input.split(",") if market != ""]
    # check, if markets valid

    user.update("markets", update_method, markets)

    context.user_data["adding_markets"] = False
    context.user_data["deleting_markets"] = False

    await update.message.reply_text(
        f"Folgende Supermärkte wurden {'hinzugefügt' if update_method == 'add' else 'gelöscht'}: {', '.join(markets)}")
