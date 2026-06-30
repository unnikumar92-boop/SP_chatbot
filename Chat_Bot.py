import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key loaded: {api_key}")
client = Anthropic()

# System prompt that defines the patient
system_prompt = """You are a patient visiting a speech pathology clinic. 
You have been diagnosed with vocal cord tumors. 
You've had a hoarse voice for six weeks, are a smoker, and occasionally experience throat pain.
Respond naturally and consistently to the student's questions."""

conversation_history = []

def chat(user_message):
    """Send a message and get the patient's response."""
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

# Main loop
if __name__ == "__main__":
    print("Student: Type your questions for the patient. Type 'exit' to quit.\n")
    
    while True:
        student_input = input("Student: ").strip()
        if student_input.lower() == 'exit':
            break
        
        response = chat(student_input)
        print(f"Patient: {response}\n")


        
