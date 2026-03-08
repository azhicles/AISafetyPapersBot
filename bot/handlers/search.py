"""Handler for /search command - LLM-powered search within collection."""

import json
import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.middleware import ensure_registered
from bot.handlers.paper_commands import _escape_md
from db import repository as repo
import services

logger = logging.getLogger(__name__)

SEARCH_PROMPT = """You are helping a user search their AI safety paper collection. Given the search query and the numbered list of papers below, return the numbers of the papers that are relevant to the query. Return ONLY a JSON array of numbers, e.g. [1, 5, 12]. If nothing matches, return [].

Query: {query}

Papers:
{paper_list}"""


@ensure_registered
async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /search <query> command - search within collection using LLM."""
    chat_id = update.effective_chat.id

    if not context.args:
        await update.effective_message.reply_text(
            "Usage: /search <query>\nExample: /search RLHF alignment"
        )
        return

    query = " ".join(context.args)
    collection = await repo.get_chat_collection(chat_id)

    if not collection:
        await update.effective_message.reply_text("Your collection is empty. Use /add to add papers first.")
        return

    await update.effective_message.reply_text(f"Searching collection for: {query}...")

    # Build numbered list for LLM
    paper_list = ""
    papers_by_idx = {}
    for i, (paper, status) in enumerate(collection, 1):
        paper_list += f"{i}. {paper.title}\n"
        papers_by_idx[i] = (paper, status)

    # Ask LLM to find relevant papers
    groq = services.get_groq_client()
    messages = [
        {"role": "system", "content": "You return only valid JSON arrays of integers. No other text."},
        {"role": "user", "content": SEARCH_PROMPT.format(query=query, paper_list=paper_list)},
    ]

    response = await groq.chat_completion(messages=messages, max_tokens=200, temperature=0.1)

    if not response:
        await update.effective_message.reply_text("Search failed. Please try again later.")
        return

    # Parse LLM response
    try:
        # Extract JSON array from response
        response = response.strip()
        if not response.startswith("["):
            start = response.find("[")
            end = response.rfind("]")
            if start != -1 and end != -1:
                response = response[start:end + 1]
        indices = json.loads(response)
        indices = [int(x) for x in indices if isinstance(x, (int, float)) and int(x) in papers_by_idx]
    except (json.JSONDecodeError, ValueError):
        # Fallback: simple text match
        indices = [
            i for i, (paper, _) in papers_by_idx.items()
            if query.lower() in paper.title.lower() or query.lower() in paper.abstract.lower()
        ]

    if not indices:
        await update.effective_message.reply_text(
            f"No papers in your collection match \"{query}\"."
        )
        return

    msg = f"*Search results for:* {_escape_md(query)}\n\n"
    for idx in indices[:10]:
        paper, status = papers_by_idx[idx]
        status_icon = "✅" if status == "sent" else "📬"
        msg += f"{status_icon} *{_escape_md(paper.title[:70])}*\n"
        msg += f"   {paper.published_date} | {paper.arxiv_url}\n\n"

    await update.effective_message.reply_text(msg, parse_mode="Markdown")
