"""ArXiv API search and PDF text extraction."""

import logging
import re
import tempfile
import aiohttp
import feedparser

from config import MAX_PAPER_TEXT_CHARS
from db.models import Paper

logger = logging.getLogger(__name__)

ARXIV_API_URL = "http://export.arxiv.org/api/query"


class ArxivService:
    async def search(self, query: str, max_results: int = 10) -> list[Paper]:
        """Search ArXiv for papers matching query."""
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ARXIV_API_URL, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        logger.error(f"ArXiv API returned {resp.status}")
                        return []
                    text = await resp.text()

            feed = feedparser.parse(text)
            papers = []
            for entry in feed.entries:
                arxiv_id = self._extract_arxiv_id(entry.get("id", ""))
                if not arxiv_id:
                    continue

                authors = [a.get("name", "") for a in entry.get("authors", [])]
                papers.append(Paper(
                    arxiv_id=arxiv_id,
                    title=entry.get("title", "").replace("\n", " ").strip(),
                    authors=str(authors),
                    abstract=entry.get("summary", "").replace("\n", " ").strip(),
                    published_date=entry.get("published", "")[:10],
                    arxiv_url=f"https://arxiv.org/abs/{arxiv_id}",
                    pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
                    source="arxiv",
                ))
            return papers

        except Exception as e:
            logger.error(f"ArXiv search error: {e}")
            return []

    async def fetch_paper_by_id(self, arxiv_id: str) -> Paper | None:
        """Fetch a single paper by ArXiv ID."""
        # Clean the ID
        arxiv_id = arxiv_id.strip()
        arxiv_id = re.sub(r'^(https?://)?arxiv\.org/(abs|pdf)/', '', arxiv_id)
        arxiv_id = arxiv_id.rstrip('.pdf').rstrip('/')

        params = {
            "id_list": arxiv_id,
            "max_results": 1,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ARXIV_API_URL, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return None
                    text = await resp.text()

            feed = feedparser.parse(text)
            if not feed.entries:
                return None

            entry = feed.entries[0]
            parsed_id = self._extract_arxiv_id(entry.get("id", ""))
            if not parsed_id:
                return None

            authors = [a.get("name", "") for a in entry.get("authors", [])]
            return Paper(
                arxiv_id=parsed_id,
                title=entry.get("title", "").replace("\n", " ").strip(),
                authors=str(authors),
                abstract=entry.get("summary", "").replace("\n", " ").strip(),
                published_date=entry.get("published", "")[:10],
                arxiv_url=f"https://arxiv.org/abs/{parsed_id}",
                pdf_url=f"https://arxiv.org/pdf/{parsed_id}",
                source="arxiv",
            )

        except Exception as e:
            logger.error(f"ArXiv fetch error for {arxiv_id}: {e}")
            return None

    async def extract_pdf_text(self, pdf_url: str) -> str | None:
        """Download PDF and extract text using pymupdf4llm."""
        try:
            import pymupdf4llm

            async with aiohttp.ClientSession() as session:
                async with session.get(pdf_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status != 200:
                        logger.error(f"PDF download failed: {resp.status}")
                        return None
                    pdf_bytes = await resp.read()

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
                tmp.write(pdf_bytes)
                tmp.flush()
                text = pymupdf4llm.to_markdown(tmp.name)

            if text:
                return text[:MAX_PAPER_TEXT_CHARS]
            return None

        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return None

    def _extract_arxiv_id(self, url: str) -> str:
        """Extract ArXiv ID from URL or ID string."""
        match = re.search(r'(\d{4}\.\d{4,5})(v\d+)?', url)
        if match:
            return match.group(1)
        # Try older format
        match = re.search(r'arxiv\.org/abs/([a-z-]+/\d+)', url)
        if match:
            return match.group(1)
        return ""
