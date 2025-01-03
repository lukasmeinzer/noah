import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

from bot import commands
from bot.user_input import (
    handle_product_input, 
    handle_zip_code_input, 
    handle_market_input,
    handle_feedback,
)
from bot.notify import notify_users_with_new_offers


async def handle_no_command_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "giving_feedback" in context.user_data and context.user_data["giving_feedback"]:
        await handle_feedback(update, context)
        
    elif "adding_products" in context.user_data and context.user_data["adding_products"]:
        await handle_product_input("add", update, context)
        
    elif "deleting_products" in context.user_data and context.user_data["deleting_products"]:
        await handle_product_input("delete", update, context)
        
    elif "adding_markets" in context.user_data and context.user_data["adding_markets"]:
        await handle_market_input("add", update, context)
        
    elif "deleting_markets" in context.user_data and context.user_data["deleting_markets"]:
        await handle_market_input("delete", update, context)
        
    elif "setting_zip_code" in context.user_data and context.user_data["setting_zip_code"]:
        await handle_zip_code_input(update, context)
    else:
        await update.message.reply_text("/start oder /help eingeben, um zu beginnen.")


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
    application.add_handler(CommandHandler("del_products", commands.del_products))
    application.add_handler(CommandHandler("del_markets", commands.del_markets))
    application.add_handler(CommandHandler("feedback", commands.feedback))
    application.add_handler(CommandHandler("notify_now", commands.notify_now))
    
    # Täglich nach neuen Angeboten suchen und Nutzer benachrichtigen
    scheduler = BackgroundScheduler()
    scheduler.add_job(notify_users_with_new_offers, "cron", hour=9, minute=0, args=[TOKEN], timezone="Europe/Berlin")
    scheduler.start()
    
    application.run_polling()

main()