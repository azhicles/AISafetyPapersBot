"""Handlers for /add, /remove, /return, /collection, /past, /next, /current."""

import json
import re
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.middleware import ensure_registered
from db import repository as repo
from db.models import Paper
import services

logger = logging.getLogger(__name__)


async def _deliver_paper(chat_id: int, paper: Paper, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Format and deliver a paper, generating summary if needed."""
    summarizer = services.get_summarizer()
    fetcher = services.get_paper_fetcher()

    # Ensure we have full text (lazy load)
    paper = await fetcher.ensure_paper_text(paper)

    # Generate summary if not cached
    if not paper.summary:
        summary = await summarizer.summarize(
            title=paper.title,
            authors=paper.authors,
            abstract=paper.abstract,
            full_text=paper.full_text,
        )
        if summary:
            await repo.update_paper_summary(paper.id, summary)
            paper.summary = summary

    # Format message
    try:
        authors_list = json.loads(paper.authors)
        authors_str = ", ".join(authors_list[:5])
        if len(authors_list) > 5:
            authors_str += f" (+{len(authors_list) - 5} more)"
    except (json.JSONDecodeError, TypeError):
        authors_str = paper.authors

    msg = f"📄 *{_escape_md(paper.title)}*\n\n"
    msg += f"👤 {_escape_md(authors_str)}\n"
    msg += f"📅 {paper.published_date}\n"
    msg += f"🔗 {paper.arxiv_url}\n\n"

    if paper.summary:
        msg += f"{paper.summary}\n\n"
    else:
        msg += f"*Abstract:*\n{_escape_md(paper.abstract[:500])}\n\n"
        msg += "_Could not generate summary at this time._\n\n"

    msg += "_Use /rate <1-5> to rate or just send a message to discuss!_"

    # Mark as sent and set as current
    await repo.mark_paper_sent(chat_id, paper.id)
    await repo.set_current_paper(chat_id, paper.id)

    return msg


def _escape_md(text: str) -> str:
    """Escape markdown special characters for Telegram."""
    # Only escape characters that break Markdown v1
    for char in ['_', '*', '[', ']', '`']:
        text = text.replace(char, f'\\{char}')
    return text


@ensure_registered
async def next_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /next command - deliver next paper from queue."""
    chat_id = update.effective_chat.id

    paper = await repo.get_next_queued_paper(chat_id)

    if not paper:
        # Queue exhausted - try novel discovery
        await update.effective_message.reply_text(
            "Queue exhausted! Searching for a new paper...",
        )
        fetcher = services.get_paper_fetcher()
        paper = await fetcher.discover_novel_paper(chat_id)
        if paper:
            await repo.add_paper_to_chat(chat_id, paper.id, added_by="discovery")
        else:
            await update.effective_message.reply_text(
                "Couldn't find a new paper right now. Try /add to add one manually, or try again later."
            )
            return

    msg = await _deliver_paper(chat_id, paper, context)
    await update.effective_message.reply_text(msg, parse_mode="Markdown")


@ensure_registered
async def current_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /current command - show current paper."""
    chat_id = update.effective_chat.id
    ctx = await repo.get_chat_context(chat_id)

    if not ctx.current_paper_id:
        await update.effective_message.reply_text(
            "No current paper. Use /next to get one!"
        )
        return

    paper = await repo.get_paper(ctx.current_paper_id)
    if not paper:
        await update.effective_message.reply_text(
            "Could not find current paper. Use /next to get a new one."
        )
        return

    try:
        authors_list = json.loads(paper.authors)
        authors_str = ", ".join(authors_list[:5])
    except (json.JSONDecodeError, TypeError):
        authors_str = paper.authors

    msg = f"📄 *Current Paper:*\n\n"
    msg += f"*{_escape_md(paper.title)}*\n"
    msg += f"👤 {_escape_md(authors_str)}\n"
    msg += f"📅 {paper.published_date}\n"
    msg += f"🔗 {paper.arxiv_url}\n"

    avg, count = await repo.get_paper_avg_rating(chat_id, paper.id)
    if count > 0:
        msg += f"\n⭐ Rating: {avg}/5 ({count} ratings)"

    await update.effective_message.reply_text(msg, parse_mode="Markdown")


def _is_arxiv_id(text: str) -> bool:
    """Check if text looks like an ArXiv ID (e.g. 2306.12001)."""
    return bool(re.match(r'^\d{4}\.\d{4,5}$', text))


@ensure_registered
async def add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add <arxiv_id or paper name>."""
    chat_id = update.effective_chat.id

    if not context.args:
        await update.effective_message.reply_text(
            "Usage:\n"
            "  /add 2306.12001 — add by ArXiv ID\n"
            "  /add RLHF survey — search by name"
        )
        return

    query = " ".join(context.args).strip()

    # If it looks like an arxiv ID, add directly
    if _is_arxiv_id(query):
        await _add_by_arxiv_id(update, chat_id, query)
        return

    # Otherwise treat as a name search
    await update.effective_message.reply_text(f"Searching ArXiv for: {query}...")

    fetcher = services.get_paper_fetcher()
    papers = await fetcher.search_papers(query, max_results=5)

    if not papers:
        await update.effective_message.reply_text("No papers found. Try a different query or use an ArXiv ID.")
        return

    # Show results with inline keyboard
    msg = f"*Results for:* {_escape_md(query)}\n\n"
    buttons = []
    for i, paper in enumerate(papers):
        msg += f"{i+1}. *{_escape_md(paper.title[:70])}*\n"
        msg += f"   {paper.published_date} | {paper.arxiv_url}\n\n"
        buttons.append([InlineKeyboardButton(
            f"{i+1}. {paper.title[:40]}",
            callback_data=f"add:{paper.arxiv_id}",
        )])

    buttons.append([InlineKeyboardButton("Cancel", callback_data="add:cancel")])

    await update.effective_message.reply_text(
        msg,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def add_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button press for /add search results."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if not data or not data.startswith("add:"):
        return

    arxiv_id = data.split(":", 1)[1]

    if arxiv_id == "cancel":
        await query.edit_message_text("Cancelled.")
        return

    chat_id = update.effective_chat.id

    # Check registration
    chat = await repo.get_chat(chat_id)
    if not chat or not chat.is_active:
        await query.edit_message_text("Please use /start first.")
        return

    await query.edit_message_text(f"Adding paper {arxiv_id}...")
    await _add_by_arxiv_id_edit(query, chat_id, arxiv_id, update.effective_user)


async def _add_by_arxiv_id(update: Update, chat_id: int, arxiv_id: str) -> None:
    """Add a paper by ArXiv ID (from /add command)."""
    await update.effective_message.reply_text("Fetching paper...")

    fetcher = services.get_paper_fetcher()
    paper = await fetcher.fetch_by_arxiv_id(arxiv_id)

    if not paper:
        await update.effective_message.reply_text(f"Could not find paper with ID: {arxiv_id}")
        return

    evaluator = services.get_paper_evaluator()
    is_relevant, explanation = await evaluator.is_relevant(paper.title, paper.abstract)

    if not is_relevant:
        await update.effective_message.reply_text(
            f"This paper doesn't appear to be AI safety related:\n_{_escape_md(explanation)}_\n\n"
            "It will still be added, but note it may not be the best fit.",
            parse_mode="Markdown",
        )

    user_name = update.effective_user.first_name if update.effective_user else "user"
    await repo.add_paper_to_chat(chat_id, paper.id, added_by=user_name)

    await update.effective_message.reply_text(
        f"✅ Added: *{_escape_md(paper.title)}*\n"
        f"📅 {paper.published_date}\n"
        f"🔗 {paper.arxiv_url}",
        parse_mode="Markdown",
    )


async def _add_by_arxiv_id_edit(query, chat_id: int, arxiv_id: str, user) -> None:
    """Add a paper by ArXiv ID (from callback button, edits the message)."""
    fetcher = services.get_paper_fetcher()
    paper = await fetcher.fetch_by_arxiv_id(arxiv_id)

    if not paper:
        await query.edit_message_text(f"Could not find paper: {arxiv_id}")
        return

    user_name = user.first_name if user else "user"
    await repo.add_paper_to_chat(chat_id, paper.id, added_by=user_name)

    await query.edit_message_text(
        f"✅ Added: {paper.title}\n"
        f"📅 {paper.published_date}\n"
        f"🔗 {paper.arxiv_url}",
    )


@ensure_registered
async def remove_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /remove <arxiv_id> command."""
    chat_id = update.effective_chat.id

    if not context.args:
        await update.effective_message.reply_text(
            "Usage: /remove <arxiv_id>\nExample: /remove 2306.12001"
        )
        return

    arxiv_id = context.args[0].strip()
    paper = await repo.get_paper_by_arxiv_id(arxiv_id)

    if not paper:
        await update.effective_message.reply_text(f"Paper not found: {arxiv_id}")
        return

    removed = await repo.remove_paper_from_chat(chat_id, paper.id)
    if removed:
        await update.effective_message.reply_text(
            f"✅ Removed: {paper.title}"
        )
    else:
        await update.effective_message.reply_text(
            "Paper was not in your collection."
        )


@ensure_registered
async def collection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /collection command - list all papers in the chat's collection."""
    chat_id = update.effective_chat.id
    collection = await repo.get_chat_collection(chat_id)

    if not collection:
        await update.effective_message.reply_text("Your collection is empty. Use /add to add papers.")
        return

    queued = [(p, s) for p, s in collection if s == "queued"]
    sent = [(p, s) for p, s in collection if s == "sent"]

    msg = f"📚 *Your Collection* ({len(collection)} papers)\n\n"
    msg += f"📬 Queued: {len(queued)} | ✅ Sent: {len(sent)}\n\n"

    # Show first 20 queued papers
    if queued:
        msg += "*Upcoming:*\n"
        for i, (paper, _) in enumerate(queued[:20]):
            msg += f"{i+1}. {paper.title[:60]}\n"
        if len(queued) > 20:
            msg += f"_...and {len(queued) - 20} more_\n"

    await update.effective_message.reply_text(msg, parse_mode="Markdown")


@ensure_registered
async def past_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /past command - list previously sent papers."""
    chat_id = update.effective_chat.id
    papers = await repo.get_sent_papers(chat_id, limit=20)

    if not papers:
        await update.effective_message.reply_text("No papers sent yet. Use /next to get your first one!")
        return

    msg = "📖 *Recently Sent Papers:*\n\n"
    for i, paper in enumerate(papers):
        avg, count = await repo.get_paper_avg_rating(chat_id, paper.id)
        rating_str = f" ⭐ {avg}/5 ({count})" if count > 0 else ""
        msg += f"{i+1}. {paper.title[:55]}{rating_str}\n"

        reviews = await repo.get_paper_reviews(chat_id, paper.id)
        for review in reviews[:2]:
            text = review.review_text[:80]
            msg += f"    💬 _{_escape_md(text)}_\n"

    await update.effective_message.reply_text(msg, parse_mode="Markdown")


@ensure_registered
async def return_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /return command - return the most recently sent paper back to the queue."""
    chat_id = update.effective_chat.id

    paper = await repo.return_last_sent_paper(chat_id)
    if not paper:
        await update.effective_message.reply_text("No sent papers to return.")
        return

    await update.effective_message.reply_text(
        f"↩️ Returned to queue: *{_escape_md(paper.title[:70])}*\n"
        "It will be the next paper delivered.",
        parse_mode="Markdown",
    )
