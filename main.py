
import logging
from core import get_response
from handlers import handle_input
from db_init import initialize_all_databases

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

def main_loop():
    logging.info("Chatbot started. Waiting for input...")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            logging.info("Chatbot session ended by user.")
            print("\nGoodbye!")
            break

        if not user_input:
            continue  # Ignore empty inputs, wait for real input

        response_data = get_response(user_input)
        if response_data:
            print(f"Bot: {response_data['response']}")
            continue

        # If no match, fall back to handler (which does vector memory + LLM)
        bot_response = handle_input(user_input)
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    setup_logging()
    initialize_all_databases()  # Setup or fix all DBs before starting
    main_loop()
