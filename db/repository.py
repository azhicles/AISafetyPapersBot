import json
import aiosqlite
from datetime import datetime

from config import DB_PATH
from db.models import Chat, Paper, ChatPaper, Rating, Review, ChatContext


def _connect():
    """Return an aiosqlite connection context manager."""
    return aiosqlite.connect(DB_PATH)


# ── Chat CRUD ──────────────────────────────────────────────

async def register_chat(chat_id: int, chat_type: str = "private", chat_title: str = "") -> Chat:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT OR IGNORE INTO chats (chat_id, chat_type, chat_title) VALUES (?, ?, ?)",
            (chat_id, chat_type, chat_title),
        )
        await db.commit()
        row = await db.execute_fetchall(
            "SELECT * FROM chats WHERE chat_id = ?", (chat_id,)
        )
        r = row[0]
        return Chat(
            chat_id=r["chat_id"], chat_type=r["chat_type"],
            chat_title=r["chat_title"], is_active=bool(r["is_active"]),
            send_hour=r["send_hour"], send_minute=r["send_minute"],
            timezone=r["timezone"],
            created_at=r["created_at"],
        )


async def get_chat(chat_id: int) -> Chat | None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT * FROM chats WHERE chat_id = ?", (chat_id,)
        )
        if not rows:
            return None
        r = rows[0]
        return Chat(
            chat_id=r["chat_id"], chat_type=r["chat_type"],
            chat_title=r["chat_title"], is_active=bool(r["is_active"]),
            send_hour=r["send_hour"], send_minute=r["send_minute"],
            timezone=r["timezone"],
            created_at=r["created_at"],
        )


async def set_chat_active(chat_id: int, is_active: bool) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "UPDATE chats SET is_active = ? WHERE chat_id = ?",
            (int(is_active), chat_id),
        )
        await db.commit()


async def update_chat_settings(
    chat_id: int,
    send_hour: int | None = None,
    send_minute: int | None = None,
    timezone: str | None = None,
) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        if send_hour is not None:
            await db.execute(
                "UPDATE chats SET send_hour = ? WHERE chat_id = ?",
                (send_hour, chat_id),
            )
        if send_minute is not None:
            await db.execute(
                "UPDATE chats SET send_minute = ? WHERE chat_id = ?",
                (send_minute, chat_id),
            )
        if timezone is not None:
            await db.execute(
                "UPDATE chats SET timezone = ? WHERE chat_id = ?",
                (timezone, chat_id),
            )
        await db.commit()


async def get_active_chats() -> list[Chat]:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT * FROM chats WHERE is_active = 1"
        )
        return [
            Chat(
                chat_id=r["chat_id"], chat_type=r["chat_type"],
                chat_title=r["chat_title"], is_active=True,
                send_hour=r["send_hour"], send_minute=r["send_minute"],
            timezone=r["timezone"],
                created_at=r["created_at"],
            )
            for r in rows
        ]


# ── Paper CRUD ─────────────────────────────────────────────

async def upsert_paper(paper: Paper) -> int:
    """Insert or update a paper, returns the paper id."""
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute("""
            INSERT INTO papers (arxiv_id, title, authors, abstract, published_date,
                                arxiv_url, pdf_url, full_text, summary, is_classic, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(arxiv_id) DO UPDATE SET
                title=excluded.title, authors=excluded.authors,
                abstract=excluded.abstract, published_date=excluded.published_date,
                arxiv_url=excluded.arxiv_url, pdf_url=excluded.pdf_url,
                is_classic=excluded.is_classic, source=excluded.source
        """, (
            paper.arxiv_id, paper.title, paper.authors, paper.abstract,
            paper.published_date, paper.arxiv_url, paper.pdf_url,
            paper.full_text, paper.summary, int(paper.is_classic), paper.source,
        ))
        await db.commit()
        rows = await db.execute_fetchall(
            "SELECT id FROM papers WHERE arxiv_id = ?", (paper.arxiv_id,)
        )
        return rows[0]["id"]


