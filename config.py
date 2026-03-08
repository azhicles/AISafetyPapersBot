import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_RPM = 30        # requests per minute
GROQ_RPD = 1000       # requests per day
GROQ_TPM = 12000      # tokens per minute

# Database
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "bot.db")

# Paper delivery defaults
DEFAULT_SEND_HOUR = 19  # 7 PM
DEFAULT_SEND_MINUTE = 0
DEFAULT_TIMEZONE = "Asia/Singapore"

# Novel paper discovery ratio (when collection has unsent papers)
CLASSIC_RATIO = 0.8  # 80% from collection, 20% novel

# PDF text truncation for LLM context
MAX_PAPER_TEXT_CHARS = 8000

# LLM summary max tokens
SUMMARY_MAX_TOKENS = 1500
CHAT_MAX_TOKENS = 1000

# Conversation history limit (messages kept per chat)
MAX_CONVERSATION_HISTORY = 20

# ArXiv search topics for novel paper discovery
SAFETY_TOPICS = [
    "AI alignment",
    "AI safety",
    "reinforcement learning from human feedback",
    "RLHF",
    "scalable oversight",
    "interpretability neural networks",
    "mechanistic interpretability",
    "AI existential risk",
    "value alignment AI",
    "reward hacking",
    "goal misgeneralization",
    "AI governance",
    "Constitutional AI",
    "debate AI safety",
    "iterated amplification",
    "corrigibility AI",
    "mesa-optimization",
    "inner alignment",
    "outer alignment",
    "deceptive alignment",
    "AI risk",
    "robustness machine learning",
    "adversarial robustness",
    "cooperative AI",
    "multi-agent safety",
    "AI transparency",
    "explainable AI safety",
    "red teaming language models",
    "jailbreak language models",
    "AI ethics research",
]
