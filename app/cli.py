from app.client import ask_jarvis

def run():
    print("JARVIS — Personal AI Assistant (V1)")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue
        response = ask_jarvis(user_input)
        print(f"\nJarvis: {response}\n")