async def get_paper(paper_id: int) -> Paper | None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT * FROM papers WHERE id = ?", (paper_id,)
        )
        if not rows:
            return None
        return _row_to_paper(rows[0])


async def get_paper_by_arxiv_id(arxiv_id: str) -> Paper | None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT * FROM papers WHERE arxiv_id = ?", (arxiv_id,)
        )
        if not rows:
            return None
        return _row_to_paper(rows[0])


async def update_paper_text(paper_id: int, full_text: str) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "UPDATE papers SET full_text = ? WHERE id = ?",
            (full_text, paper_id),
        )
        await db.commit()


async def update_paper_summary(paper_id: int, summary: str) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "UPDATE papers SET summary = ? WHERE id = ?",
            (summary, paper_id),
        )
        await db.commit()


async def get_all_paper_arxiv_ids() -> set[str]:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("SELECT arxiv_id FROM papers")
        return {r["arxiv_id"] for r in rows}


async def search_papers(query: str, limit: int = 10) -> list[Paper]:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT * FROM papers WHERE title LIKE ? OR abstract LIKE ? LIMIT ?",
            (f"%{query}%", f"%{query}%", limit),
        )
        return [_row_to_paper(r) for r in rows]


def _row_to_paper(r) -> Paper:
    return Paper(
        id=r["id"], arxiv_id=r["arxiv_id"], title=r["title"],
        authors=r["authors"], abstract=r["abstract"],
        published_date=r["published_date"], arxiv_url=r["arxiv_url"],
        pdf_url=r["pdf_url"], full_text=r["full_text"],
        summary=r["summary"], is_classic=bool(r["is_classic"]),
        source=r["source"], created_at=r["created_at"],
    )


# ── ChatPaper CRUD ─────────────────────────────────────────

async def add_paper_to_chat(chat_id: int, paper_id: int, added_by: str = "system") -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT MAX(queue_position) as max_pos FROM chat_papers WHERE chat_id = ?",
            (chat_id,),
        )
        max_pos = rows[0]["max_pos"] or 0
        await db.execute(
            "INSERT OR IGNORE INTO chat_papers (chat_id, paper_id, queue_position, added_by) VALUES (?, ?, ?, ?)",
            (chat_id, paper_id, max_pos + 1, added_by),
        )
        await db.commit()


async def remove_paper_from_chat(chat_id: int, paper_id: int) -> bool:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "DELETE FROM chat_papers WHERE chat_id = ? AND paper_id = ?",
            (chat_id, paper_id),
        )
        await db.commit()
        return cursor.rowcount > 0


async def get_next_queued_paper(chat_id: int) -> Paper | None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("""
            SELECT p.* FROM papers p
            JOIN chat_papers cp ON p.id = cp.paper_id
            WHERE cp.chat_id = ? AND cp.status = 'queued'
            ORDER BY RANDOM()
            LIMIT 1
        """, (chat_id,))
        if not rows:
            return None
        return _row_to_paper(rows[0])


async def mark_paper_sent(chat_id: int, paper_id: int) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "UPDATE chat_papers SET status = 'sent', sent_at = datetime('now') WHERE chat_id = ? AND paper_id = ?",
            (chat_id, paper_id),
        )
        await db.commit()


async def get_chat_collection(chat_id: int) -> list[tuple[Paper, str]]:
    """Returns list of (Paper, status) for a chat's collection."""
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("""
            SELECT p.*, cp.status FROM papers p
            JOIN chat_papers cp ON p.id = cp.paper_id
            WHERE cp.chat_id = ?
            ORDER BY cp.queue_position ASC
        """, (chat_id,))
        return [(_row_to_paper(r), r["status"]) for r in rows]


async def get_sent_papers(chat_id: int, limit: int = 20) -> list[Paper]:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("""
            SELECT p.* FROM papers p
            JOIN chat_papers cp ON p.id = cp.paper_id
            WHERE cp.chat_id = ? AND cp.status = 'sent'
            ORDER BY cp.sent_at DESC
            LIMIT ?
        """, (chat_id, limit))
        return [_row_to_paper(r) for r in rows]


async def get_queued_count(chat_id: int) -> int:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT COUNT(*) as cnt FROM chat_papers WHERE chat_id = ? AND status = 'queued'",
            (chat_id,),
        )
        return rows[0]["cnt"]


async def get_sent_count(chat_id: int) -> int:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT COUNT(*) as cnt FROM chat_papers WHERE chat_id = ? AND status = 'sent'",
            (chat_id,),
        )
        return rows[0]["cnt"]


async def get_chat_paper_ids(chat_id: int) -> set[int]:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT paper_id FROM chat_papers WHERE chat_id = ?", (chat_id,)
        )
        return {r["paper_id"] for r in rows}


async def get_all_known_arxiv_ids_for_chat(chat_id: int) -> set[str]:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("""
            SELECT p.arxiv_id FROM papers p
            JOIN chat_papers cp ON p.id = cp.paper_id
            WHERE cp.chat_id = ?
        """, (chat_id,))
        return {r["arxiv_id"] for r in rows}


async def return_last_sent_paper(chat_id: int) -> Paper | None:
    """Return the most recently sent paper back to the queue. Returns the paper or None."""
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("""
            SELECT cp.paper_id, cp.queue_position FROM chat_papers cp
            WHERE cp.chat_id = ? AND cp.status = 'sent'
            ORDER BY cp.sent_at DESC
            LIMIT 1
        """, (chat_id,))
        if not rows:
            return None
        paper_id = rows[0]["paper_id"]
        # Find the minimum queue position so we insert at the front
        min_rows = await db.execute_fetchall(
            "SELECT MIN(queue_position) as min_pos FROM chat_papers WHERE chat_id = ? AND status = 'queued'",
            (chat_id,),
        )
        min_pos = min_rows[0]["min_pos"]
        new_pos = (min_pos - 1) if min_pos is not None else 1
        await db.execute(
            "UPDATE chat_papers SET status = 'queued', sent_at = NULL, queue_position = ? WHERE chat_id = ? AND paper_id = ?",
            (new_pos, chat_id, paper_id),
        )
        await db.commit()
        paper_rows = await db.execute_fetchall("SELECT * FROM papers WHERE id = ?", (paper_id,))
        if not paper_rows:
            return None
        return _row_to_paper(paper_rows[0])


async def was_scheduled_recently(chat_id: int, hours: int = 20) -> bool:
    """Check if the scheduler already delivered to this chat recently."""
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT last_scheduled_at FROM chats WHERE chat_id = ?",
            (chat_id,),
        )
        if not rows or not rows[0]["last_scheduled_at"]:
            return False
        last = rows[0]["last_scheduled_at"]
        # Compare against threshold
        threshold = await db.execute_fetchall(
            "SELECT datetime('now', ?) as cutoff", (f"-{hours} hours",)
        )
        return last > threshold[0]["cutoff"]


async def mark_scheduled_delivery(chat_id: int) -> None:
    """Record that the scheduler just delivered to this chat."""
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "UPDATE chats SET last_scheduled_at = datetime('now') WHERE chat_id = ?",
            (chat_id,),
        )
        await db.commit()


# ── Seed papers to a chat ─────────────────────────────────

async def seed_papers_to_chat(chat_id: int) -> int:
    """Add all classic papers to a chat's queue. Returns count added."""
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT id FROM papers WHERE is_classic = 1 ORDER BY id"
        )
        count = 0
        for i, r in enumerate(rows):
            cursor = await db.execute(
                "INSERT OR IGNORE INTO chat_papers (chat_id, paper_id, queue_position, added_by) VALUES (?, ?, ?, ?)",
                (chat_id, r["id"], i + 1, "system"),
            )
            if cursor.rowcount > 0:
                count += 1
        await db.commit()
        return count


# ── Rating CRUD ────────────────────────────────────────────

async def set_rating(chat_id: int, paper_id: int, user_id: int, rating: int) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute("""
            INSERT INTO ratings (chat_id, paper_id, user_id, rating)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(chat_id, paper_id, user_id) DO UPDATE SET rating=excluded.rating
        """, (chat_id, paper_id, user_id, rating))
        await db.commit()


