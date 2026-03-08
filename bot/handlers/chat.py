"""Handler for free-form messages (Q&A about current paper)."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from db import repository as repo
import services

logger = logging.getLogger(__name__)


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle free-form text messages for paper Q&A."""
    if not update.effective_message or not update.effective_message.text:
        return
    if not update.effective_chat:
        return

    chat_id = update.effective_chat.id
    message_text = update.effective_message.text

    # Check if chat is registered
    chat = await repo.get_chat(chat_id)
    if not chat:
        return  # Silently ignore unregistered chats

    # Group chat gating: only respond if @mentioned or replied to
    if chat.chat_type in ("group", "supergroup"):
        bot_username = context.bot.username
        is_mentioned = bot_username and f"@{bot_username}" in message_text
        is_reply_to_bot = (
            update.effective_message.reply_to_message
            and update.effective_message.reply_to_message.from_user
            and update.effective_message.reply_to_message.from_user.is_bot
            and update.effective_message.reply_to_message.from_user.username == bot_username
        )

        if not is_mentioned and not is_reply_to_bot:
            return  # Ignore messages not directed at the bot

        # Remove @mention from the message text
        if bot_username:
            message_text = message_text.replace(f"@{bot_username}", "").strip()

    if not message_text:
        return

    # Get response from chat service
    chat_svc = services.get_chat_service()
    response = await chat_svc.chat(chat_id, message_text)

    if response:
        await update.effective_message.reply_text(response, parse_mode="Markdown")
