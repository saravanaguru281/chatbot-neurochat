
# memory.py

import sqlite3
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
from config import VECTOR_MEMORY_DB_PATH, EMBEDDING_MODEL_NAME, SIMILARITY_THRESHOLD
from utils import cosine_similarity

# Initialize embedding model once (heavy load, don’t do this repeatedly)
try:
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    logging.info(f"Loaded embedding model '{EMBEDDING_MODEL_NAME}' successfully.")
except Exception as e:
    logging.error(f"Failed to load embedding model '{EMBEDDING_MODEL_NAME}': {e}")
    model = None

def ensure_table():
    """Ensure the vector memory table exists in the DB."""
    with sqlite3.connect(VECTOR_MEMORY_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT UNIQUE,
            response TEXT,
            vector BLOB
        )
        ''')
        conn.commit()
    logging.debug(f"Ensured vector memory table at {VECTOR_MEMORY_DB_PATH}")

def embed(text: str) -> np.ndarray:
    """Convert input text to embedding vector (float32)."""
    if model is None:
        raise RuntimeError("Embedding model not loaded.")
    vec = model.encode(text)
    return vec.astype(np.float32)

def vector_to_blob(vector: np.ndarray) -> bytes:
    """Serialize numpy vector to bytes for SQLite BLOB storage."""
    return vector.tobytes()

def blob_to_vector(blob: bytes) -> np.ndarray:
    """Deserialize bytes back to numpy vector."""
    return np.frombuffer(blob, dtype=np.float32)

def check_vector_memory(user_input: str, threshold: float = SIMILARITY_THRESHOLD):
    """
    Check vector memory for best match above similarity threshold.
    Returns dict with 'input' and 'response' or None.
    """
    if model is None:
        logging.error("Embedding model not available, skipping vector memory check.")
        return None

    try:
        vec = embed(user_input)
    except Exception as e:
        logging.error(f"Error generating embedding for input '{user_input}': {e}")
        return None

    best_match = None
    best_score = -1

    try:
        with sqlite3.connect(VECTOR_MEMORY_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT input, response, vector FROM memory")
            rows = cursor.fetchall()

        for stored_input, stored_response, vector_blob in rows:
            stored_vec = blob_to_vector(vector_blob)
            sim = cosine_similarity(vec, stored_vec)
            logging.debug(f"Similarity between input and '{stored_input}': {sim:.4f}")
            if sim > best_score:
                best_score = sim
                best_match = {"input": stored_input, "response": stored_response}

        if best_score >= threshold:
            logging.info(f"Vector memory matched '{best_match['input']}' with similarity {best_score:.3f}")
            return best_match
        else:
            logging.info(f"No vector memory match above threshold ({threshold}). Best similarity: {best_score:.3f}")
            return None

    except Exception as e:
        logging.error(f"Error during vector memory lookup: {e}")
        return None

def save_to_memory(user_input: str, response: str):
    """
    Save user input, response, and embedding vector to memory.
    Ignores if input already exists.
    """
    if model is None:
        logging.error("Embedding model not available, skipping save to vector memory.")
        return

    try:
        vec = embed(user_input)
        blob = vector_to_blob(vec)
        with sqlite3.connect(VECTOR_MEMORY_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO memory (input, response, vector) VALUES (?, ?, ?)",
                (user_input, response, blob)
            )
            conn.commit()
        logging.info(f"Saved new input to vector memory: '{user_input}'")
    except Exception as e:
        logging.error(f"Failed to save to vector memory: {e}")

# Ensure table exists on import
ensure_table()

