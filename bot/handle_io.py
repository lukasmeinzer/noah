from telegram import Update
from telegram.ext import ContextTypes
from user import User

async def handle_zip_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = context.user_data["user"]
    
    zip_code_input = update.message.text.strip()
    # check if zip is valid
    
    user.update_zip_code(zip_code_input)
    
    context.user_data["setting_zip_code"] = False
    
    await update.message.reply_text(f"PLZ erfolgreich hinterlegt.")
        
        
async def handle_product_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = context.user_data["user"]
    
    products_input = update.message.text
    products = [product.strip() for product in products_input.split(",") if product != ""]
    # Check, if product is valid

    user.update("products", "add", products)

    context.user_data["adding_products"] = False

    await update.message.reply_text(f"Folgende Produkte wurden hinzugefügt: {', '.join(products)}")


async def handle_market_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user: User = context.user_data["user"]
    
    markets_input = update.message.text
    markets = [market.strip() for market in markets_input.split(",") if market != ""]
    # check, if markets valid

    user.update("markets", "add", markets)

    context.user_data["adding_markets"] = False

    await update.message.reply_text(f"Folgende Supermärkte wurden hinzugefügt: {', '.join(markets)}")
