"""LLM-based relevance check for papers added via /add."""

import logging

from services.groq_client import GroqClient

logger = logging.getLogger(__name__)

RELEVANCE_PROMPT = """You are an AI safety research curator. Evaluate whether the following paper is relevant to AI safety research.

Title: {title}
Abstract: {abstract}

AI safety includes topics like: alignment, RLHF, interpretability, robustness, value alignment, corrigibility, mesa-optimization, scalable oversight, AI governance, reward hacking, deceptive alignment, jailbreaking, red teaming, AI ethics, and related areas.

Respond with exactly one word: "RELEVANT" or "IRRELEVANT"
Then on a new line, give a brief (1 sentence) explanation."""


class PaperEvaluator:
    def __init__(self, groq_client: GroqClient):
        self._groq = groq_client

    async def is_relevant(self, title: str, abstract: str) -> tuple[bool, str]:
        """Check if a paper is relevant to AI safety. Returns (is_relevant, explanation)."""
        prompt = RELEVANCE_PROMPT.format(title=title, abstract=abstract)
        messages = [
            {"role": "system", "content": "You are an AI safety research curator."},
            {"role": "user", "content": prompt},
        ]

        response = await self._groq.chat_completion(
            messages=messages, max_tokens=100, temperature=0.1,
        )

        if not response:
            # Default to relevant if we can't evaluate
            return True, "Could not evaluate relevance (API unavailable)."

        lines = response.strip().split("\n", 1)
        is_relevant = "RELEVANT" in lines[0].upper() and "IRRELEVANT" not in lines[0].upper()
        explanation = lines[1].strip() if len(lines) > 1 else ""
        return is_relevant, explanation
