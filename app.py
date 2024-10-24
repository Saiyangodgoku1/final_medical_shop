# File: app.py

import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import re

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

# Medical keywords and categories for validation
MEDICAL_KEYWORDS = {
    'symptoms': ['pain', 'fever', 'cough', 'headache', 'nausea', 'fatigue', 'dizziness', 'rash'],
    'body_parts': ['head', 'chest', 'stomach', 'back', 'leg', 'arm', 'throat', 'ear', 'eye'],
    'conditions': ['diabetes', 'hypertension', 'asthma', 'allergies', 'infection', 'disease', 'syndrome'],
    'medical_terms': ['diagnosis', 'treatment', 'medication', 'prescription', 'dosage', 'vaccine', 'surgery'],
    'healthcare': ['doctor', 'hospital', 'clinic', 'emergency', 'medical', 'health', 'medicine'],
}

def init_session_state():
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

def is_medical_question(text):
    """
    Validate if the question is medical-related using keywords and context
    """
    text = text.lower()
    
    # Check for medical keywords
    for category in MEDICAL_KEYWORDS.values():
        if any(keyword in text for keyword in category):
            return True
    
    # Additional validation using medical context patterns
    medical_patterns = [
        r'(how|what|when|why|is|are|can|should).*(treat|cure|heal|help|relieve)',
        r'(symptoms of|signs of|treatment for|medicine for)',
        r'(medical|health|clinical|doctor|hospital)',
        r'(side effects|dosage|prescription)',
        r'(diagnosed with|suffering from|experiencing)',
    ]
    
    return any(re.search(pattern, text) for pattern in medical_patterns)

def validate_and_format_prompt(user_input):
    """
    Validate the input and format it for medical context
    """
    if not is_medical_question(user_input):
        return None, "I can only assist with medical and health-related questions. Please ask something related to health, symptoms, treatments, or medical conditions."
    
    # Format prompt with medical context
    formatted_prompt = f"""As a medical information assistant, please address this health-related query:

Question: {user_input}

Please provide information based on these guidelines:
1. Offer general medical information from reputable sources
2. Include relevant health precautions and warnings
3. Recommend professional medical consultation when appropriate
4. Focus only on well-established medical knowledge
5. Provide context for medical terms used

Response:"""
    
    return formatted_prompt, None

def get_medical_response(prompt):
    try:
        formatted_prompt, error = validate_and_format_prompt(prompt)
        if error:
            return error
            
        response = st.session_state.chat.send_message(formatted_prompt)
        return response.text
    except Exception as e:
        return "I apologize, but I encountered an error processing your medical query. Please try rephrasing your question."

def main():
    st.set_page_config(
        page_title="MediChat Assistant",
        page_icon="🏥",
        layout="wide"
    )
    
    init_session_state()
    
    # Sidebar with information
    with st.sidebar:
        st.title("ℹ️ About MediChat")
        st.markdown("""
        This medical chatbot provides general health information and guidance. 
        
        **Important Notes:**
        - Strictly for medical and health-related queries only
        - Not a substitute for professional medical advice
        - For emergencies, call emergency services immediately
        - Consult healthcare providers for personal medical advice
        
        **Supported Topics:**
        - General medical information
        - Symptom guidance
        - Health conditions
        - Treatment information
        - Medication general knowledge
        - Preventive care
        - Health education
        """)
        
        # Add API key input in sidebar
        api_key = st.text_input("Enter your Google API Key:", type="password")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            
        # Add medical disclaimer
        st.markdown("---")
        st.markdown("""
        ⚠️ **Medical Disclaimer**
        
        This chatbot provides general medical information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
        """)

    # Main chat interface
    st.title("🏥 MediChat Assistant")
    st.markdown("*Your trusted source for medical information - Ask health-related questions only*")
    st.markdown("---")

    # Chat interface
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Type your medical question here..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.conversation_history.append({"role": "user", "content": user_input})

        # Show thinking message
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your medical query..."):
                response = get_medical_response(user_input)
                st.markdown(response)
                st.session_state.conversation_history.append({"role": "assistant", "content": response})

                # Add medical disclaimer for treatments/medications
                if any(word in user_input.lower() for word in ['treatment', 'medication', 'medicine', 'drug']):
                    st.markdown("---")
                    st.markdown("""
                    *⚠️ Reminder: This information is for educational purposes only. Always consult a healthcare provider before starting or changing any treatment.*
                    """)

        # Add timestamp for the conversation
        st.caption(f"Response generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
