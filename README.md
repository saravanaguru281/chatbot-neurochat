# chatbot-neurochat
Chatbot-NeuroChat 🧠 – A hybrid AI chatbot combining rule-based responses, semantic memory, and LLM fallback with a Gradio interface.
# 🧠 NeuroChat : Intelligent Chatbot - Rule-based + LLM Hybrid

Welcome to my NeuroChat  -custom-built intelligent chatbot, designed with a hybrid system that combines:
- ⚙️ Rule-based logic
- 🧠 Vector memory
- 🔮 LLM fallback (Notus-7B)

This project serves as both a **learning tool** and a **resume-worthy AI assistant**, built from scratch in Python, and deployed seamlessly on Hugging Face Spaces.

## 🚀 Live Demo

👉 Try it out here: [**Chatbot on Hugging Face**](https://huggingface.co/spaces/Hugg-Vij04/Chatbot)

---

## 🛠️ Features

- 💬 Natural text responses with fallback to LLM (Notus-7B via `llama-cpp-python`)
- 🧠 Vector memory: stores and retrieves previous conversations using cosine similarity
- 🧾 Rule-based engine: responds instantly to custom rules stored in SQLite
- 🧱 Embedding-based similarity matching via `sentence-transformers`
- 📦 Fully containerized and deployed on Hugging Face Spaces

---

## 🧩 Tech Stack

| Component             | Description                                         |
|----------------------|-----------------------------------------------------|
| Python               | Core language                                       |
| SQLite               | Lightweight DB for rules + memory                   |
| Sentence Transformers| For text embeddings (e.g., `all-MiniLM-L6-v2`)      |
| Notus-7B             | Lightweight LLM for intelligent fallback            |
| Gradio               | Interactive chat UI                                 |
| Hugging Face Spaces  | Deployment platform                                 |

---

## 🧠 How It Works

1. **Rule Check**
   - Checks user input against stored rules in `rules.db`.

2. **Vector Memory Check**
   - Embeds user input, compares against prior conversations using cosine similarity.

3. **LLM Fallback**
   - If no close match is found, response is generated using Notus-7B via `llama-cpp-python`.

4. **Learning & Storage**
   - New prompt-response pairs are stored for future retrieval.

---

## 📂 Project Structure

chatbot-deploy/
├── app.py               # Hugging Face entry point  
├── chatbot.py           # Main controller logic  
├── core.py              # Response handler  
├── db_init.py           # Initializes databases  
├── gradio_ui.py         # Chat interface via Gradio  
├── llm.py               # Notus-7B integration  
├── memory.py            # Vector memory logic  
├── config.py            # Global config  
├── utils.py             # Helper functions (e.g., cosine similarity)  
├── rules.db             # SQLite DB for rules  
├── vector_memory.db     # SQLite DB for vector memory  
├── chat_history.txt     # Logs all interactions  
├── requirements.txt     # All dependencies  
└── models/              # Contains LLM model files (Notus-7B)

---

## 💻 Running Locally

1. **Clone the Repo**
   ```bash
   git clone https://github.com/SimcoD-Vij/Chatbot-NeuroChat.git
      cd YourChatbot

Install Dependencies-    pip install -r requirements.txt


Run the App-     python app.py

