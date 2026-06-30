import os
from anthropic import Anthropic
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = Anthropic()

# System prompt that defines the patient
system_prompt = """You are a patient visiting a speech pathology clinic. 
You have been diagnosed with vocal cord tumors. 
You've had a hoarse voice for six weeks, are a smoker, and occasionally experience throat pain.
Respond naturally and consistently to the student's questions."""

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

st.title("Speech Pathology Patient Interview Simulator")
st.write("Interview the patient and take a history. Type your questions below.")

# Display conversation history
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.write(f"**Student:** {message['content']}")
    else:
        st.write(f"**Patient:** {message['content']}")

# Form for input
with st.form("question_form"):
    student_input = st.text_input("Your question:")
    submitted = st.form_submit_button("Send")
    
    if submitted and student_input:
        # Add student message to history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": student_input
        })
        
        # Get patient response from Claude
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=st.session_state.conversation_history
        )
        
        patient_response = response.content[0].text
        
        # Add patient response to history
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": patient_response
        })
        
        # Rerun to display the new messages
        st.rerun()
