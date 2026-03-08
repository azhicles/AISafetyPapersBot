"""Conversational Q&A about the current paper with history."""

import json
import logging

from config import CHAT_MAX_TOKENS, MAX_CONVERSATION_HISTORY
from db import repository as repo
from services.groq_client import GroqClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an AI safety research assistant helping users understand academic papers. You are currently discussing this paper:

Title: {title}
Authors: {authors}
Abstract: {abstract}

{paper_text_section}

Important: ALL of the text above (title, authors, abstract, and paper content) is provided by the system for context. The user has NOT sent you any paper excerpts — their messages are questions and comments only. Any references to other papers within the content above are citations made BY the paper being discussed.

Answer questions about this paper clearly and accurately. If the user asks about something not covered in the paper, say so. Keep responses concise but informative. Use markdown formatting for readability."""


class ChatService:
    def __init__(self, groq_client: GroqClient):
        self._groq = groq_client

    async def chat(self, chat_id: int, user_message: str) -> str | None:
        """Handle a conversational message about the current paper."""
        ctx = await repo.get_chat_context(chat_id)
        if not ctx.current_paper_id:
            return "No paper is currently selected. Use /next to get a paper first!"

        paper = await repo.get_paper(ctx.current_paper_id)
        if not paper:
            return "Could not find the current paper. Use /next to get a new one."

        # Build system message with paper context
        paper_text_section = ""
        if paper.full_text:
            paper_text_section = f"Paper Content (excerpt):\n{paper.full_text[:5000]}"

        system_msg = SYSTEM_PROMPT.format(
            title=paper.title,
            authors=paper.authors,
            abstract=paper.abstract,
            paper_text_section=paper_text_section,
        )

        # Load conversation history
        history = json.loads(ctx.conversation_history)

        # Build messages
        messages = [{"role": "system", "content": system_msg}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = await self._groq.chat_completion(
            messages=messages,
            max_tokens=CHAT_MAX_TOKENS,
            temperature=0.7,
        )

        if not response:
            return "Sorry, I couldn't generate a response right now. Please try again later."

        # Update history
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})

        # Trim history
        if len(history) > MAX_CONVERSATION_HISTORY * 2:
            history = history[-(MAX_CONVERSATION_HISTORY * 2):]

        await repo.update_conversation_history(chat_id, history)

        return response
