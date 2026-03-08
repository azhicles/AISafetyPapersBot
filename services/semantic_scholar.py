"""Semantic Scholar API as a backup search service."""

import logging
import aiohttp

from db.models import Paper

logger = logging.getLogger(__name__)

S2_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


class SemanticScholarService:
    async def search(self, query: str, max_results: int = 10) -> list[Paper]:
        """Search Semantic Scholar for papers."""
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,abstract,externalIds,url,year",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(S2_API_URL, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        logger.error(f"Semantic Scholar API returned {resp.status}")
                        return []
                    data = await resp.json()

            papers = []
            for item in data.get("data", []):
                ext_ids = item.get("externalIds", {}) or {}
                arxiv_id = ext_ids.get("ArXiv", "")
                if not arxiv_id:
                    continue

                authors = [a.get("name", "") for a in (item.get("authors", []) or [])]
                year = item.get("year", "")
                papers.append(Paper(
                    arxiv_id=arxiv_id,
                    title=item.get("title", ""),
                    authors=str(authors),
                    abstract=item.get("abstract", "") or "",
                    published_date=str(year) if year else "",
                    arxiv_url=f"https://arxiv.org/abs/{arxiv_id}",
                    pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
                    source="semantic_scholar",
                ))
            return papers

        except Exception as e:
            logger.error(f"Semantic Scholar search error: {e}")
            return []
