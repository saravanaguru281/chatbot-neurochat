import gradio as gr
import time
from core import get_response
from handlers import handle_input
from db_init import initialize_all_databases

# 🛠 Initialize DBs
initialize_all_databases()

# 💬 Message handling
def chatbot_reply(user_message, chat_history):
    chat_history = chat_history or []
    response_data = get_response(user_message)

    if response_data:
        chat_history.append(("user", user_message, time.strftime("%H:%M")))
        chat_history.append(("bot", response_data["response"], time.strftime("%H:%M")))
    else:
        bot_response = handle_input(user_message)
        chat_history.append(("user", user_message, time.strftime("%H:%M")))
        chat_history.append(("bot", bot_response, time.strftime("%H:%M")))
    
    return "", chat_history, render_chat_html(chat_history)

# 🖼️ HTML Renderer for Chat UI
def render_chat_html(chat_history):
    if not chat_history:
        return "<div style='text-align:center;color:#999;margin-top:50px;'>No conversation yet.</div>"
    
    html = "<div id='chat-box'>"
    for sender, message, timestamp in chat_history:
        if sender == "user":
            html += f"""
            <div class='chat-row user'>
                <span class='sender'>You</span>
                <div class='bubble user-bubble'>{message}</div>
                <div class='time'>{timestamp}</div>
            </div>"""
        else:
            html += f"""
            <div class='chat-row bot'>
                <span class='sender'>Chatbot</span>
                <div class='bubble bot-bubble'>{message}</div>
                <div class='time'>{timestamp}</div>
            </div>"""
    html += "</div>"
    
    return html

# 🎨 Stylish CSS (Fixed User Message Bubble & Wrapping)
custom_css = """
body {
    background-color: #0e0e11;
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
    color: white;
}

#chat-box {
    padding: 16px;
    overflow-y: auto;
    height: 80vh;
    border-radius: 10px;
    background-color: #0e0e11;
    display: flex;
    flex-direction: column;
    width: 95%;
    max-width: 1100px;
    margin: auto;
}

/* Ensure messages align properly */
.chat-row {
    display: flex;
    flex-direction: column;
    max-width: fit-content;
    margin: 10px;
    padding: 0;
}

.chat-row.user {
    align-self: flex-end;
    text-align: right;
}

.chat-row.bot {
    align-self: flex-start;
    text-align: left;
}

.sender {
    font-weight: bold;
    font-size: 0.9em;
    color: #ddd;
    margin-bottom: 3px;
}

/* User message bubble */
.user-bubble {
    background-color: #6a5acd;
    color: white;
    border-radius: 18px 18px 0px 18px;
    padding: 12px 16px;
    font-size: 1.2em;
    line-height: 1.4;
    display: inline-block;
    max-width: 95%;
    word-wrap: break-word;
    white-space: normal;
    overflow-wrap: break-word;
    min-width: 80px;
    box-shadow: 0px 1px 4px rgba(0,0,0,0.2);
}

/* Bot message bubble */
.bot-bubble {
    background-color: white;
    color: black !important; /* Force black text */
    border: 1px solid #ccc;
    border-radius: 18px 18px 18px 0px;
    padding: 12px 16px;
    font-size: 1.2em;
    line-height: 1.4;
    display: inline-block;
    max-width: 95%;
    word-wrap: break-word;
    white-space: normal;
    overflow-wrap: break-word;
    min-width: 80px;
    box-shadow: 0px 1px 4px rgba(0,0,0,0.2);
}



.time {
    font-size: 0.7em;
    color: #aaa;
    margin-top: 3px;
}

/* Align input box properly */
#chat-input-section {
    display: flex;
    justify-content: center;
    align-items: center;
    max-width: 1000px;
    margin: 0 auto;
    padding: 12px;
    background-color: #0e0e11;
    position: sticky;
    bottom: 0;
    z-index: 10;
}

/* Dynamic height for text input */
#user-input {
    flex: 1;
    background-color: #1e1e22;
    color: white;
    border: 1px solid #555;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 16px;
    margin-right: 8px;
    min-height: 50px;
    max-height: 150px;
    width: 95%;
    overflow-y: auto;
}

/* Square send button */
#send-btn {
    width: 40px;
    height: 40px;
    background-color: #444;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s ease;
}

#send-btn:hover {
    background-color: #666;
}

/* Hide Gradio footer */
footer, .svelte-13f3c3s {
    display: none !important;
}

/* Mobile responsiveness */
@media screen and (max-width: 600px) {
    #chat-box {
        width: 95%;
        height: 75vh;
    }
    .bubble {
        font-size: 1em;
    }
    #user-input {
        width: 90%;
        min-height: 45px;
        max-height: 120px;
    }
}
"""

# 🧠 UI Assembly
with gr.Blocks(css=custom_css) as demo:
    chat_history = gr.State([])

    with gr.Column(elem_id="welcome-screen") as welcome_screen:
        gr.HTML("""
        <div style='text-align:center; margin-top: 150px;'>
            <h2>Welcome to Vijaypargavan’s Chatbot</h2>
            <p>How may I help you? Let's chat!</p>
        </div>
        """)
        start_btn = gr.Button("Start Chat")

    with gr.Column(visible=False) as chat_container:
        chat_html = gr.HTML("<div id='chat-box'></div>")

        with gr.Row(elem_id="chat-input-section"):
            user_input = gr.Textbox(
                placeholder="Type your message...",
                show_label=False,
                elem_id="user-input",
                scale=8
            )
            send_btn = gr.Button("➤", elem_id="send-btn", scale=1)

    # View switcher
    def switch_to_chat():
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True), []

    start_btn.click(switch_to_chat, [], [welcome_screen, chat_container, user_input, chat_history])
    send_btn.click(chatbot_reply, [user_input, chat_history], [user_input, chat_history, chat_html])
    user_input.submit(chatbot_reply, [user_input, chat_history], [user_input, chat_history, chat_html])

demo.launch()
