import os
from anthropic import Anthropic
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

load_dotenv()

# Load API key from Streamlit secrets or .env
if "ANTHROPIC_API_KEY" in st.secrets:
    client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
else:
    client = Anthropic()

# System prompt that defines the patient
system_prompt = """You are a patient visiting a speech pathology clinic. 
You have been diagnosed with vocal cord tumors. 
You've had a hoarse voice for six weeks, are a smoker, and occasionally experience throat pain.
Respond naturally and consistently to the student's questions."""

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "interaction_started" not in st.session_state:
    st.session_state.interaction_started = False

st.title("Speech Pathology Patient Interview Simulator")

# Begin/End interaction buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Begin Interaction with Patient"):
        st.session_state.interaction_started = True
        st.session_state.conversation_history = []
        st.success("Interaction started! Begin asking the patient questions.")

with col2:
    if st.button("End Interaction"):
        st.session_state.interaction_started = False

# If interaction hasn't started, show instructions
if not st.session_state.interaction_started:
    st.info("Click 'Begin Interaction with Patient' to start the interview.")
else:
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

# Show save options when interaction has ended
if not st.session_state.interaction_started and st.session_state.conversation_history:
    st.divider()
    st.subheader("Interaction Record")
    
    # Create conversation summary
    conversation_text = "SPEECH PATHOLOGY PATIENT INTERVIEW RECORD\n"
    conversation_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    conversation_text += "=" * 60 + "\n\n"
    
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            conversation_text += f"Student: {message['content']}\n\n"
        else:
            conversation_text += f"Patient: {message['content']}\n\n"
    
    # Display the record
    st.text_area("Conversation Record:", value=conversation_text, height=300, disabled=True)
    
    # Download button
    st.download_button(
        label="Download Conversation Record",
        data=conversation_text,
        file_name=f"patient_interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )
