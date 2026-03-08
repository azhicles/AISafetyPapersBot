"""Singleton service container for lazy initialization."""

from services.groq_client import GroqClient
from services.arxiv_service import ArxivService
from services.semantic_scholar import SemanticScholarService
from services.summarizer import SummarizerService
from services.paper_fetcher import PaperFetcher
from services.paper_evaluator import PaperEvaluator
from services.chat_service import ChatService

_groq_client: GroqClient | None = None
_arxiv_service: ArxivService | None = None
_semantic_scholar: SemanticScholarService | None = None
_summarizer: SummarizerService | None = None
_paper_fetcher: PaperFetcher | None = None
_paper_evaluator: PaperEvaluator | None = None
_chat_service: ChatService | None = None


def get_groq_client() -> GroqClient:
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient()
    return _groq_client


def get_arxiv_service() -> ArxivService:
    global _arxiv_service
    if _arxiv_service is None:
        _arxiv_service = ArxivService()
    return _arxiv_service


def get_semantic_scholar() -> SemanticScholarService:
    global _semantic_scholar
    if _semantic_scholar is None:
        _semantic_scholar = SemanticScholarService()
    return _semantic_scholar


def get_summarizer() -> SummarizerService:
    global _summarizer
    if _summarizer is None:
        _summarizer = SummarizerService(get_groq_client())
    return _summarizer


def get_paper_fetcher() -> PaperFetcher:
    global _paper_fetcher
    if _paper_fetcher is None:
        _paper_fetcher = PaperFetcher(get_arxiv_service(), get_semantic_scholar())
    return _paper_fetcher


def get_paper_evaluator() -> PaperEvaluator:
    global _paper_evaluator
    if _paper_evaluator is None:
        _paper_evaluator = PaperEvaluator(get_groq_client())
    return _paper_evaluator


def get_chat_service() -> ChatService:
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService(get_groq_client())
    return _chat_service
