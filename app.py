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

# Initialize session state at the very beginning
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Configure Gemini API with key from secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
except Exception as e:
    st.error("Please configure GOOGLE_API_KEY in your Streamlit secrets.")
    st.stop()

# Enhanced CSS (your existing CSS code here)
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
    
    /* Message styling */
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
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

def is_medical_question(text):
    """Check if the question is medical-related"""
    medical_keywords = [
        'symptom', 'pain', 'treatment', 'medicine', 'doctor', 'health',
        'disease', 'condition', 'medical', 'diagnosis', 'hospital', 'clinic',
        'prescription', 'therapy', 'healing', 'recovery', 'patient', 'care'
    ]
    return any(keyword in text.lower() for keyword in medical_keywords)

def get_medical_response(prompt):
    """Get response from Gemini API with medical context"""
    if not is_medical_question(prompt):
        return "I can only assist with medical and health-related questions. Please ask something related to health, symptoms, treatments, or medical conditions."
    
    safety_prompt = f"""As a medical information assistant, please address this health-related query:
    {prompt}
    
    Please note:
    1. Provide general medical information from reputable sources
    2. Include relevant health precautions
    3. Recommend professional consultation when appropriate"""
    
    try:
        response = st.session_state.chat.send_message(safety_prompt)
        return response.text
    except Exception as e:
        return "I apologize, but I encountered an error processing your medical query. Please try rephrasing your question."

def main():
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("""
        <div style='padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%); border-radius: 10px;'>
            <h2 style='color: #2980b9; margin-bottom: 20px;'>
                <span style='font-size: 28px;'>🏥 🤖 MediChat Guide</span>
            </h2>
            
            <div class='info-card'>
                <h4 style='color: #2980b9;'>
                    <span style='font-size: 20px;'>💊 About This Assistant</span>
                </h4>
                <p>Your professional medical information companion</p>
            </div>
            
            <div class='info-card'>
                <h4 style='color: #2980b9;'>
                    <span style='font-size: 20px;'>⚕️ Important Notes</span>
                </h4>
                <p>
                🏨 Professional medical guidance<br>
                🚑 Emergency services information<br>
                👨‍⚕️ Healthcare consultation advice
                </p>
            </div>
            
            <div class='info-card'>
                <h4 style='color: #2980b9;'>
                    <span style='font-size: 20px;'>📋 Available Topics</span>
                </h4>
                <p>
                🔍 Medical Information<br>
                🤒 Symptom Guidance<br>
                📚 Health Education<br>
                💪 Wellness Tips
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced main interface
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>🏥 MediChat Assistant</h1>
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

                if any(word in user_input.lower() for word in ['treatment', 'medication', 'medicine']):
                    st.markdown("""
                    <div style='background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 10px; margin-top: 10px;'>
                    ⚠️ This information is for educational purposes only. Always consult a healthcare provider before starting or changing any treatment.
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
