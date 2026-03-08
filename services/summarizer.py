"""LLM-powered paper summarization service."""

import logging

from config import SUMMARY_MAX_TOKENS
from services.groq_client import GroqClient

logger = logging.getLogger(__name__)

SUMMARY_PROMPT = """Summarize this AI safety paper. Output ONLY the summary — no headers with #, no preamble, no repetition of the title/authors, and do not echo these instructions.

Title: {title}
Authors: {authors}
Abstract: {abstract}

{paper_text_section}

Use exactly this format (keep the bold labels, use plain text after each — no bullet points except for Takeaways):

**Key Contribution:** One sentence.

**Summary:** 3-5 sentences on the main ideas, methods, and findings.

**Why It Matters:** 1-2 sentences on AI safety relevance.

**Takeaways:**
- First insight
- Second insight
- Third insight (optional)"""


class SummarizerService:
    def __init__(self, groq_client: GroqClient):
        self._groq = groq_client

    async def summarize(
        self, title: str, authors: str, abstract: str, full_text: str | None = None
    ) -> str | None:
        """Generate a structured summary of a paper."""
        paper_text_section = ""
        if full_text:
            paper_text_section = f"Paper Content (excerpt):\n{full_text[:6000]}"

        prompt = SUMMARY_PROMPT.format(
            title=title,
            authors=authors,
            abstract=abstract,
            paper_text_section=paper_text_section,
        )

        messages = [
            {"role": "system", "content": "You are an expert AI safety researcher. Output only the requested summary — no markdown headers (#), no preamble, no repeated title/authors. Use **bold** labels only as instructed."},
            {"role": "user", "content": prompt},
        ]

        return await self._groq.chat_completion(
            messages=messages,
            max_tokens=SUMMARY_MAX_TOKENS,
            temperature=0.3,
        )
