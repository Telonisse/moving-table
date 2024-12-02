import os
from dotenv import load_dotenv
from openai import OpenAI
import signal
import sys

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_ai_response(prompt):
    """Get AI response for a given prompt."""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    
    ai_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content.strip()
            print(f"RAW API RESPONSE CHUNK: '{content}'")  # Debugging output
            ai_response += content + " "
    
    return ai_response.strip()

def signal_handler(signum, frame):
    """Handler for SIGINT signal (Ctrl+C)"""
    print("\nChatbot: Goodbye! It was nice chatting with you.")
    sys.exit(0)

def chatbot():
    """Main chatbot functionality."""
    print("Welcome to the OpenAI Chatbot!")
    print("Type 'quit' to exit.")
    print("Available commands:")
    print("- info: Get information about the chatbot")
    print("- joke: Tell me a joke")
    print("- story: Start a short story")
    print("- help: Show available commands")

    # Set up signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            user_input = input("\nUser: ").lower()

            if user_input == 'quit':
                break
            
            elif user_input == 'info':
                print("\nInfo:")
                print("This chatbot uses OpenAI's GPT-4o-mini model to respond to user inputs.")
                print("It can tell jokes, start stories, and provide general information.")

            elif user_input == 'joke':
                ai_response = get_ai_response("Tell me a joke")
                print(f"\nChatbot: {ai_response}")

            elif user_input == 'story':
                ai_response = get_ai_response("Start a short story about a robot who dreams of becoming an artist.")
                print(f"\nChatbot: {ai_response}")

            elif user_input == 'help':
                print("\nAvailable commands:")
                print("- info: Get information about the chatbot")
                print("- joke: Tell me a joke")
                print("- story: Start a short story")
                print("- help: Show available commands")

            else:
                ai_response = get_ai_response(user_input)
                
                if ai_response:
                    print(f"\nChatbot: {ai_response}")
                else:
                    print("\nChatbot: Sorry, I didn't understand that.")

        except KeyboardInterrupt:
            print("\nChatbot: Goodbye! It was nice chatting with you.")
            break

if __name__ == "__main__":
    try:
        chatbot()
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")