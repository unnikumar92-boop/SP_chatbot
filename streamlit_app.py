from anthropic import Anthropic
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Load API key from Streamlit secrets or .env
if "ANTHROPIC_API_KEY" in st.secrets:
    client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
else:
    client = Anthropic()

system_prompt = """You are a patient visiting a speech pathology clinic. 
You have been diagnosed with a vocal cord tumor. 
You've had a hoarse voice for six weeks, are a smoker, and occasionally experience throat pain.
Respond naturally and consistently to the student's questions."""

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def add_message(role, content):
    """Helper function to add messages to conversation history."""
    st.session_state.conversation_history.append({
        "role": role,
        "content": content
    })

def display_messages():
    """Display all conversation messages."""
    for message in st.session_state.conversation_history:
        role = "Student" if message["role"] == "user" else "Patient"
        st.write(f"**{role}:** {message['content']}")

st.title("Speech Pathology Patient Interview Simulator")
st.write("Interview the patient and take a history. Type your questions below.")

display_messages()

with st.form("question_form"):
    student_input = st.text_input("Your question:")
    submitted = st.form_submit_button("Send")
    
    if submitted and student_input:
        add_message("user", student_input)
        
        try:
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                system=system_prompt,
                messages=st.session_state.conversation_history
            )
            
            add_message("assistant", response.content[0].text)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.info("Once you have completed your conversation click the three dots found at the top right hand corner and click print")

