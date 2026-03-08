from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Chat:
    chat_id: int
    chat_type: str = "private"
    chat_title: str = ""
    is_active: bool = True
    send_hour: int = 19
    send_minute: int = 0
    timezone: str = "Asia/Singapore"
    created_at: str = ""


@dataclass
class Paper:
    id: int = 0
    arxiv_id: str = ""
    title: str = ""
    authors: str = "[]"  # JSON list
    abstract: str = ""
    published_date: str = ""
    arxiv_url: str = ""
    pdf_url: str = ""
    full_text: str | None = None
    summary: str | None = None
    is_classic: bool = False
    source: str = "seed"
    created_at: str = ""


@dataclass
class ChatPaper:
    chat_id: int = 0
    paper_id: int = 0
    status: str = "queued"  # queued, sent
    queue_position: int = 0
    added_by: str = "system"
    sent_at: str | None = None


@dataclass
class Rating:
    chat_id: int = 0
    paper_id: int = 0
    user_id: int = 0
    rating: int = 0
    created_at: str = ""


@dataclass
class Review:
    id: int = 0
    chat_id: int = 0
    paper_id: int = 0
    user_id: int = 0
    review_text: str = ""
    created_at: str = ""


@dataclass
class ChatContext:
    chat_id: int = 0
    current_paper_id: int | None = None
    conversation_history: str = "[]"  # JSON list
