"""Rate-limited Groq API wrapper."""

import asyncio
import time
import logging
from groq import AsyncGroq
from aiolimiter import AsyncLimiter

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_RPM, GROQ_TPM

logger = logging.getLogger(__name__)


class GroqClient:
    def __init__(self):
        self._client = AsyncGroq(api_key=GROQ_API_KEY)
        self._rpm_limiter = AsyncLimiter(GROQ_RPM, 60)
        self._tpm_tokens = 0
        self._tpm_window_start = time.monotonic()

    async def _check_tpm(self, estimated_tokens: int) -> None:
        """Wait if we'd exceed TPM limit."""
        now = time.monotonic()
        if now - self._tpm_window_start >= 60:
            self._tpm_tokens = 0
            self._tpm_window_start = now

        if self._tpm_tokens + estimated_tokens > GROQ_TPM:
            wait_time = 60 - (now - self._tpm_window_start)
            if wait_time > 0:
                logger.info(f"TPM limit approaching, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
            self._tpm_tokens = 0
            self._tpm_window_start = time.monotonic()

    async def chat_completion(
        self,
        messages: list[dict],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str | None:
        """Send a chat completion request with rate limiting."""
        # Rough token estimate: 4 chars per token
        estimated_input_tokens = sum(len(m.get("content", "")) for m in messages) // 4
        estimated_total = estimated_input_tokens + max_tokens

        try:
            await self._check_tpm(estimated_total)
            async with self._rpm_limiter:
                response = await self._client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                # Track actual usage
                if response.usage:
                    self._tpm_tokens += response.usage.total_tokens

                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip()
                return None

        except Exception as e:
            logger.error(f"Groq API error: {e}")
            if "rate_limit" in str(e).lower():
                return "I've hit the rate limit. Please try again in a minute."
            return None
