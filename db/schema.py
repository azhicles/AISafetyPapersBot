import aiosqlite
import os

from config import DB_PATH


async def init_db() -> None:
    """Create all tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER PRIMARY KEY,
                chat_type TEXT NOT NULL DEFAULT 'private',
                chat_title TEXT NOT NULL DEFAULT '',
                is_active INTEGER NOT NULL DEFAULT 1,
                send_hour INTEGER NOT NULL DEFAULT 19,
                send_minute INTEGER NOT NULL DEFAULT 0,
                last_scheduled_at TEXT,
                timezone TEXT NOT NULL DEFAULT 'Asia/Singapore',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arxiv_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                authors TEXT NOT NULL DEFAULT '[]',
                abstract TEXT NOT NULL DEFAULT '',
                published_date TEXT NOT NULL DEFAULT '',
                arxiv_url TEXT NOT NULL DEFAULT '',
                pdf_url TEXT NOT NULL DEFAULT '',
                full_text TEXT,
                summary TEXT,
                is_classic INTEGER NOT NULL DEFAULT 0,
                source TEXT NOT NULL DEFAULT 'seed',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS chat_papers (
                chat_id INTEGER NOT NULL,
                paper_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'queued',
                queue_position INTEGER NOT NULL DEFAULT 0,
                added_by TEXT NOT NULL DEFAULT 'system',
                sent_at TEXT,
                PRIMARY KEY (chat_id, paper_id),
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                chat_id INTEGER NOT NULL,
                paper_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                PRIMARY KEY (chat_id, paper_id, user_id),
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                paper_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                review_text TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS chat_context (
                chat_id INTEGER PRIMARY KEY,
                current_paper_id INTEGER,
                conversation_history TEXT NOT NULL DEFAULT '[]',
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
                FOREIGN KEY (current_paper_id) REFERENCES papers(id)
            )
        """)

        # Migrate: add columns if missing (older DBs)
        cols = await db.execute_fetchall("PRAGMA table_info(chats)")
        col_names = {c[1] for c in cols}
        if "send_minute" not in col_names:
            await db.execute("ALTER TABLE chats ADD COLUMN send_minute INTEGER NOT NULL DEFAULT 0")
        if "last_scheduled_at" not in col_names:
            await db.execute("ALTER TABLE chats ADD COLUMN last_scheduled_at TEXT")

        await db.commit()
