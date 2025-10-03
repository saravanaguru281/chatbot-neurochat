import logging
from rules import check_rules
from memory import check_vector_memory

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def get_response(user_input: str, vector_threshold: float = 0.7):
    """
    Core function to get response by checking rules first,
    then vector memory if no rule matches.

    Returns:
        dict with keys: 'response' and 'source' (either 'rule' or 'memory'),
        or None if no response found.
    """

    # 1. Check rules database
    rule_response = check_rules(user_input)
    if rule_response:
        logging.info("Response found from rules.")
        return {"response": rule_response["response"], "source": "rule"}

    # 2. Check vector memory database
    vector_response = check_vector_memory(user_input, threshold=vector_threshold)
    if vector_response:
        logging.info("Response found from vector memory.")
        return {"response": vector_response["response"], "source": "memory"}

    # 3. No matching response found
    logging.info("No matching response found in rules or vector memory.")
    return None

# -----
# Status: Completed
# Reminder: llm.py, handlers.py already given.
