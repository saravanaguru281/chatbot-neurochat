import logging
from pathlib import Path

# === Paths ===
BASE_DIR = Path(__file__).parent.resolve()

# Database file locations
RULES_DB_PATH = BASE_DIR / "rules.db"
VECTOR_MEMORY_DB_PATH = BASE_DIR / "vector_memory.db"

# Your LLM model file path
MODEL_PATH = BASE_DIR / "models" / "notus-7b-v1.Q4_0.gguf"

# === Model & Embedding Config ===
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'  # SentenceTransformer model for vector memory
VECTOR_DIM = 384  # Make sure this matches the output dimension of the embedding model

# Similarity threshold for vector memory matching (between 0 and 1)
SIMILARITY_THRESHOLD = 0.7

# === Logging Configuration ===
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

# === Other settings ===
# Add more config options here if needed later

# -----
# Status: Completed
# Reminder: core.py, llm.py, handlers.py, memory.py, rules.py, utils.py, main.py already given.
