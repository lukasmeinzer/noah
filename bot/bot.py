import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Define your command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi, schön dich zu sehen :)")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Get help")

def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return update.message.reply_text("test")

# Main function to run the bot
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
    application = Application.builder().token(TOKEN).build()

    # Add command handlers to the application
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("new", new_command))

    # Start the bot
    application.run_polling()

main()
