# File: app.py

import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="MediChat Assistant",
    page_icon="🏥",
    layout="wide"
)

# Enhanced CSS with beautiful blue gradients and modern styling
st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #3498db, #2980b9);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #f8fafc;
        border-right: 1px solid #e1e8f0;
    }
    
    /* Chat message styling */
    .stTextInput input {
        border-radius: 20px;
        border: 2px solid #e1e8f0;
        padding: 10px 20px;
    }
    
    .stTextInput input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    /* Custom card styling */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(90deg, #2980b9, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    /* Message containers */
    .user-message {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
    }
    
    .assistant-message {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #3498db;
    }
    </style>
""", unsafe_allow_html=True)

# Rest of your existing code...

def main():
    init_session_state()
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("""
        <div style='padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%); border-radius: 10px;'>
            <h2 style='color: #2980b9; margin-bottom: 20px;'>🏥 MediChat Guide</h2>
            
            <div class='info-card'>
                <h4 style='color: #2980b9;'>About This Assistant</h4>
                <p>Your professional medical information companion</p>
            </div>
            
            <div class='info-card'>
                <h4 style='color: #2980b9;'>Important Notes</h4>
                • Professional medical guidance<br>
                • Emergency services information<br>
                • Healthcare consultation advice
            </div>
            
            <div class='info-card'>
                <h4 style='color: #2980b9;'>Available Topics</h4>
                • Medical Information<br>
                • Symptom Guidance<br>
                • Health Education<br>
                • Wellness Tips
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced main interface
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>MediChat Assistant</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Your Trusted Source for Medical Information</p>
        </div>
    """, unsafe_allow_html=True)

    # Chat interface
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

    # User input
    if user_input := st.chat_input("How can I help you with your health questions?"):
        with st.chat_message("user"):
            st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)
        st.session_state.conversation_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Processing your query..."):
                response = get_medical_response(user_input)
                st.markdown(f"<div class='assistant-message'>{response}</div>", unsafe_allow_html=True)
                st.session_state.conversation_history.append({"role": "assistant", "content": response})

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