async def get_paper_avg_rating(chat_id: int, paper_id: int) -> tuple[float | None, int]:
    """Returns (avg_rating, count)."""
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT AVG(rating) as avg, COUNT(*) as cnt FROM ratings WHERE chat_id = ? AND paper_id = ?",
            (chat_id, paper_id),
        )
        r = rows[0]
        if r["cnt"] == 0:
            return None, 0
        return round(r["avg"], 1), r["cnt"]


# ── Review CRUD ────────────────────────────────────────────

async def add_review(chat_id: int, paper_id: int, user_id: int, review_text: str) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT INTO reviews (chat_id, paper_id, user_id, review_text) VALUES (?, ?, ?, ?)",
            (chat_id, paper_id, user_id, review_text),
        )
        await db.commit()


async def get_paper_reviews(chat_id: int, paper_id: int) -> list[Review]:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT * FROM reviews WHERE chat_id = ? AND paper_id = ? ORDER BY created_at DESC",
            (chat_id, paper_id),
        )
        return [
            Review(
                id=r["id"], chat_id=r["chat_id"], paper_id=r["paper_id"],
                user_id=r["user_id"], review_text=r["review_text"],
                created_at=r["created_at"],
            )
            for r in rows
        ]


# ── ChatContext CRUD ───────────────────────────────────────

async def get_chat_context(chat_id: int) -> ChatContext:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall(
            "SELECT * FROM chat_context WHERE chat_id = ?", (chat_id,)
        )
        if not rows:
            return ChatContext(chat_id=chat_id)
        r = rows[0]
        return ChatContext(
            chat_id=r["chat_id"],
            current_paper_id=r["current_paper_id"],
            conversation_history=r["conversation_history"],
        )


async def set_current_paper(chat_id: int, paper_id: int) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute("""
            INSERT INTO chat_context (chat_id, current_paper_id, conversation_history)
            VALUES (?, ?, '[]')
            ON CONFLICT(chat_id) DO UPDATE SET
                current_paper_id=excluded.current_paper_id,
                conversation_history='[]'
        """, (chat_id, paper_id))
        await db.commit()


async def update_conversation_history(chat_id: int, history: list[dict]) -> None:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "UPDATE chat_context SET conversation_history = ? WHERE chat_id = ?",
            (json.dumps(history), chat_id),
        )
        await db.commit()


# ── Stats ──────────────────────────────────────────────────

async def get_chat_stats(chat_id: int) -> dict:
    async with _connect() as db:
        db.row_factory = aiosqlite.Row
        total = await db.execute_fetchall(
            "SELECT COUNT(*) as cnt FROM chat_papers WHERE chat_id = ?", (chat_id,)
        )
        queued = await db.execute_fetchall(
            "SELECT COUNT(*) as cnt FROM chat_papers WHERE chat_id = ? AND status = 'queued'",
            (chat_id,),
        )
        sent = await db.execute_fetchall(
            "SELECT COUNT(*) as cnt FROM chat_papers WHERE chat_id = ? AND status = 'sent'",
            (chat_id,),
        )
        rated = await db.execute_fetchall(
            "SELECT COUNT(DISTINCT paper_id) as cnt FROM ratings WHERE chat_id = ?",
            (chat_id,),
        )
        avg_rating = await db.execute_fetchall(
            "SELECT AVG(rating) as avg FROM ratings WHERE chat_id = ?", (chat_id,)
        )
        reviewed = await db.execute_fetchall(
            "SELECT COUNT(DISTINCT paper_id) as cnt FROM reviews WHERE chat_id = ?",
            (chat_id,),
        )
        return {
            "total_papers": total[0]["cnt"],
            "queued": queued[0]["cnt"],
            "sent": sent[0]["cnt"],
            "rated": rated[0]["cnt"],
            "avg_rating": round(avg_rating[0]["avg"], 1) if avg_rating[0]["avg"] else None,
            "reviewed": reviewed[0]["cnt"],
        }
