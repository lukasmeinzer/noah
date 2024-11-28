import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from user import User

import commands
from handle_io import handle_product_input, handle_zip_code_input, handle_market_input


async def handle_no_command_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "adding_products" in context.user_data and context.user_data["adding_products"]:
        await handle_product_input(update, context)
        
    if "adding_markets" in context.user_data and context.user_data["adding_markets"]:
        await handle_market_input(update, context)
        
    if "setting_zip_code" in context.user_data and context.user_data["setting_zip_code"]:
        await handle_zip_code_input(update, context)


def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_no_command_message))
    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("about", commands.about))
    application.add_handler(CommandHandler("help", commands.help))
    application.add_handler(CommandHandler("show_me", commands.show_me))
    application.add_handler(CommandHandler("set_zip", commands.set_zip))
    application.add_handler(CommandHandler("add_products", commands.add_products))
    application.add_handler(CommandHandler("add_markets", commands.add_markets))
    
    # Nicht implementiert:
    application.add_handler(CommandHandler("del_products", commands.del_products))
    application.add_handler(CommandHandler("del_markets", commands.del_markets))
    

    application.run_polling()

main()