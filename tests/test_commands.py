import sys
import os
import pytest
from unittest.mock import patch, AsyncMock
from aiogram.types import Update, User as TelegramUser, Message, Chat
from aiogram.fsm.context import FSMContext as Context
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.commands import start, notify_now, about
from bot.user import User, load_user, save_user, check_for_user
from bot.notify import notify_single_user_with_current_offers

@pytest.fixture
def telegram_user():
    return TelegramUser(id=12345, is_bot=False, first_name="Test", last_name="User", username="testuser", frozen=False)

@pytest.fixture
def update(telegram_user):
    chat = Chat(id=12345, type="private")
    message = Message(message_id=1, from_user=telegram_user, chat=chat, date=datetime.now(), text="/start", frozen=False)
    message.reply_text = AsyncMock()  # Mock reply_text method directly on the message instance
    update = Update(update_id=1, message=message, frozen=False)
    update.effective_user = telegram_user  # Add effective_user attribute to the update
    return update

@pytest.fixture
def context():
    storage = MemoryStorage()
    key = "test_key"
    return Context(storage=storage, key=key)

@pytest.mark.asyncio
async def test_start_new_user(update, context):
    with patch('bot.user.load_user', return_value=None) as mock_load_user, \
         patch('bot.user.save_user') as mock_save_user:

        await start(update, context)

        mock_load_user.assert_called_once_with(id=update.effective_user.id)
        mock_save_user.assert_called_once()
        update.message.reply_text.assert_called_once_with(
            "Hi Test, schön dich zu sehen :) \nDu bist scheinbar zum ersten Mal hier! Mit /about erfährst du was dieser Bot kann. \nMit /help siehst du alle verfügbaren Kommandos. \nAm Anfang ist es auch sinnvoll, deine Postleitzahl mit /set_zip anzugeben"
        )

@pytest.mark.asyncio
async def test_start_known_user(update, context):
    user = User(id=12345, first_name="Test", last_name="User", zip_code=None, markets=None, products=None)
    with patch('bot.user.load_user', return_value=user) as mock_load_user:

        await start(update, context)

        mock_load_user.assert_called_once_with(id=update.effective_user.id)
        update.message.reply_text.assert_called_once_with(
            "Hi Test, schön dich zu sehen :) \nMit /help siehst du alle verfügbaren Kommandos."
        )

@pytest.mark.asyncio
async def test_notify_now(update, context):
    user = User(id=12345, first_name="Test", last_name="User", zip_code=None, markets=None, products=None)
    with patch('bot.user.check_for_user', return_value=user) as mock_check_for_user, \
         patch('bot.notify.notify_single_user_with_current_offers') as mock_notify_single_user_with_current_offers:

        await notify_now(update, context)

        mock_check_for_user.assert_called_once_with(update)
        mock_notify_single_user_with_current_offers.assert_called_once_with(user, context.bot.token)

@pytest.mark.asyncio
async def test_about(update, context):
    await about(update, context)

    update.message.reply_text.assert_called_once_with(
        "Dieser Bot wird dich täglich um 9 Uhr benachrichtigen, sobald deine Lieblingsprodukte im Angebot sind. \n\nDu wirst für alle Produkte auf deiner Watchlist benachrichtigt, "
    )