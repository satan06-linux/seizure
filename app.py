"""
SeizureGuard AI - Main Streamlit Application
Intelligent Seizure Detection and Neurologist Recommendation System
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import os

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.predictor import SeizurePredictor
from modules.file_processor import FileProcessor
from modules.symptom_checker import SymptomChecker
from modules.chatbot import SeizureChatbot
from modules.doctor_recommender import DoctorRecommender


# Page configuration
st.set_page_config(
    page_title="SeizureGuard AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .risk-medium {
        background-color: #ffaa00;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .risk-low {
        background-color: #00cc66;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = SeizureChatbot()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'predictor_loaded' not in st.session_state:
        st.session_state.predictor_loaded = False
    if 'predictor' not in st.session_state:
        st.session_state.predictor = None


init_session_state()


# Sidebar navigation
def sidebar():
    st.sidebar.markdown("# 🧠 SeizureGuard AI")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📁 Upload EEG File", "🩺 Symptom Checker", 
         "💬 Chatbot", "👨‍⚕️ Find Neurologist"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "SeizureGuard AI uses machine learning to detect seizures "
        "and provide intelligent recommendations."
    )
    
    st.sidebar.markdown("### ⚠️ Disclaimer")
    st.sidebar.warning(
        "This is an AI assistant tool. Always consult healthcare "
        "professionals for medical advice."
    )
    
    return page


# Home page
def home_page():
    st.markdown('<div class="main-header">🧠 SeizureGuard AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Intelligent Seizure Detection and Neurologist Recommendation System</div>',
        unsafe_allow_html=True
    )
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 EEG Analysis")
        st.write("Upload EEG data in multiple formats (CSV, PDF, Image, EDF)")
        st.write("✓ Automated feature extraction")
        st.write("✓ Real-time prediction")
        st.write("✓ Confidence scoring")
    
    with col2:
        st.markdown("### 🩺 Symptom Analysis")
        st.write("Describe your symptoms in natural language")
        st.write("✓ Intelligent symptom detection")
        st.write("✓ Risk assessment")
        st.write("✓ Personalized recommendations")
    
    with col3:
        st.markdown("### 👨‍⚕️ Doctor Finder")
        st.write("Find qualified neurologists near you")
        st.write("✓ Specialization matching")
        st.write("✓ Emergency availability")
        st.write("✓ Rating-based ranking")
    
    st.markdown("---")
    
    # How it works
    st.markdown("## 🔍 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 1️⃣ Input")
        st.write("Upload EEG file or describe symptoms")
    
    with col2:
        st.markdown("### 2️⃣ Analysis")
        st.write("AI processes and extracts features")
    
    with col3:
        st.markdown("### 3️⃣ Prediction")
        st.write("ML model predicts seizure risk")
    
    with col4:
        st.markdown("### 4️⃣ Recommendation")
        st.write("Get doctor recommendations")
    
    st.markdown("---")
    
    # Statistics
    st.markdown("## 📈 System Capabilities")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Supported Formats", "5+", "CSV, PDF, Image, EDF")
    
    with col2:
        st.metric("Detection Classes", "3", "Normal, Preictal, Seizure")
    
    with col3:
        st.metric("Neurologists", "10+", "Across major cities")
    
    with col4:
        st.metric("Response Time", "<2s", "Real-time analysis")


# Upload EEG File page
def upload_file_page():
    st.markdown("# 📁 Upload EEG File")
    st.markdown("Upload your EEG data for seizure detection analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'pdf', 'png', 'jpg', 'jpeg', 'edf'],
        help="Supported formats: CSV, PDF, Image (PNG/JPG), EDF"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✓ File uploaded: {uploaded_file.name}")
        
        # Process file
        with st.spinner("Processing file..."):
            try:
                processor = FileProcessor()
                result = processor.process_file(temp_path)
                
                if result['success']:
                    st.success(f"✓ {result['message']}")
                    
                    # Show file info
                    st.markdown("### File Information")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**File Type:** {result['file_type'].upper()}")
                        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
                    
                    # Make prediction if model is available
                    if st.button("🔍 Analyze for Seizure Detection", type="primary"):
                        with st.spinner("Analyzing..."):
                            try:
                                # Load predictor
                                if not st.session_state.predictor_loaded:
                                    st.session_state.predictor = SeizurePredictor()
                                    st.session_state.predictor_loaded = True
                                
                                # Make prediction
                                prediction_result = st.session_state.predictor.predict(result['features'])
                                
                                # Display results
                                display_prediction_results(prediction_result)
                                
                                # Recommend doctors
                                st.markdown("---")
                                recommend_doctors_section(prediction_result['risk_level'])
                                
                            except FileNotFoundError:
                                st.error("⚠️ Model not found. Please train the model first.")
                                st.info("Run: `python modules/trainer.py` to train the model")
                            except Exception as e:
                                st.error(f"Error during prediction: {str(e)}")
                else:
                    st.error(f"Error processing file: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    else:
        # Show example
        st.info("👆 Upload a file to begin analysis")
        
        st.markdown("### Supported File Types:")
        st.markdown("""
        - **CSV**: EEG channel data in tabular format
        - **PDF**: EEG reports with text and numerical data
        - **Image (PNG/JPG)**: Scanned EEG reports
        - **EDF**: Standard EEG data format
        """)


# Symptom Checker page
def symptom_checker_page():
    st.markdown("# 🩺 Symptom Checker")
    st.markdown("Describe your symptoms to get a risk assessment")
    
    # Symptom input
    symptom_text = st.text_area(
        "Describe your symptoms:",
        placeholder="Example: I feel dizziness, confusion, and strange smells...",
        height=150
    )
    
    if st.button("🔍 Analyze Symptoms", type="primary"):
        if symptom_text.strip():
            with st.spinner("Analyzing symptoms..."):
                checker = SymptomChecker()
                result = checker.analyze_symptoms(symptom_text)
                
                # Display results
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                
                # Risk level
                risk_class = f"risk-{result['risk_level'].lower()}"
                st.markdown(
                    f'<div class="{risk_class}">Risk Level: {result["risk_level"]}</div>',
                    unsafe_allow_html=True
                )
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Risk Score", f"{result['risk_score']}/100")
                with col2:
                    st.metric("Condition", result['possible_condition'])
                with col3:
                    st.metric("Urgency", result['urgency'])
                
                # Detected symptoms
                if result['detected_symptoms']:
                    st.markdown("### Detected Symptoms")
                    for symptom in result['detected_symptoms']:
                        st.write(f"• {symptom['symptom'].title()} (Severity: {symptom['severity']})")
                
                # Explanation
                st.markdown("### Explanation")
                st.info(result['explanation'])
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                for rec in result['recommendations']:
                    st.write(f"• {rec}")
                
                # Doctor recommendations
                st.markdown("---")
                recommend_doctors_section(result['risk_level'])
        else:
            st.warning("Please describe your symptoms")
    
    # Common symptoms reference
    with st.expander("📋 Common Seizure Symptoms Reference"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Pre-Seizure (Aura):**")
            st.write("• Strange smells or tastes")
            st.write("• Visual disturbances")
            st.write("• Déjà vu feelings")
            st.write("• Sudden anxiety")
            
            st.markdown("**During Seizure:**")
            st.write("• Convulsions")
            st.write("• Loss of consciousness")
            st.write("• Muscle stiffness")
            st.write("• Jerking movements")
        
        with col2:
            st.markdown("**After Seizure:**")
            st.write("• Confusion")
            st.write("• Fatigue")
            st.write("• Memory loss")
            st.write("• Headache")
            
            st.markdown("**Other Symptoms:**")
            st.write("• Dizziness")
            st.write("• Numbness")
            st.write("• Weakness")
            st.write("• Tremors")


# Chatbot page
def chatbot_page():
    st.markdown("# 💬 AI Chatbot Assistant")
    st.markdown("Ask me anything about seizures, epilepsy, and neurological health")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['message']}")
            else:
                st.markdown(f"**Assistant:** {message['message']}")
            st.markdown("---")
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'message': user_input
        })
        
        # Get bot response
        response = st.session_state.chatbot.chat(user_input)
        
        # Add bot response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'message': response['message']
        })
        
        # Rerun to update display
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.chatbot.clear_history()
        st.rerun()
    
    # Quick questions
    st.markdown("### 💡 Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What is a seizure?"):
            st.session_state.chat_history.append({'role': 'user', 'message': 'What is a seizure?'})
            response = st.session_state.chatbot.chat('What is a seizure?')
            st.session_state.chat_history.append({'role': 'assistant', 'message': response['message']})
            st.rerun()
    
    with col2:
        if st.button("Seizure first aid"):
            st.session_state.chat_history.append({'role': 'user', 'message': 'What is seizure first aid?'})
            response = st.session_state.chatbot.chat('What is seizure first aid?')
            st.session_state.chat_history.append({'role': 'assistant', 'message': response['message']})
            st.rerun()
    
    with col3:
        if st.button("Types of seizures"):
            st.session_state.chat_history.append({'role': 'user', 'message': 'What are the types of seizures?'})
            response = st.session_state.chatbot.chat('What are the types of seizures?')
            st.session_state.chat_history.append({'role': 'assistant', 'message': response['message']})
            st.rerun()


# Find Neurologist page
def find_neurologist_page():
    st.markdown("# 👨‍⚕️ Find a Neurologist")
    st.markdown("Search for qualified neurologists in your area")
    
    recommender = DoctorRecommender()
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        location = st.selectbox(
            "Location",
            ["All Locations"] + recommender.get_all_locations()
        )
    
    with col2:
        specialization = st.selectbox(
            "Specialization",
            ["All Specializations"] + recommender.get_all_specializations()
        )
    
    with col3:
        emergency = st.checkbox("Emergency Care Available")
    
    # Search button
    if st.button("🔍 Search", type="primary"):
        # Prepare search parameters
        search_params = {
            'location': None if location == "All Locations" else location,
            'specialization': None if specialization == "All Specializations" else specialization,
            'emergency': emergency,
            'top_n': 10
        }
        
        # Get recommendations
        doctors = recommender.recommend_doctors(**search_params)
        
        if doctors:
            st.success(f"Found {len(doctors)} neurologist(s)")
            
            # Display doctors
            for i, doctor in enumerate(doctors, 1):
                with st.expander(f"{i}. {doctor['name']} - {doctor['specialization']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Hospital:** {doctor['hospital']}")
                        st.write(f"**Location:** {doctor['location']}")
                        st.write(f"**Phone:** {doctor['phone']}")
                    
                    with col2:
                        st.write(f"**Experience:** {doctor['experience_years']} years")
                        st.write(f"**Rating:** {doctor['rating']}/5.0 ⭐")
                        emergency_text = "✓ Available" if doctor['accepts_emergency'] else "✗ Not Available"
                        st.write(f"**Emergency Care:** {emergency_text}")
        else:
            st.warning("No doctors found matching your criteria. Try adjusting your filters.")
    
    # Emergency contacts
    st.markdown("---")
    st.markdown("### 🚨 Emergency Contacts")
    
    if st.button("Show Emergency Neurologists"):
        emergency_doctors = recommender.get_emergency_contacts()
        
        for doctor in emergency_doctors:
            st.error(f"**{doctor['name']}** - {doctor['phone']}")
            st.write(f"{doctor['hospital']}, {doctor['location']}")


# Helper functions
def display_prediction_results(result):
    """Display prediction results in a formatted way"""
    st.markdown("## 🎯 Prediction Results")
    
    # Risk level banner
    risk_class = f"risk-{result['risk_level'].lower()}"
    st.markdown(
        f'<div class="{risk_class}">Risk Level: {result["risk_level"]}</div>',
        unsafe_allow_html=True
    )
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Prediction", result['prediction'])
    
    with col2:
        st.metric("Confidence", f"{result['confidence']:.2f}%")
    
    with col3:
        st.metric("Risk Level", result['risk_level'])
    
    # Explanation
    st.markdown("### 📝 Explanation")
    st.info(result['explanation'])
    
    # Probability distribution
    st.markdown("### 📊 Probability Distribution")
    
    prob_df = pd.DataFrame({
        'Class': list(result['probabilities'].keys()),
        'Probability': list(result['probabilities'].values())
    })
    
    fig = px.bar(
        prob_df,
        x='Class',
        y='Probability',
        color='Probability',
        color_continuous_scale='RdYlGn_r',
        title='Prediction Probabilities'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def recommend_doctors_section(risk_level):
    """Display doctor recommendations based on risk level"""
    st.markdown("## 👨‍⚕️ Recommended Neurologists")
    
    recommender = DoctorRecommender()
    
    # Get recommendations based on risk level
    emergency = risk_level == 'HIGH'
    doctors = recommender.recommend_doctors(risk_level=risk_level, emergency=emergency, top_n=3)
    
    if risk_level == 'HIGH':
        st.error("⚠️ HIGH RISK: Immediate medical attention recommended!")
    
    for i, doctor in enumerate(doctors, 1):
        with st.expander(f"{i}. {doctor['name']} - {doctor['specialization']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Hospital:** {doctor['hospital']}")
                st.write(f"**Location:** {doctor['location']}")
                st.write(f"**Phone:** {doctor['phone']}")
            
            with col2:
                st.write(f"**Experience:** {doctor['experience_years']} years")
                st.write(f"**Rating:** {doctor['rating']}/5.0 ⭐")
                emergency_text = "✓ Available" if doctor['accepts_emergency'] else "✗ Not Available"
                st.write(f"**Emergency Care:** {emergency_text}")


# Main app
def main():
    page = sidebar()
    
    if page == "🏠 Home":
        home_page()
    elif page == "📁 Upload EEG File":
        upload_file_page()
    elif page == "🩺 Symptom Checker":
        symptom_checker_page()
    elif page == "💬 Chatbot":
        chatbot_page()
    elif page == "👨‍⚕️ Find Neurologist":
        find_neurologist_page()


if __name__ == "__main__":
    main()
