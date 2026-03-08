"""Daily paper delivery scheduler using python-telegram-bot's JobQueue."""

import logging
import random
from datetime import time as dt_time

import pytz
from telegram.ext import ContextTypes

from config import CLASSIC_RATIO
from db import repository as repo
from db.models import Paper
from bot.handlers.paper_commands import _deliver_paper
import services

logger = logging.getLogger(__name__)


async def _deliver_to_chat(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Core delivery logic for a specific chat."""
    chat = await repo.get_chat(chat_id)
    if not chat or not chat.is_active:
        return

    paper = await _select_paper(chat_id)
    if not paper:
        logger.info(f"No paper to deliver for chat {chat_id}")
        return

    # Ensure paper is in chat's collection
    chat_paper_ids = await repo.get_chat_paper_ids(chat_id)
    if paper.id not in chat_paper_ids:
        await repo.add_paper_to_chat(chat_id, paper.id, added_by="scheduler")

    try:
        msg = await _deliver_paper(chat_id, paper, context)
        await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
        await repo.mark_scheduled_delivery(chat_id)
        logger.info(f"Delivered paper '{paper.title[:50]}' to chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to deliver paper to chat {chat_id}: {e}")


async def deliver_daily_paper(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Job callback: deliver a paper to a specific chat (for manual run_once triggers)."""
    chat_id = context.job.chat_id
    if not chat_id:
        return
    await _deliver_to_chat(chat_id, context)


async def _select_paper(chat_id: int) -> Paper | None:
    """Select paper using 80/20 logic (collection vs novel)."""
    queued_count = await repo.get_queued_count(chat_id)

    if queued_count == 0:
        # Queue exhausted - 100% novel discovery
        fetcher = services.get_paper_fetcher()
        return await fetcher.discover_novel_paper(chat_id)

    # 80/20 split: collection vs novel
    if random.random() < CLASSIC_RATIO:
        # Pick from queue
        return await repo.get_next_queued_paper(chat_id)
    else:
        # Try novel discovery
        fetcher = services.get_paper_fetcher()
        paper = await fetcher.discover_novel_paper(chat_id)
        if paper:
            return paper
        # Fallback to queue
        return await repo.get_next_queued_paper(chat_id)


def schedule_daily_jobs(job_queue, chats: list | None = None) -> None:
    """Schedule daily paper delivery for all active chats.
    Called at startup; individual chat jobs are also created on /start."""
    # Check every 5 minutes so we can match HH:MM send times
    job_queue.run_repeating(
        _periodic_check,
        interval=300,  # every 5 minutes
        first=10,  # start after 10 seconds
        name="periodic_check",
    )
    logger.info("Periodic delivery check scheduled (every 5 min)")


async def _periodic_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check all active chats and deliver if it's their send time."""
    from datetime import datetime

    chats = await repo.get_active_chats()

    for chat in chats:
        try:
            tz = pytz.timezone(chat.timezone)
            now = datetime.now(tz)

            if now.hour == chat.send_hour and now.minute // 5 == chat.send_minute // 5:
                # Check if scheduler already delivered recently (ignores manual /next)
                if await repo.was_scheduled_recently(chat.chat_id, hours=20):
                    continue

                logger.info(f"Chat {chat.chat_id}: delivering paper ({now.hour}:{now.minute:02d}, tz={chat.timezone})")
                await _deliver_to_chat(chat.chat_id, context)
        except Exception as e:
            logger.error(f"Error checking delivery for chat {chat.chat_id}: {e}")
