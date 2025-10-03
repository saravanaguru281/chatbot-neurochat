import logging
from rules import create_or_fix_rules_table
from memory import ensure_table
from config import RULES_DB_PATH, VECTOR_MEMORY_DB_PATH

def initialize_all_databases():
    """
    Initialize or fix all required databases before starting the chatbot.
    This ensures tables exist and are ready for use.
    """
    logging.info("Initializing all databases...")

    try:
        create_or_fix_rules_table()
        ensure_table()
        logging.info("All databases initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize databases: {e}")
        raise
