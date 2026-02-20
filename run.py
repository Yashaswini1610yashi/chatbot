import os

def main():
    print("🚀 Starting Universal AI Chatbot...")
    
    # Simple check for the model
    print("Launching Web Chat UI...")
    try:
        from app import demo
        demo.launch(share=False) 
    except Exception as e:
        print(f"Failed to launch app: {e}")

if __name__ == "__main__":
    main()
