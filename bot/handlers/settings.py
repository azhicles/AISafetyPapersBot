"""Handler for /settings command."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.middleware import ensure_registered
from db import repository as repo

logger = logging.getLogger(__name__)


@ensure_registered
async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command - view or change settings."""
    chat_id = update.effective_chat.id
    chat = await repo.get_chat(chat_id)

    if not context.args:
        msg = "⚙️ *Settings*\n\n"
        msg += f"🕐 Send time: {chat.send_hour}:{chat.send_minute:02d}\n"
        msg += f"🌍 Timezone: {chat.timezone}\n"
        msg += f"📡 Status: {'Active' if chat.is_active else 'Paused'}\n\n"
        msg += "To change:\n"
        msg += "`/settings time <HH:MM>` - Set send time (24h)\n"
        msg += "`/settings timezone <tz>` - Set timezone\n"
        await update.effective_message.reply_text(msg, parse_mode="Markdown")
        return

    setting = context.args[0].lower()

    if setting == "time" and len(context.args) >= 2:
        time_str = context.args[1].strip()
        try:
            if ":" in time_str:
                parts = time_str.split(":")
                hour, minute = int(parts[0]), int(parts[1])
            else:
                hour, minute = int(time_str), 0
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except (ValueError, IndexError):
            await update.effective_message.reply_text(
                "Please provide a time in 24h format, e.g. `14:30` or `9:00`",
                parse_mode="Markdown",
            )
            return

        await repo.update_chat_settings(chat_id, send_hour=hour, send_minute=minute)
        await update.effective_message.reply_text(
            f"✅ Daily send time updated to {hour}:{minute:02d} ({chat.timezone})"
        )

    elif setting == "timezone" and len(context.args) >= 2:
        import pytz
        tz_name = context.args[1]
        try:
            pytz.timezone(tz_name)
        except pytz.exceptions.UnknownTimeZoneError:
            await update.effective_message.reply_text(
                f"Unknown timezone: {tz_name}\n"
                "Examples: Asia/Singapore, US/Eastern, Europe/London"
            )
            return

        await repo.update_chat_settings(chat_id, timezone=tz_name)
        await update.effective_message.reply_text(
            f"✅ Timezone updated to {tz_name}"
        )

    else:
        await update.effective_message.reply_text(
            "Usage:\n"
            "`/settings time <HH:MM>` - Set send time (24h format)\n"
            "`/settings timezone <tz>` - Set timezone",
            parse_mode="Markdown",
        )
