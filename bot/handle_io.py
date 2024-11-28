from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from user import User

async def handle_zip_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "setting_zip_code" in context.user_data and context.user_data["setting_zip_code"]:
        user: User = context.user_data["user"]
        zip_code_input = update.message.text.strip()
        # check if zip is valid
        user.update_zip_code(zip_code_input)
        context.user_data["setting_zip_code"] = False
        await update.message.reply_text(f"PLZ erfolgreich hinterlegt.")
        
        
async def handle_product_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "adding_products" in context.user_data and context.user_data["adding_products"]:
        user: User = context.user_data["user"]
        
        products_input = update.message.text
        products = [product.strip() for product in products_input.split(",") if product != ""]
        
        # check if products valid:
        products_valid = check_products(products)

        user.update_products("add", products)

        context.user_data["adding_products"] = False

        await update.message.reply_text(f"Folgende Produkte wurden hinzugefügt: {', '.join(products)}")

        
        
def check_products(products: list) -> dict:
    # am Besten gleich bei Marktguru gucken, ob es dieses Produkt gibt.
    pass