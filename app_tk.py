import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import ollama
import threading
import os
import time
from vector_db import search_docs, index_single_doc
from memory import store_memory, get_memory
import voice

# Configuration
MODEL_NAME = "llama3.2"
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AIChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Assistant - Desktop")
        self.geometry("900x700")

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Chat display
        self.chat_display = ctk.CTkTextbox(self, state="disabled", wrap="word", font=("Inter", 14))
        self.chat_display.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        # Input area frame
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Ask me something...", height=50, font=("Inter", 14))
        self.user_input.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.user_input.bind("<Return>", lambda e: self.send_message())

        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=1, sticky="e")

        self.voice_btn = ctk.CTkButton(self.buttons_frame, text="🎤", width=40, height=40, font=("Inter", 18), command=self.start_voice)
        self.voice_btn.grid(row=0, column=0, padx=5)

        self.upload_btn = ctk.CTkButton(self.buttons_frame, text="📎", width=40, height=40, font=("Inter", 18), command=self.upload_file)
        self.upload_btn.grid(row=0, column=1, padx=5)

        self.send_btn = ctk.CTkButton(self.buttons_frame, text="Send", width=80, height=40, font=("Inter", 14, "bold"), command=self.send_message)
        self.send_btn.grid(row=0, column=2, padx=5)

        self.append_chat("System", "Welcome! I am your AI Assistant. You can chat with me, upload PDFs for knowledge, or use voice command.")

    def append_chat(self, speaker, text):
        self.chat_display.configure(state="normal")
        tag = f"\n[{speaker}] {time.strftime('%H:%M')}\n"
        self.chat_display.insert("end", tag, "bold")
        self.chat_display.insert("end", f"{text}\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def send_message(self):
        query = self.user_input.get()
        if not query.strip():
            return
        
        self.user_input.delete(0, "end")
        self.append_chat("You", query)
        
        # Run AI response in a thread to keep UI responsive
        threading.Thread(target=self.get_ai_response, args=(query,), daemon=True).start()

    def get_ai_response(self, query):
        try:
            # 1. Context & Memory
            memory_context = get_memory()
            rag_context = search_docs(query)

            system_prompt = f"""
            You are a professional AI Assistant.
            {memory_context if memory_context else ""}
            {f"Relevant Context from Documents: {rag_context}" if rag_context else ""}
            """

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]

            response = ollama.chat(model=MODEL_NAME, messages=messages)
            answer = response["message"]["content"]

            # 2. Update UI (must use root.after for thread safety if using standard tk, but ctk handles it mostly)
            self.after(0, lambda: self.append_chat("Assistant", answer))
            
            # 3. Store Memory
            store_memory(query, answer)
        except Exception as e:
            self.after(0, lambda: self.append_chat("System", f"Error: {e}"))

    def start_voice(self):
        self.append_chat("System", "Listening...")
        threading.Thread(target=self.voice_task, daemon=True).start()

    def voice_task(self):
        text = voice.listen()
        if text:
            self.after(0, lambda: self.user_input.insert(0, text))
            self.after(0, lambda: self.append_chat("System", f"Recognized: {text}"))
        else:
            self.after(0, lambda: self.append_chat("System", "Could not understand audio."))

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Documents", "*.pdf"), ("Images", "*.jpg;*.jpeg;*.png")])
        if file_path:
            if file_path.lower().endswith(".pdf"):
                self.append_chat("System", f"Indexing PDF: {os.path.basename(file_path)}...")
                threading.Thread(target=self.index_pdf_task, args=(file_path,), daemon=True).start()
            else:
                self.append_chat("System", f"Image uploaded: {os.path.basename(file_path)} (Note: Vision not yet fully integrated)")

    def index_pdf_task(self, file_path):
        if index_single_doc(file_path):
            self.after(0, lambda: self.append_chat("System", f"Successfully indexed {os.path.basename(file_path)}."))
        else:
            self.after(0, lambda: self.append_chat("System", f"Failed to index {os.path.basename(file_path)}."))

if __name__ == "__main__":
    app = AIChatApp()
    app.mainloop()
