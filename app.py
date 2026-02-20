import gradio as gr
import ollama

# Configuration
MODEL_NAME = "llama3.2"

def chat(message, history):
    # Prepare messages for Ollama
    messages = []
    
    # Add history for continuity
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
        
    messages.append({"role": "user", "content": message})

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error: {e}. Make sure Ollama is running (`ollama run {MODEL_NAME}`)."

# Custom CSS for High-Contrast Black & White Aesthetics
css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Outfit:wght@700&display=swap');

:root {
    --bg-color: #ffffff;
    --text-primary: #000000;
    --border-color: #e5e7eb;
    --user-bubble: #000000;
    --user-text: #ffffff;
    --bot-bubble: #f3f4f6;
    --bot-text: #000000;
}

body, .gradio-container {
    background-color: var(--bg-color) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

#main-container {
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 2rem 15% !important;
    box-sizing: border-box !important;
}

#title-area {
    text-align: center;
    margin-bottom: 2rem;
}

#title-area h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 2.5rem;
    color: #000000;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

#chat-box {
    flex-grow: 1 !important;
    background: #ffffff !important;
    border: 2px solid #000000 !important;
    border-radius: 1rem !important;
    overflow: hidden !important;
}

.message.user {
    background: var(--user-bubble) !important;
    color: var(--user-text) !important;
    border-radius: 1rem 1rem 0.2rem 1rem !important;
    font-weight: 400 !important;
}

.message.bot {
    background: var(--bot-bubble) !important;
    color: var(--bot-text) !important;
    border-radius: 1rem 1rem 1rem 0.2rem !important;
    border: 1px solid #d1d5db !important;
}

#input-container {
    margin-top: 1.5rem;
    border: 2px solid #000000 !important;
    border-radius: 0.8rem !important;
    padding: 0.5rem !important;
    background: #ffffff !important;
}

footer {
    display: none !important;
}

/* Ensure letters are very sharp and visible */
* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
"""

with gr.Blocks(css=css, title="Universal AI assistant") as demo:
    with gr.Column(elem_id="main-container"):
        with gr.Column(elem_id="title-area"):
            gr.Markdown("# 🌌 Universal AI assistant")
            gr.Markdown("Answering everything about the universe with high-contrast clarity.")
        
        chatbot = gr.Chatbot(
            show_label=False,
            elem_id="chat-box",
            avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=AI")
        )
        
        with gr.Row(elem_id="input-container"):
            msg = gr.Textbox(
                show_label=False,
                placeholder="Type your message here...",
                container=False,
                scale=9
            )
            submit = gr.Button("Send", variant="primary", scale=1)

        def respond(message, chat_history):
            if not message.strip():
                return "", chat_history
            bot_message = chat(message, chat_history)
            chat_history.append((message, bot_message))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit.click(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(share=False)
