"""Orchestrator for fetching paper metadata, content, and novel papers."""

import logging
import random

from config import SAFETY_TOPICS
from db.models import Paper
from db import repository as repo
from services.arxiv_service import ArxivService
from services.semantic_scholar import SemanticScholarService

logger = logging.getLogger(__name__)


class PaperFetcher:
    def __init__(self, arxiv: ArxivService, semantic_scholar: SemanticScholarService):
        self._arxiv = arxiv
        self._s2 = semantic_scholar

    async def fetch_by_arxiv_id(self, arxiv_id: str) -> Paper | None:
        """Fetch a paper by ArXiv ID (from API or DB cache)."""
        # Check DB first
        existing = await repo.get_paper_by_arxiv_id(arxiv_id)
        if existing:
            return existing

        # Fetch from ArXiv
        paper = await self._arxiv.fetch_paper_by_id(arxiv_id)
        if paper:
            paper_id = await repo.upsert_paper(paper)
            paper.id = paper_id
            return paper

        return None

    async def ensure_paper_text(self, paper: Paper) -> Paper:
        """Lazily load full text for a paper if not already cached."""
        if paper.full_text:
            return paper

        text = await self._arxiv.extract_pdf_text(paper.pdf_url)
        if text:
            await repo.update_paper_text(paper.id, text)
            paper.full_text = text

        return paper

    async def discover_novel_paper(self, chat_id: int) -> Paper | None:
        """Discover a novel paper not already in chat's collection."""
        known_ids = await repo.get_all_known_arxiv_ids_for_chat(chat_id)

        # Try random safety topic on ArXiv
        topic = random.choice(SAFETY_TOPICS)
        logger.info(f"Discovering novel paper with topic: {topic}")

        papers = await self._arxiv.search(topic, max_results=20)
        novel = [p for p in papers if p.arxiv_id not in known_ids]

        if not novel:
            # Fallback to Semantic Scholar
            papers = await self._s2.search(topic, max_results=20)
            novel = [p for p in papers if p.arxiv_id not in known_ids]

        if not novel:
            return None

        # Pick a random novel paper
        paper = random.choice(novel)
        paper_id = await repo.upsert_paper(paper)
        paper.id = paper_id
        return paper

    async def search_papers(self, query: str, max_results: int = 10) -> list[Paper]:
        """Search for papers across sources."""
        papers = await self._arxiv.search(query, max_results=max_results)
        if not papers:
            papers = await self._s2.search(query, max_results=max_results)
        return papers
