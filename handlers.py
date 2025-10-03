import logging
from core import get_response
from llm import llm_generate_response
from memory import save_to_memory

def handle_input(user_input: str) -> str:
    """
    Given user input, attempt to generate the most appropriate response:
    1. Rules
    2. Vector Memory
    3. LLM fallback
    Returns the bot's response.
    """
    # 1 & 2. Use core to get rules or vector memory response
    core_result = get_response(user_input)
    if core_result:
        logging.debug(f"→ Matched using {core_result['source']}.")
        return core_result['response']

    # 3. LLM fallback
    logging.debug("→ Falling back to LLM generation.")
    llm_response = llm_generate_response(user_input)
    if llm_response:
        # Save this conversation to memory for future matching
        save_to_memory(user_input, llm_response)
        return llm_response
    if llm_response and len(llm_response.strip()) > 3:
        save_to_memory(user_input, llm_response)
    else:
        logging.warning("LLM response too short or empty — not saving to memory.")
    if llm_response and len(llm_response.strip()) > 10 and '?' not in llm_response.strip():
        save_to_memory(user_input, llm_response)
    else:
        logging.warning(f"LLM response discarded: '{llm_response}'")

    # 4. Total failure (should rarely happen)
    logging.warning("→ No match from rules, memory, or LLM.")
    return "Sorry, I don't know how to respond. Can you teach me something new?"

# -----
# Status: Completed
# Reminder: llm.py, core.py already given.
