import json
from telegram import Update
from telegram.ext import ContextTypes

from user import User
from utils import check_for_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    with open("bot/known_users.json", "r") as f:
        known_users = json.load(f)
    
    if str(update.effective_user.id) not in known_users:
        user = User(
            id=update.effective_user.id,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
            zip_code=None,
            markets=None,
            products=None,
        )
        known_users[user.id] = user.to_dict()
        with open("bot/known_users.json", "w") as f:
            json.dump(known_users, f, indent=4)
    else:
        user_data = known_users[str(update.effective_user.id)]
        user = User(**user_data) 
    
    await update.message.reply_text(
        f"Hi {user.first_name}, schön dich zu sehen :) \n" \
        "Mit /help erhälst du mehr Infos")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Dieser Bot wird dich benachrichtigen, sobald deine Lieblingsprodukte im Angebot sind. \n\n" \
        "Du wirst für alle Produkte auf deiner Watchlist benachrichtigt, " \
        "allerdings nur, wenn sie auch bei Supermärkten auf deiner Watchlist im Angebot sind. \n" \
        "Wenn du noch keine Supermärkte eingetragen hast, wirst du standardmäßig für alle "\
        "Supermärkte benachrichtigt.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Verfügbare Kommandos: \n" \
        "/start - Bot starten \n" \
        "/about - Was tut dieser Bot? \n" \
        "/help - Hilfe anfordern \n" \
        "/set_zip - Postleitzahl konfigurieren \n" \
        "/add_products - Produkte zur Watchlist hinzufügen \n" \
        "/del_products - Produkte von der Watchlist entfernen \n" \
        "/add_markets - Supermärkte zur Watchlist hinzufügen \n" \
        "/del_markets - Supermärkte von der Watchlist entfernen \n" \
        "/show_me - Zeige meinen Konfigurationsstand \n")


async def set_zip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await check_for_user(update)
    if user is None: return
    
    context.user_data["setting_zip_code"] = True
    context.user_data["user"] = user
    
    await update.message.reply_text("Bitte schick mir deine PLZ")


async def add_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await check_for_user(update)
    if user is None: return
    
    context.user_data["adding_products"] = True
    context.user_data["user"] = user
    
    await update.message.reply_text("Bitte schick mir ein Einzelnes oder eine Liste von Produkten, mit Kommas getrennt")
    

async def del_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await check_for_user(update)
    if user is None: return
    
    await update.message.reply_text("Noch nicht implementiert")


async def add_markets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await check_for_user(update)
    if user is None: return
    
    context.user_data["user"] = user
    context.user_data["adding_markets"] = True
    
    await update.message.reply_text("Bitte schick mir einen Einzelnen oder eine Liste von Supermärkten, mit Kommas getrennt")
    
    
async def del_markets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await check_for_user(update)
    if user is None: return
    
    await update.message.reply_text("Noch nicht implementiert")


async def show_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await check_for_user(update)
    if user is None: return
    
    formatted_user = json.dumps(user.to_dict(), indent=4)
    await update.message.reply_text(formatted_user)
