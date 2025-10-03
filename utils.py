# utils.py

import logging
import re
import numpy as np

def clean_text(text: str) -> str:
    """
    Lowercases, strips, and removes extra spaces and punctuation for matching.
    """
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    return text

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    """
    if a.shape != b.shape:
        logging.warning(f"Vector dim mismatch: {a.shape} vs {b.shape}")
        return -1
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return -1
    return float(np.dot(a, b) / (norm_a * norm_b))

def truncate_response(response: str, max_tokens: int = 512) -> str:
    """
    Truncates the response to a max token length (approximate).
    """
    words = response.split()
    if len(words) > max_tokens:
        return ' '.join(words[:max_tokens]) + '...'
    return response

def log_section(title: str):
    """
    Logs a clean section break in the logs for readability.
    """
    logging.info(f"\n{'=' * 40}\n{title}\n{'=' * 40}")

