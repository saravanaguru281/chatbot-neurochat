# rules.py

import sqlite3
import logging
from config import RULES_DB_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def create_or_fix_rules_table():
    """Create 'rules' table if missing, ensure 'input' column exists."""
    try:
        conn = sqlite3.connect(RULES_DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT NOT NULL,
            response TEXT NOT NULL,
            tags TEXT
        )
        ''')
        conn.commit()
        logging.info("✅ 'rules' table created or verified successfully.")

        # Check if 'input' column exists; add if missing (rare case)
        cursor.execute("PRAGMA table_info(rules)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'input' not in columns:
            cursor.execute("ALTER TABLE rules ADD COLUMN input TEXT")
            conn.commit()
            logging.info("Added missing 'input' column to 'rules' table.")

    except Exception as e:
        logging.error(f"Error creating or fixing 'rules' table: {e}")
    finally:
        conn.close()

def check_rules(user_input: str):
    """Return the response from rules DB if exact input matches."""
    try:
        with sqlite3.connect(RULES_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT response FROM rules WHERE input = ?", (user_input,))
            result = cursor.fetchone()
            if result:
                logging.info(f"Rule matched for input: '{user_input}'")
                return {"response": result[0]}
    except Exception as e:
        logging.error(f"Error querying rules DB: {e}")
    return None

def save_rule(input_text: str, response_text: str, tags: str = None):
    """Insert a new rule into the rules table."""
    try:
        with sqlite3.connect(RULES_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO rules (input, response, tags) VALUES (?, ?, ?)",
                (input_text, response_text, tags)
            )
            conn.commit()
        logging.info(f"Saved new rule: '{input_text}' -> '{response_text}'")
    except Exception as e:
        logging.error(f"Error saving rule: {e}")

# Ensure the rules table is ready on import
create_or_fix_rules_table()
