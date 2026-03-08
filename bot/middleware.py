"""Middleware for ensuring chat registration before command processing."""

import logging
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from db import repository as repo

logger = logging.getLogger(__name__)


def ensure_registered(func):
    """Decorator that ensures the chat is registered before handling a command."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_chat:
            return
        chat_id = update.effective_chat.id
        chat = await repo.get_chat(chat_id)
        if not chat:
            await update.effective_message.reply_text(
                "Please use /start first to register this chat."
            )
            return
        if not chat.is_active:
            await update.effective_message.reply_text(
                "This chat is paused. Use /resume to reactivate."
            )
            return
        return await func(update, context)
    return wrapper
