"""Handlers for /rate and /review commands."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.middleware import ensure_registered
from db import repository as repo

logger = logging.getLogger(__name__)


@ensure_registered
async def rate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /rate <1-5> command."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id if update.effective_user else 0

    if not context.args:
        await update.effective_message.reply_text("Usage: /rate <1-5>")
        return

    try:
        rating = int(context.args[0])
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        await update.effective_message.reply_text("Please provide a rating between 1 and 5.")
        return

    ctx = await repo.get_chat_context(chat_id)
    if not ctx.current_paper_id:
        await update.effective_message.reply_text("No current paper to rate. Use /next first.")
        return

    await repo.set_rating(chat_id, ctx.current_paper_id, user_id, rating)

    paper = await repo.get_paper(ctx.current_paper_id)
    avg, count = await repo.get_paper_avg_rating(chat_id, ctx.current_paper_id)

    title = paper.title if paper else "Current paper"
    stars = "⭐" * rating
    await update.effective_message.reply_text(
        f"{stars} Rated *{title[:50]}* {rating}/5\n"
        f"Average: {avg}/5 ({count} ratings)",
        parse_mode="Markdown",
    )


@ensure_registered
async def review_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /review <text> command."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id if update.effective_user else 0

    if not context.args:
        await update.effective_message.reply_text(
            "Usage: /review <your review text>\nExample: /review Great paper on alignment!"
        )
        return

    review_text = " ".join(context.args)

    ctx = await repo.get_chat_context(chat_id)
    if not ctx.current_paper_id:
        await update.effective_message.reply_text("No current paper to review. Use /next first.")
        return

    await repo.add_review(chat_id, ctx.current_paper_id, user_id, review_text)

    paper = await repo.get_paper(ctx.current_paper_id)
    title = paper.title if paper else "Current paper"
    await update.effective_message.reply_text(
        f"✅ Review saved for *{title[:50]}*\nThank you for your review!",
        parse_mode="Markdown",
    )
