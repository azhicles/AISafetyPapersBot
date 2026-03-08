"""Entry point for AI Safety Papers Bot."""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from db.schema import init_db
from db.seed import seed_database
from bot.handlers.start import start_handler, stop_handler, resume_handler, help_handler
from bot.handlers.paper_commands import (
    next_handler, current_handler, add_handler, add_callback_handler,
    remove_handler, collection_handler, past_handler, return_handler,
)
from bot.handlers.rating import rate_handler, review_handler
from bot.handlers.chat import chat_handler
from bot.handlers.stats import stats_handler
from bot.handlers.search import search_handler
from bot.handlers.settings import settings_handler
from bot.scheduler import schedule_daily_jobs

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context) -> None:
    """Log errors."""
    logger.error(f"Update {update} caused error: {context.error}")
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "An error occurred. Please try again."
            )
        except Exception:
            pass


async def post_init(application: Application) -> None:
    """Initialize database and seed data after the application starts."""
    logger.info("Initializing database...")
    await init_db()

    logger.info("Seeding papers...")
    count = await seed_database()
    logger.info(f"Seeded {count} papers")

    # Schedule daily delivery jobs
    schedule_daily_jobs(application.job_queue)
    logger.info("Scheduler started")


def main() -> None:
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set. Please set it in .env")
        return

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("stop", stop_handler))
    application.add_handler(CommandHandler("resume", resume_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("next", next_handler))
    application.add_handler(CommandHandler("current", current_handler))
    application.add_handler(CommandHandler("add", add_handler))
    application.add_handler(CommandHandler("remove", remove_handler))
    application.add_handler(CommandHandler("collection", collection_handler))
    application.add_handler(CommandHandler("past", past_handler))
    application.add_handler(CommandHandler("return", return_handler))
    application.add_handler(CommandHandler("rate", rate_handler))
    application.add_handler(CommandHandler("review", review_handler))
    application.add_handler(CommandHandler("stats", stats_handler))
    application.add_handler(CommandHandler("search", search_handler))
    application.add_handler(CommandHandler("settings", settings_handler))

    # Callback query handler (inline keyboard buttons)
    application.add_handler(CallbackQueryHandler(add_callback_handler, pattern=r"^add:"))

    # Free-form message handler (must be last)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler)
    )

    # Error handler
    application.add_error_handler(error_handler)

    # Start polling
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
