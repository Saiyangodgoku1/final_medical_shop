# File: app.py

import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure Streamlit page settings
st.set_page_config(
    page_title="MediChat Assistant",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for lighter color scheme
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .stMarkdown {
        color: #495057;
    }
    .stSidebar {
        background-color: #ffffff;
    }
    .stButton button {
        background-color: #6c9dc6;
        color: white;
    }
    .stTextInput input {
        background-color: #ffffff;
    }
    div[data-testid="stHeader"] {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Configure Gemini API with key from secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    st.error("Please configure GOOGLE_API_KEY in your Streamlit secrets.")
    st.stop()

# Medical keywords and categories for validation
MEDICAL_KEYWORDS = {
    'symptoms': ['pain', 'fever', 'cough', 'headache', 'nausea', 'fatigue'],
    'body_parts': ['head', 'chest', 'stomach', 'back', 'leg', 'arm', 'throat'],
    'conditions': ['diabetes', 'hypertension', 'asthma', 'allergies', 'infection'],
    'medical_terms': ['diagnosis', 'treatment', 'medication', 'prescription'],
    'healthcare': ['doctor', 'hospital', 'clinic', 'emergency', 'medical', 'health']
}

def init_session_state():
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

def is_medical_question(text):
    text = text.lower()
    return any(keyword in text for category in MEDICAL_KEYWORDS.values() for keyword in category)

def get_medical_response(prompt):
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
    init_session_state()
    
    # Sidebar with lighter colors
    with st.sidebar:
        st.title("ℹ️ MediChat Guide")
        st.markdown("""
        <div style='background-color: #ffffff; padding: 15px; border-radius: 5px; border: 1px solid #e9ecef;'>
        <h4 style='color: #6c9dc6;'>About This Assistant</h4>
        This medical chatbot provides general health information and guidance.
        
        <h4 style='color: #6c9dc6; margin-top: 15px;'>Important Notes:</h4>
        • Not a substitute for professional medical advice<br>
        • For emergencies, call emergency services<br>
        • Consult healthcare providers for personal medical advice
        
        <h4 style='color: #6c9dc6; margin-top: 15px;'>Topics Covered:</h4>
        • General medical information<br>
        • Symptom guidance<br>
        • Health education<br>
        • Wellness tips
        </div>
        """, unsafe_allow_html=True)

    # Main chat interface
    st.title("🏥 MediChat Assistant")
    st.markdown("<p style='color: #6c9dc6; font-size: 1.2em;'>Your trusted source for medical information</p>", unsafe_allow_html=True)
    st.markdown("<hr style='background-color: #e9ecef;'>", unsafe_allow_html=True)

    # Chat interface
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Ask your health-related question..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.conversation_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your query..."):
                response = get_medical_response(user_input)
                st.markdown(response)
                st.session_state.conversation_history.append({"role": "assistant", "content": response})

                if any(word in user_input.lower() for word in ['treatment', 'medication', 'medicine']):
                    st.markdown("""
                    <div style='background-color: #e9ecef; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                    ⚠️ This information is for educational purposes only. Always consult a healthcare provider before starting or changing any treatment.
                    </div>
                    """, unsafe_allow_html=True)

        st.caption(f"Response generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
