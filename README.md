# AI Safety Papers Bot

A Telegram bot that delivers a daily AI safety paper with an LLM-generated summary. Built with python-telegram-bot, Groq (Llama 3.3 70B), and SQLite.

## Features

- **Daily paper delivery** at a configurable time and timezone per chat
- **75 curated seed papers** spanning foundational to cutting-edge AI safety research (2016-2025)
- **LLM summaries** generated on-demand via Groq, with PDF text extraction
- **Novel discovery** via ArXiv and Semantic Scholar when your queue runs out
- **Conversational Q&A** -- ask follow-up questions about the current paper
- **Ratings and reviews** to track your reading
- **Group chat support** -- responds when @mentioned or replied to
- **Per-chat state** -- independent collections, queues, and settings

## Prerequisites

- Python 3.11+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Groq API Key (from [console.groq.com](https://console.groq.com))

## Installation

1. Clone the repository and enter the project directory.

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example env file and fill in your keys:
```bash
cp .env.example .env
```

Edit `.env`:
```
TELEGRAM_BOT_TOKEN=your-bot-token-here
GROQ_API_KEY=your-groq-key-here
GROQ_MODEL=llama-3.3-70b-versatile
```

## Running Locally

```bash
python main.py
```

The bot will:
- Create the SQLite database in `data/bot.db`
- Seed 75 curated AI safety papers
- Start polling for Telegram updates
- Schedule checks every 5 minutes for daily paper delivery

## Deploying to Fly.io

```bash
fly launch
fly secrets set TELEGRAM_BOT_TOKEN=... GROQ_API_KEY=...
fly deploy
```

Ensure `fly.toml` has no `[http_service]` section (this is a worker process, not a web server) and uses `[restart] policy = 'always'`. After deploying, set the machine to never auto-stop:

```bash
fly machine update <machine-id> --autostop=off --restart=always -y
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Register and seed your collection |
| `/stop` | Pause daily deliveries |
| `/resume` | Resume daily deliveries |
| `/help` | Show help message |
| `/next` | Get the next paper with summary |
| `/current` | Show the current paper |
| `/add <arxiv_id>` | Add a paper by ArXiv ID |
| `/remove <arxiv_id>` | Remove a paper from collection |
| `/collection` | View your paper collection |
| `/past` | View previously sent papers |
| `/rate <1-5>` | Rate the current paper |
| `/review <text>` | Write a review |
| `/search <query>` | Search ArXiv for papers |
| `/stats` | View collection statistics |
| `/settings time <HH:MM>` | Change daily send time |
| `/settings timezone <tz>` | Change timezone |

Send any free-form message to chat about the current paper.

## Configuration

Key settings in `config.py`:
- `DEFAULT_SEND_HOUR` / `DEFAULT_SEND_MINUTE`: Default daily delivery time (default: 19:00)
- `DEFAULT_TIMEZONE`: Default timezone (default: Asia/Singapore)
- `CLASSIC_RATIO`: Probability of picking from collection vs novel paper (default: 0.8)
- `MAX_PAPER_TEXT_CHARS`: PDF text truncation limit (default: 8000 chars)
- `GROQ_RPM/TPM`: Groq rate limits

## Architecture

- **Scheduler**: Repeating job every 5 minutes checks each chat's `send_hour`/`send_minute` in their timezone
- **80/20 rule**: 80% papers from collection queue, 20% novel discovery via ArXiv/Semantic Scholar
- **Queue exhaustion**: When all queued papers are sent, switches to 100% novel discovery
- **Lazy loading**: PDF text extracted and summaries generated on first use, then cached
- **Group chat**: Bot only responds to free-form messages when @mentioned or replied to
- **Per-chat state**: Each group/private chat has independent collection, queue, and ratings

## Groq Rate Limits

The bot respects Groq's free tier limits:
- 30 requests per minute (RPM)
- 12,000 tokens per minute (TPM)
- Rate limiting via `aiolimiter` with graceful fallback messages

## Data

- SQLite database stored in `data/bot.db` (gitignored)
- Persistent volume mounted at `/app/data` on Fly.io
- Paper full text and summaries are cached after first generation
- Conversation history is stored per-chat for contextual Q&A
