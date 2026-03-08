"""Handlers for /start, /stop, /resume, /help."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from db import repository as repo
from db.seed import seed_database

logger = logging.getLogger(__name__)

WELCOME_MESSAGE = """Welcome to the AI Safety Papers Bot!

I'll deliver a curated AI safety research paper daily with an LLM-powered summary, and you can chat with me about any paper.

Your collection has been seeded with ~47 classic AI safety papers.

**Commands:**
/add <id or name> - Add a paper by ID or search
/collection - View your paper collection
/current - Show current paper
/help - Show this help message
/next - Get the next paper
/past - View previously sent papers
/rate <1-5> - Rate the current paper
/remove <arxiv\\_id> - Remove a paper
/resume - Resume deliveries
/return - Return last sent paper to queue
/review <text> - Write a review
/search <query> - Search your collection
/settings time <HH:MM> - Change daily send time
/start - Register and seed collection
/stats - View statistics
/stop - Pause daily deliveries

Just send me a message to discuss the current paper!"""

HELP_MESSAGE = WELCOME_MESSAGE


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    chat = update.effective_chat
    if not chat:
        return

    chat_type = chat.type if chat.type else "private"
    chat_title = chat.title or chat.first_name or "Unknown"

    # Register chat
    await repo.register_chat(chat.id, chat_type, chat_title)

    # Ensure seed papers exist
    await seed_database()

    # Seed papers to this chat's queue
    count = await repo.seed_papers_to_chat(chat.id)

    await update.effective_message.reply_text(
        WELCOME_MESSAGE + f"\n\n_{count} papers added to your queue._",
        parse_mode="Markdown",
    )


async def stop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stop command."""
    if not update.effective_chat:
        return

    chat_id = update.effective_chat.id
    chat = await repo.get_chat(chat_id)
    if not chat:
        await update.effective_message.reply_text("Use /start first.")
        return

    await repo.set_chat_active(chat_id, False)
    await update.effective_message.reply_text(
        "Daily paper deliveries paused. Use /resume to restart."
    )


async def resume_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /resume command."""
    if not update.effective_chat:
        return

    chat_id = update.effective_chat.id
    chat = await repo.get_chat(chat_id)
    if not chat:
        await update.effective_message.reply_text("Use /start first.")
        return

    await repo.set_chat_active(chat_id, True)
    await update.effective_message.reply_text(
        "Daily paper deliveries resumed! Use /next to get a paper now."
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await update.effective_message.reply_text(HELP_MESSAGE, parse_mode="Markdown")
