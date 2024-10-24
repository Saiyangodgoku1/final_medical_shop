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

# Enhanced CSS
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
        margin-bottom: 20px;
    }
    
    /* Message styling */
    .user-message {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    .assistant-message {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .info-card h4 {
        margin-bottom: 15px;
        color: #2980b9;
    }
    
    .info-card p {
        color: #2c3e50;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    /* List item styling */
    .list-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        padding: 5px;
        border-radius: 5px;
        transition: background-color 0.2s;
    }
    
    .list-item:hover {
        background-color: #f8fafc;
    }
    
    /* Emoji styling */
    .emoji {
        font-size: 1.2em;
        margin-right: 8px;
    }
    
    /* Input styling */
    .stTextInput > div > div {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #e1e8f0;
        padding: 8px 12px;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1d3e2;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3498db;
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
        st.title("🏥 🤖 MediChat Guide")
        
        col1, = st.columns(1)
        with col1:
            # About Section
            st.markdown("### 💊 About This Assistant")
            st.write("Your professional medical information companion")
            
            # Important Notes Section
            st.markdown("### ⚕️ Important Notes")
            st.markdown("- 🏥 Professional medical guidance")
            st.markdown("- 🚑 Emergency services information")
            st.markdown("- 👨‍⚕️ Healthcare consultation advice")
            
            # Available Topics Section
            st.markdown("### 📋 Available Topics")
            st.markdown("- 🔍 Medical Information")
            st.markdown("- 🤒 Symptom Guidance")
            st.markdown("- 📚 Health Education")
            st.markdown("- 💪 Wellness Tips")

    # Enhanced main interface (keeping original)
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>🏥 MediChat Assistant</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Your Trusted Source for Medical Information</p>
        </div>
    """, unsafe_allow_html=True)

    # Chat interface (keeping original)
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

    # User input (keeping original)
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
