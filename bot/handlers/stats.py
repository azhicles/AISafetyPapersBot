"""Handler for /stats command."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.middleware import ensure_registered
from db import repository as repo

logger = logging.getLogger(__name__)


@ensure_registered
async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command - show collection statistics."""
    chat_id = update.effective_chat.id
    stats = await repo.get_chat_stats(chat_id)

    msg = "📊 *Collection Statistics*\n\n"
    msg += f"📚 Total papers: {stats['total_papers']}\n"
    msg += f"📬 Queued: {stats['queued']}\n"
    msg += f"✅ Sent: {stats['sent']}\n"
    msg += f"⭐ Rated: {stats['rated']} papers\n"
    if stats['avg_rating']:
        msg += f"📈 Average rating: {stats['avg_rating']}/5\n"
    msg += f"📝 Reviewed: {stats['reviewed']} papers\n"

    await update.effective_message.reply_text(msg, parse_mode="Markdown")
