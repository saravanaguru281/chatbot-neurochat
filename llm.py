import logging
from huggingface_hub import hf_hub_download

try:
    from llama_cpp import Llama
except ImportError:
    logging.error("llama_cpp not installed. Install with `pip install llama-cpp-python`.")
    raise

# 🔁 Download model from Hugging Face Hub
MODEL_PATH = hf_hub_download(
    repo_id="Hugg-Vij04/HuggVij04notus7bv1Q40",
    filename="notus-7b-v1.Q4_0.gguf"
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# 📦 Load model once
try:
    logging.info(f"Loading LLM model from {MODEL_PATH} ...")
    llama_model = Llama(model_path=str(MODEL_PATH))
    logging.info("Loaded Notus-7B model successfully")
except Exception as e:
    logging.error(f"Failed to load LLM model: {e}")
    llama_model = None

def llm_generate_response(prompt: str, max_tokens: int = 256) -> str:
    if llama_model is None:
        logging.error("LLM model is not loaded, cannot generate response.")
        return None

    full_prompt = f"You are a helpful assistant. Respond clearly.\nUser: {prompt}\nBot:"
    
    try:
        response = llama_model(full_prompt, max_tokens=max_tokens, stop=["\n"], echo=False)
        text = response.get('choices', [{}])[0].get('text', '').strip()
        return text if text else None
    except Exception as e:
        logging.error(f"Error generating response from LLM: {e}")
        return None
