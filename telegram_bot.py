from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
load_dotenv()
from database import Session
from models import User, Offer


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Use your API token from BotFather
app = Application.builder().token(BOT_TOKEN).build()

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initialize bot for new user."""
    session = Session()
    user = session.query(User).filter_by(chat_id=update.message.chat_id).first()
    print("_________________")
    print(update.message.chat_id)
    
    if not user:
        user = User(chat_id=update.message.chat_id)
        session.add(user)
        session.commit()
        await update.message.reply_text("Welcome! I’ve registered you. Use /add <offer> to track offers.")
    else:
        await update.message.reply_text("You’re already registered! Use /add <offer> to track more offers.")
    
    session.close()

async def add_offer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add an offer to user’s watchlist."""
    session = Session()
    user = session.query(User).filter_by(chat_id=update.message.chat_id).first()
    
    if user and context.args:
        offer_name = ' '.join(context.args)
        offer = Offer(name=offer_name, user=user)
        session.add(offer)
        session.commit()
        await update.message.reply_text(f"Offer '{offer_name}' added to your watchlist.")
    else:
        await update.message.reply_text("Please use /add <offer> to specify an offer.")
    
    session.close()

async def del_offer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove an offer from user’s watchlist."""
    session = Session()
    user = session.query(User).filter_by(chat_id=update.message.chat_id).first()
    
    if user and context.args:
        offer_name = ' '.join(context.args)
        offer = session.query(Offer).filter_by(user=user, name=offer_name).first()
        
        if offer:
            session.delete(offer)
            session.commit()
            await update.message.reply_text(f"Offer '{offer_name}' removed from your watchlist.")
        else:
            await update.message.reply_text(f"Couldn’t find offer '{offer_name}' in your watchlist.")
    else:
        await update.message.reply_text("Please specify the offer to delete with /del <offer>.")
    
    session.close()

async def list_offers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all offers in user’s watchlist."""
    session = Session()
    user = session.query(User).filter_by(chat_id=update.message.chat_id).first()
    
    if user and user.offers:
        offers = "\n".join(offer.name for offer in user.offers)
        await update.message.reply_text(f"Offers you’re tracking:\n{offers}")
    else:
        await update.message.reply_text("You’re not tracking any offers. Use /add <offer> to add one.")
    
    session.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide help information to user."""
    help_text = (
        "/start - Register with the bot\n"
        "/add <offer> - Add an offer to your watchlist\n"
        "/del <offer> - Remove an offer from your watchlist\n"
        "/list - List all offers you’re tracking\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)

# Set up command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_offer))
app.add_handler(CommandHandler("del", del_offer))
app.add_handler(CommandHandler("list", list_offers))
app.add_handler(CommandHandler("help", help_command))

# Run the bot
if __name__ == "__main__":
    print("Starting bot...")
    app.run_polling()