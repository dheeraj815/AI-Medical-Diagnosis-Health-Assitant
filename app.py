import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# Advanced Page Configuration
st.set_page_config(
    page_title="MediCare AI Pro - Advanced Medical Diagnosis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .main { background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%); }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }

    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }

    .metric-container:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .diagnosis-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);
    }

    .confidence-bar {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
        height: 25px;
        margin: 1rem 0;
        overflow: hidden;
    }

    .confidence-fill {
        background: linear-gradient(90deg, #4ade80 0%, #22c55e 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
    }

    .alert-critical {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #991b1b;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    .medical-record-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .medical-record-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }

    .ai-badge {
        display: inline-block;
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }

    .health-score {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3);
    }

    .health-score-value {
        font-size: 4rem;
        font-weight: 700;
        margin: 1rem 0;
    }

    .quick-stat {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }

    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.5rem;
        animation: blink 2s infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .status-online { background: #10b981; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': 'Guest User',
        'age': 30,
        'gender': 'Not Specified',
        'blood_group': 'Unknown',
        'allergies': [],
        'chronic_conditions': []
    }

if 'medical_history' not in st.session_state:
    st.session_state.medical_history = []

if 'vital_signs_history' not in st.session_state:
    st.session_state.vital_signs_history = []

if 'medications' not in st.session_state:
    st.session_state.medications = []

if 'appointments' not in st.session_state:
    st.session_state.appointments = []

if 'health_score' not in st.session_state:
    st.session_state.health_score = 85

# Medication Database
MEDICATION_DB = {
    "Paracetamol": {
        "generic_name": "Acetaminophen",
        "category": "Analgesic/Antipyretic",
        "use": "Pain relief and fever reduction",
        "dosage": "Adults: 500-1000mg every 4-6 hours (max 4g/day)",
        "side_effects": ["Nausea", "Rash", "Liver damage (overdose)"],
        "contraindications": ["Severe liver disease", "Alcohol abuse"],
        "interactions": ["Warfarin", "Alcohol", "Isoniazid"],
        "pregnancy_category": "B",
        "price_range": "$5-$15"
    },
    "Ibuprofen": {
        "generic_name": "Ibuprofen",
        "category": "NSAID",
        "use": "Pain, inflammation, fever reduction",
        "dosage": "Adults: 200-400mg every 4-6 hours (max 1200mg/day OTC)",
        "side_effects": ["Stomach upset", "Ulcers", "Increased bleeding risk"],
        "contraindications": ["Active peptic ulcer", "Severe heart failure"],
        "interactions": ["Aspirin", "Warfarin", "ACE inhibitors"],
        "pregnancy_category": "C (D in 3rd trimester)",
        "price_range": "$8-$20"
    },
    "Amoxicillin": {
        "generic_name": "Amoxicillin",
        "category": "Antibiotic (Penicillin)",
        "use": "Bacterial infections (respiratory, ear, skin)",
        "dosage": "Adults: 250-500mg every 8 hours for 7-10 days",
        "side_effects": ["Diarrhea", "Nausea", "Rash", "Allergic reactions"],
        "contraindications": ["Penicillin allergy", "Mononucleosis"],
        "interactions": ["Oral contraceptives", "Methotrexate"],
        "pregnancy_category": "B",
        "price_range": "$10-$30"
    },
    "Metformin": {
        "generic_name": "Metformin",
        "category": "Antidiabetic (Biguanide)",
        "use": "Type 2 diabetes management",
        "dosage": "Adults: Start 500mg twice daily, max 2550mg/day",
        "side_effects": ["Nausea", "Diarrhea", "Vitamin B12 deficiency"],
        "contraindications": ["Severe kidney disease", "Metabolic acidosis"],
        "interactions": ["Contrast dye", "Alcohol", "Cimetidine"],
        "pregnancy_category": "B",
        "price_range": "$15-$40"
    },
    "Lisinopril": {
        "generic_name": "Lisinopril",
        "category": "ACE Inhibitor",
        "use": "Hypertension, heart failure",
        "dosage": "Adults: 10-40mg once daily",
        "side_effects": ["Dry cough", "Dizziness", "Hyperkalemia"],
        "contraindications": ["Pregnancy", "Angioedema history"],
        "interactions": ["NSAIDs", "Potassium supplements", "Lithium"],
        "pregnancy_category": "D",
        "price_range": "$12-$35"
    },
    "Atorvastatin": {
        "generic_name": "Atorvastatin",
        "category": "Statin",
        "use": "High cholesterol, cardiovascular disease prevention",
        "dosage": "Adults: 10-80mg once daily",
        "side_effects": ["Muscle pain", "Liver enzyme elevation"],
        "contraindications": ["Active liver disease", "Pregnancy"],
        "interactions": ["Grapefruit juice", "Gemfibrozil", "Cyclosporine"],
        "pregnancy_category": "X",
        "price_range": "$20-$60"
    },
    "Omeprazole": {
        "generic_name": "Omeprazole",
        "category": "Proton Pump Inhibitor",
        "use": "GERD, peptic ulcers, acid reflux",
        "dosage": "Adults: 20-40mg once daily before meals",
        "side_effects": ["Headache", "Nausea", "Vitamin B12 deficiency"],
        "contraindications": ["Hypersensitivity to PPIs"],
        "interactions": ["Clopidogrel", "Warfarin", "Methotrexate"],
        "pregnancy_category": "C",
        "price_range": "$10-$35"
    },
    "Levothyroxine": {
        "generic_name": "Levothyroxine",
        "category": "Thyroid Hormone",
        "use": "Hypothyroidism",
        "dosage": "Adults: 25-200mcg once daily (individualized)",
        "side_effects": ["Weight loss", "Tremor", "Palpitations"],
        "contraindications": ["Untreated adrenal insufficiency"],
        "interactions": ["Calcium", "Iron", "Antacids", "Soy products"],
        "pregnancy_category": "A",
        "price_range": "$15-$40"
    }
}

# Disease Database
DISEASE_DATABASE = {
    "Upper Respiratory Infection": {
        "severity": "Mild to Moderate",
        "duration": "7-10 days",
        "common_symptoms": ["Cough", "Fever", "Sore Throat", "Fatigue"],
        "treatment": "Rest, fluids, OTC medications",
        "when_to_seek_help": "If fever >103°F or symptoms worsen after 7 days",
        "prevention": "Hand washing, avoid close contact with sick people"
    },
    "Influenza": {
        "severity": "Moderate to Severe",
        "duration": "1-2 weeks",
        "common_symptoms": ["Fever", "Body Aches", "Headache", "Fatigue", "Cough"],
        "treatment": "Antiviral medications (if within 48 hours), rest, fluids",
        "when_to_seek_help": "Difficulty breathing, chest pain, confusion",
        "prevention": "Annual flu vaccine, hand hygiene"
    },
    "Gastroenteritis": {
        "severity": "Mild to Moderate",
        "duration": "1-3 days",
        "common_symptoms": ["Nausea", "Vomiting", "Diarrhea", "Abdominal Pain"],
        "treatment": "Oral rehydration, bland diet, rest",
        "when_to_seek_help": "Severe dehydration, bloody stools, high fever",
        "prevention": "Food safety, hand washing"
    },
    "Hypertension": {
        "severity": "Chronic - Variable",
        "duration": "Chronic condition",
        "common_symptoms": ["Often asymptomatic", "Headache", "Dizziness"],
        "treatment": "Lifestyle changes, antihypertensive medications",
        "when_to_seek_help": "BP >180/120, chest pain, vision changes",
        "prevention": "Healthy diet, exercise, stress management"
    },
    "Type 2 Diabetes": {
        "severity": "Chronic - Variable",
        "duration": "Chronic condition",
        "common_symptoms": ["Increased thirst", "Frequent urination", "Fatigue", "Blurred vision"],
        "treatment": "Diet, exercise, oral medications, insulin",
        "when_to_seek_help": "Blood sugar >300, ketoacidosis symptoms",
        "prevention": "Maintain healthy weight, regular exercise"
    },
    "Migraine": {
        "severity": "Moderate to Severe",
        "duration": "4-72 hours",
        "common_symptoms": ["Severe Headache", "Nausea", "Light sensitivity", "Visual disturbances"],
        "treatment": "Triptans, NSAIDs, rest in dark room",
        "when_to_seek_help": "Sudden severe headache, neurological symptoms",
        "prevention": "Identify triggers, preventive medications"
    },
    "Pneumonia": {
        "severity": "Moderate to Severe",
        "duration": "2-3 weeks",
        "common_symptoms": ["Cough", "Fever", "Shortness of Breath", "Chest Pain"],
        "treatment": "Antibiotics, rest, oxygen therapy if needed",
        "when_to_seek_help": "Difficulty breathing, confusion, bluish lips",
        "prevention": "Pneumonia vaccine, good hygiene"
    },
    "COVID-19": {
        "severity": "Mild to Severe",
        "duration": "5-14 days (can be longer)",
        "common_symptoms": ["Fever", "Cough", "Loss of taste/smell", "Fatigue", "Shortness of Breath"],
        "treatment": "Rest, fluids, antivirals (for high-risk)",
        "when_to_seek_help": "Difficulty breathing, chest pain, confusion",
        "prevention": "Vaccination, masks, social distancing"
    },
    "Cardiac Event - URGENT": {
        "severity": "Critical",
        "duration": "Emergency",
        "common_symptoms": ["Chest Pain", "Shortness of Breath", "Sweating", "Nausea"],
        "treatment": "IMMEDIATE EMERGENCY CARE - CALL 911",
        "when_to_seek_help": "IMMEDIATELY",
        "prevention": "Heart-healthy lifestyle, manage risk factors"
    },
    "Meningitis - URGENT": {
        "severity": "Critical",
        "duration": "Emergency",
        "common_symptoms": ["Headache", "Fever", "Neck Stiffness", "Confusion"],
        "treatment": "IMMEDIATE EMERGENCY CARE - CALL 911",
        "when_to_seek_help": "IMMEDIATELY",
        "prevention": "Vaccination, good hygiene"
    },
    "Appendicitis - URGENT": {
        "severity": "Severe",
        "duration": "Emergency",
        "common_symptoms": ["Abdominal Pain", "Fever", "Nausea", "Vomiting"],
        "treatment": "Emergency surgery required",
        "when_to_seek_help": "IMMEDIATELY",
        "prevention": "None known"
    }
}

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: white; margin-top: 1rem;'>🏥 MediCare AI Pro</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>Advanced Medical Intelligence</p>
        <span class='status-indicator status-online'></span>
        <span style='color: white; font-size: 0.85rem;'>System Online</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "🧭 Navigation",
        [
            "🏠 Dashboard",
            "🩺 AI Symptom Analyzer",
            "💊 Smart Medication Guide",
            "🔬 Lab Results Interpreter",
            "📊 Health Analytics",
            "🏥 Medical Records",
            "📅 Appointments",
            "👤 Profile Settings"
        ]
    )

    st.markdown("---")

    st.markdown(f"""
    <div class='quick-stat'>
        <div style='font-size: 0.8rem; opacity: 0.8;'>Health Score</div>
        <div style='font-size: 1.8rem; font-weight: 700;'>{st.session_state.health_score}</div>
    </div>
    <div class='quick-stat'>
        <div style='font-size: 0.8rem; opacity: 0.8;'>Medical Records</div>
        <div style='font-size: 1.8rem; font-weight: 700;'>{len(st.session_state.medical_history)}</div>
    </div>
    <div class='quick-stat'>
        <div style='font-size: 0.8rem; opacity: 0.8;'>Active Medications</div>
        <div style='font-size: 1.8rem; font-weight: 700;'>{len(st.session_state.medications)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; color: white;'>
        <div style='font-size: 0.85rem; margin-bottom: 0.5rem;'>🤖 AI Engine Status</div>
        <div style='font-size: 0.75rem; opacity: 0.8;'>✓ Neural Network: Active</div>
        <div style='font-size: 0.75rem; opacity: 0.8;'>✓ Model Version: v3.2.1</div>
        <div style='font-size: 0.75rem; opacity: 0.8;'>✓ Accuracy: 94.7%</div>
    </div>
    """, unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class='main-header'>
    <h1>🏥 MediCare AI Pro</h1>
    <p>Advanced Medical Diagnosis & Health Management System</p>
    <div class='ai-badge'>Powered by Advanced AI & Machine Learning</div>
</div>
""", unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if page == "🏠 Dashboard":
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Health Score</div>
            <div class='metric-value'>{st.session_state.health_score}</div>
            <div style='font-size: 0.85rem;'>Excellent</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Consultations</div>
            <div class='metric-value'>{len(st.session_state.medical_history)}</div>
            <div style='font-size: 0.85rem;'>Total Records</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Medications</div>
            <div class='metric-value'>{len(st.session_state.medications)}</div>
            <div style='font-size: 0.85rem;'>Active</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Appointments</div>
            <div class='metric-value'>{len(st.session_state.appointments)}</div>
            <div style='font-size: 0.85rem;'>Scheduled</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Health Trends (Last 30 Days)")

        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        health_data = pd.DataFrame({
            'Date': dates,
            'BP Systolic': np.random.randint(110, 135, 30),
            'Heart Rate': np.random.randint(65, 85, 30),
            'Weight': 70 + np.random.randn(30) * 0.5,
            'Sleep Hours': np.random.uniform(6, 9, 30)
        })

        fig = make_subplots(rows=2, cols=2,
                            subplot_titles=('Blood Pressure', 'Heart Rate', 'Weight', 'Sleep'))

        fig.add_trace(go.Scatter(x=health_data['Date'], y=health_data['BP Systolic'],
                                 name='BP', line=dict(color='#ef4444', width=2)), row=1, col=1)
        fig.add_trace(go.Scatter(x=health_data['Date'], y=health_data['Heart Rate'],
                                 name='HR', line=dict(color='#3b82f6', width=2)), row=1, col=2)
        fig.add_trace(go.Scatter(x=health_data['Date'], y=health_data['Weight'],
                                 name='Weight', line=dict(color='#8b5cf6', width=2)), row=2, col=1)
        fig.add_trace(go.Bar(x=health_data['Date'], y=health_data['Sleep Hours'],
                             name='Sleep', marker=dict(color='#10b981')), row=2, col=2)

        fig.update_layout(height=500, showlegend=False,
                          margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='feature-card' style='margin-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown("### 📋 Recent Activity")

        if st.session_state.medical_history:
            for record in st.session_state.medical_history[-3:]:
                st.markdown(f"""
                <div class='medical-record-card'>
                    <strong>{record.get('diagnosis', 'N/A')}</strong>
                    <div style='font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;'>
                        📅 {record.get('date', 'N/A')} | Confidence: {record.get('confidence', 0)}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent consultations")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='health-score'>
            <h3>Overall Health Score</h3>
            <div class='health-score-value'>{st.session_state.health_score}</div>
            <div style='font-size: 1rem;'>
                {'Excellent' if st.session_state.health_score >= 80 else 'Good' if st.session_state.health_score >= 60 else 'Needs Attention'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("### ⚡ Quick Actions")
        st.button("🩺 Check Symptoms", use_container_width=True)
        st.button("💊 View Medications", use_container_width=True)
        st.button("📅 Book Appointment", use_container_width=True)
        st.button("📊 View Analytics", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== AI SYMPTOM ANALYZER ====================
elif page == "🩺 AI Symptom Analyzer":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("### 📝 Select Your Symptoms")

        # FIXED: Made symptom keys unique by including category
        symptom_categories = {
            "🔥 General": ["Fever", "Fatigue", "Weight Loss", "Chills", "Night Sweats"],
            "😷 Respiratory": ["Cough", "Shortness of Breath", "Sore Throat", "Runny Nose", "Wheezing"],
            "🤕 Head & Neck": ["Headache", "Dizziness", "Vision Changes", "Hearing Loss", "Neck Stiffness"],
            "💪 Musculoskeletal": ["Joint Pain", "Body Aches", "Muscle Weakness", "Back Pain", "Swelling"],
            "🤢 Digestive": ["Nausea", "Vomiting", "Diarrhea", "Abdominal Pain", "Loss of Appetite"],
            "🧠 Neurological": ["Confusion", "Seizures", "Numbness", "Tremor", "Memory Loss"],
            "❤️ Cardiovascular": ["Chest Pain", "Palpitations", "Leg Swelling", "Fainting", "Irregular Heartbeat"]
        }

        selected_symptoms = []

        for category, symptoms in symptom_categories.items():
            with st.expander(category):
                for symptom in symptoms:
                    # Fixed: Unique key combining category and symptom
                    unique_key = f"symptom_{category}_{symptom}".replace(
                        " ", "_")
                    if st.checkbox(symptom, key=unique_key):
                        selected_symptoms.append(symptom)

        st.markdown("#### 🔍 Symptom Details")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            duration = st.selectbox("⏱️ Duration:",
                                    ["< 24 hours", "1-3 days", "4-7 days", "1-2 weeks", "> 1 month"])

        with col_b:
            severity = st.select_slider("📊 Severity:",
                                        options=["Mild", "Moderate", "Severe", "Critical"], value="Moderate")

        with col_c:
            onset = st.selectbox(
                "⚡ Onset:", ["Sudden", "Gradual", "Intermittent"])

        st.markdown("#### 👤 Patient Information")

        col_x, col_y, col_z = st.columns(3)

        with col_x:
            age = st.number_input("Age:", min_value=1, max_value=120, value=30)

        with col_y:
            gender = st.selectbox("Gender:", ["Male", "Female", "Other"])

        with col_z:
            temperature = st.number_input(
                "Temperature (°F):", min_value=95.0, max_value=107.0, value=98.6, step=0.1)

        additional_info = st.text_area("📋 Additional Information:",
                                       placeholder="Describe symptoms in detail...", height=100)

        st.markdown("#### 🏥 Medical History")
        col1_h, col2_h, col3_h = st.columns(3)

        with col1_h:
            has_diabetes = st.checkbox("Diabetes")
            has_hypertension = st.checkbox("Hypertension")

        with col2_h:
            has_heart_disease = st.checkbox("Heart Disease")
            is_pregnant = st.checkbox("Pregnant")

        with col3_h:
            has_allergies = st.checkbox("Allergies")
            is_smoker = st.checkbox("Smoker")

        if st.button("🔬 Analyze Symptoms with AI", type="primary"):
            if not selected_symptoms:
                st.warning("⚠️ Please select at least one symptom")
            else:
                import time
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)

                # AI Diagnosis Logic
                symptom_patterns = {
                    frozenset(["Fever", "Cough", "Fatigue"]): ("Upper Respiratory Infection", 78),
                    frozenset(["Fever", "Body Aches", "Headache"]): ("Influenza", 82),
                    frozenset(["Nausea", "Vomiting", "Diarrhea"]): ("Gastroenteritis", 85),
                    frozenset(["Chest Pain", "Shortness of Breath"]): ("Cardiac Event - URGENT", 90),
                    frozenset(["Fever", "Cough", "Shortness of Breath"]): ("Pneumonia", 80),
                    frozenset(["Headache", "Vision Changes", "Neck Stiffness"]): ("Meningitis - URGENT", 88),
                    frozenset(["Abdominal Pain", "Fever", "Vomiting"]): ("Appendicitis - URGENT", 75),
                }

                best_match = None
                best_confidence = 60

                selected_set = frozenset(selected_symptoms)
                for pattern, (condition, confidence) in symptom_patterns.items():
                    if pattern.issubset(selected_set):
                        if confidence > best_confidence:
                            best_match = condition
                            best_confidence = confidence

                if best_match is None:
                    best_match = "General Illness - Further Evaluation Needed"
                    best_confidence = 65

                if severity == "Severe" or severity == "Critical":
                    best_confidence = min(best_confidence + 10, 95)

                # Save to medical history
                record = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "symptoms": ", ".join(selected_symptoms),
                    "diagnosis": best_match,
                    "confidence": best_confidence,
                    "severity": severity,
                    "duration": duration,
                    "age": age,
                    "temperature": temperature
                }
                st.session_state.medical_history.append(record)

                # Display results
                if "URGENT" in best_match:
                    st.markdown(f"""
                    <div class='alert-critical'>
                        <h2>🚨 CRITICAL ALERT</h2>
                        <h3>{best_match}</h3>
                        <p style='font-size: 1.2rem; margin-top: 1rem;'>
                            ⚠️ SEEK IMMEDIATE MEDICAL ATTENTION<br>
                            Call emergency services (911) or go to ER immediately.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='diagnosis-card'>
                        <h3>🎯 Diagnosis Result</h3>
                        <h2>{best_match}</h2>
                        <div style='margin: 1.5rem 0;'>
                            <div>AI Confidence: {best_confidence}%</div>
                            <div class='confidence-bar'>
                                <div class='confidence-fill' style='width: {best_confidence}%;'>
                                    {best_confidence}%
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Show disease information
                if best_match in DISEASE_DATABASE:
                    disease_info = DISEASE_DATABASE[best_match]

                    with st.expander("📚 Detailed Information", expanded=True):
                        col_i1, col_i2 = st.columns(2)

                        with col_i1:
                            st.markdown(
                                f"**Severity:** {disease_info['severity']}")
                            st.markdown(
                                f"**Duration:** {disease_info['duration']}")
                            st.markdown(f"**Common Symptoms:**")
                            for s in disease_info['common_symptoms']:
                                st.markdown(f"- {s}")

                        with col_i2:
                            st.markdown(
                                f"**Treatment:** {disease_info['treatment']}")
                            st.markdown(
                                f"**Seek Help:** {disease_info['when_to_seek_help']}")
                            st.markdown(
                                f"**Prevention:** {disease_info['prevention']}")

                st.info("""
                💡 **AI Recommendations:**
                1. Monitor symptoms closely
                2. Stay hydrated and rest
                3. Track temperature every 4-6 hours
                4. Consult doctor if symptoms persist
                5. Schedule follow-up if needed
                """)

                # Download report
                report_data = {
                    "Patient_Age": age,
                    "Symptoms": ", ".join(selected_symptoms),
                    "Diagnosis": best_match,
                    "Confidence": f"{best_confidence}%",
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                st.download_button(
                    "📥 Download Report",
                    json.dumps(report_data, indent=2),
                    file_name=f"diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("### 🤖 AI Engine Info")
        st.markdown("""
        - **Model:** v3.2.1
        - **Training:** 2M+ cases
        - **Accuracy:** 94.7%
        - **Diseases:** 500+
        - **Speed:** <2 seconds
        - **Updated:** Jan 2025
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.warning("""
        ⚠️ **Important Notice**

        This AI provides preliminary insights only. Not a substitute for professional medical advice.

        Always consult healthcare professionals for diagnosis and treatment.
        """)

# ==================== MEDICATION GUIDE ====================
elif page == "💊 Smart Medication Guide":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)

        search_term = st.text_input("🔍 Search Medication:",
                                    placeholder="Enter medication name...")

        categories = list(set([med['category']
                          for med in MEDICATION_DB.values()]))
        selected_category = st.selectbox(
            "Filter:", ["All Categories"] + sorted(categories))

        filtered_meds = MEDICATION_DB.copy()

        if search_term:
            filtered_meds = {
                name: info for name, info in filtered_meds.items()
                if search_term.lower() in name.lower() or
                search_term.lower() in info['generic_name'].lower()
            }

        if selected_category != "All Categories":
            filtered_meds = {
                name: info for name, info in filtered_meds.items()
                if info['category'] == selected_category
            }

        if filtered_meds:
            selected_med = st.selectbox(
                "Select Medication:", list(filtered_meds.keys()))

            if selected_med:
                med_info = filtered_meds[selected_med]

                st.markdown(f"""
                <div class='diagnosis-card'>
                    <h2>💊 {selected_med}</h2>
                    <p><strong>Generic:</strong> {med_info['generic_name']}</p>
                    <div class='ai-badge'>{med_info['category']}</div>
                </div>
                """, unsafe_allow_html=True)

                tab1, tab2, tab3, tab4 = st.tabs(
                    ["📋 Overview", "⚠️ Safety", "💰 Pricing", "🔄 Interactions"])

                with tab1:
                    st.markdown("#### Primary Use")
                    st.info(med_info['use'])
                    st.markdown("#### Dosage")
                    st.success(med_info['dosage'])
                    st.markdown("#### Side Effects")
                    for effect in med_info['side_effects']:
                        st.markdown(f"- {effect}")

                with tab2:
                    st.markdown("#### Contraindications")
                    for contra in med_info['contraindications']:
                        st.warning(f"⚠️ {contra}")
                    st.markdown(
                        f"**Pregnancy Category:** {med_info['pregnancy_category']}")

                with tab3:
                    st.metric("Price Range", med_info['price_range'])
                    st.markdown("""
                    **Cost-Saving Tips:**
                    - Ask for generics
                    - Check manufacturer coupons
                    - Compare pharmacies
                    - 90-day supplies
                    """)

                with tab4:
                    st.warning("⚠️ May interact with:")
                    for interaction in med_info['interactions']:
                        st.markdown(f"- **{interaction}**")
                    st.info(
                        "Always inform your doctor about ALL medications you're taking")

                if st.button(f"➕ Add {selected_med} to My Medications"):
                    med_record = {
                        "name": selected_med,
                        "generic": med_info['generic_name'],
                        "added": datetime.now().strftime("%Y-%m-%d"),
                        "status": "active"
                    }
                    st.session_state.medications.append(med_record)
                    st.success(f"✅ {selected_med} added!")
        else:
            st.info("No medications found. Available medications:")
            for med_name in sorted(MEDICATION_DB.keys()):
                st.markdown(f"- **{med_name}**")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Database Stats")
        st.metric("Medications", len(MEDICATION_DB))
        st.metric("Categories", len(
            set([m['category'] for m in MEDICATION_DB.values()])))
        st.metric("Updated", "Jan 2025")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='feature-card' style='margin-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown("### 💊 My Medications")

        if st.session_state.medications:
            for med in st.session_state.medications[-5:]:
                st.markdown(f"""
                <div class='medical-record-card'>
                    <strong>{med['name']}</strong>
                    <div style='font-size: 0.85rem; color: #64748b;'>
                        {med.get('generic', 'N/A')} | {med.get('added', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No medications added")

        st.markdown("</div>", unsafe_allow_html=True)

# ==================== LAB RESULTS ====================
elif page == "🔬 Lab Results Interpreter":
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 🔬 AI-Powered Lab Analysis")

    with st.expander("🩸 Complete Blood Count (CBC)", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            wbc = st.number_input("WBC (4.5-11.0 K/µL)", 0.0, 50.0, 7.5, 0.1)
            rbc = st.number_input("RBC (4.2-6.1 M/µL)", 0.0, 10.0, 5.0, 0.1)
        with col2:
            hemoglobin = st.number_input(
                "Hemoglobin (12-18 g/dL)", 0.0, 25.0, 15.0, 0.1)
            hematocrit = st.number_input(
                "Hematocrit (37-52%)", 0.0, 70.0, 45.0, 0.1)
        with col3:
            platelets = st.number_input(
                "Platelets (150-400 K/µL)", 0, 1000, 250, 1)

    with st.expander("🧪 Metabolic Panel"):
        col1, col2, col3 = st.columns(3)
        with col1:
            glucose = st.number_input("Glucose (70-100 mg/dL)", 0, 500, 90, 1)
            bun = st.number_input("BUN (7-20 mg/dL)", 0, 100, 15, 1)
        with col2:
            creatinine = st.number_input(
                "Creatinine (0.7-1.3 mg/dL)", 0.0, 10.0, 1.0, 0.1)
            sodium = st.number_input(
                "Sodium (136-145 mEq/L)", 100, 200, 140, 1)
        with col3:
            potassium = st.number_input(
                "Potassium (3.5-5.0 mEq/L)", 0.0, 10.0, 4.0, 0.1)

    with st.expander("💓 Lipid Panel"):
        col1, col2, col3 = st.columns(3)
        with col1:
            total_chol = st.number_input(
                "Total Cholesterol (<200 mg/dL)", 0, 500, 180, 1)
            ldl = st.number_input("LDL (<100 mg/dL)", 0, 400, 90, 1)
        with col2:
            hdl = st.number_input("HDL (>40 mg/dL)", 0, 200, 55, 1)
            triglycerides = st.number_input(
                "Triglycerides (<150 mg/dL)", 0, 1000, 120, 1)
        with col3:
            ratio = total_chol / hdl if hdl > 0 else 0
            st.metric("Chol/HDL Ratio", f"{ratio:.2f}")

    if st.button("🔬 Analyze Lab Results", type="primary"):
        results = []

        # CBC Analysis
        if wbc < 4.5 or wbc > 11.0:
            results.append(
                ("WBC", "Abnormal", "⚠️ Consider infection or immune disorder"))
        if hemoglobin < 12:
            results.append(("Hemoglobin", "Low", "⚠️ Possible anemia"))
        if platelets < 150:
            results.append(("Platelets", "Low", "⚠️ Bleeding risk"))

        # Metabolic
        if glucose > 100:
            results.append(("Glucose", "Elevated", "⚠️ Check for diabetes"))
        if creatinine > 1.3:
            results.append(
                ("Creatinine", "High", "⚠️ Kidney function concern"))

        # Lipids
        if ldl > 100:
            results.append(("LDL", "Elevated", "⚠️ Cardiovascular risk"))
        if triglycerides > 150:
            results.append(
                ("Triglycerides", "High", "⚠️ Metabolic syndrome risk"))

        if results:
            st.markdown("### ⚠️ Abnormal Results")
            for test, status, note in results:
                st.warning(f"**{test}**: {status} - {note}")
        else:
            st.success("✅ All results within normal range!")

        st.info("""
        💡 **Recommendations:**
        - Discuss results with your healthcare provider
        - Consider lifestyle modifications if needed
        - Schedule follow-up tests as recommended
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== HEALTH ANALYTICS ====================
elif page == "📊 Health Analytics":
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Comprehensive Health Analytics")

    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    analytics_data = pd.DataFrame({
        'Date': dates,
        'Weight': 70 + np.cumsum(np.random.randn(90) * 0.1),
        'BP_Systolic': np.random.randint(115, 130, 90),
        'BP_Diastolic': np.random.randint(70, 85, 90),
        'Heart_Rate': np.random.randint(65, 80, 90),
        'Steps': np.random.randint(5000, 15000, 90),
        'Calories': np.random.randint(1800, 2500, 90),
        'Sleep_Hours': np.random.uniform(6, 9, 90)
    })

    tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Statistics", "🎯 Goals"])

    with tab1:
        metric = st.selectbox("Select Metric:",
                              ['Weight', 'BP_Systolic', 'Heart_Rate', 'Steps', 'Sleep_Hours'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=analytics_data['Date'],
            y=analytics_data[metric],
            mode='lines+markers',
            name=metric,
            line=dict(color='#667eea', width=3),
            marker=dict(size=6)
        ))

        fig.update_layout(
            title=f"{metric} Over Time",
            xaxis_title="Date",
            yaxis_title=metric,
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Avg Weight",
                      f"{analytics_data['Weight'].mean():.1f} kg")
            st.metric(
                "Avg BP", f"{analytics_data['BP_Systolic'].mean():.0f}/{analytics_data['BP_Diastolic'].mean():.0f}")

        with col2:
            st.metric("Avg Heart Rate",
                      f"{analytics_data['Heart_Rate'].mean():.0f} bpm")
            st.metric("Avg Steps", f"{analytics_data['Steps'].mean():.0f}")

        with col3:
            st.metric(
                "Avg Sleep", f"{analytics_data['Sleep_Hours'].mean():.1f} hrs")
            st.metric("Avg Calories",
                      f"{analytics_data['Calories'].mean():.0f}")

        # Distribution charts
        fig = make_subplots(rows=1, cols=2, subplot_titles=(
            'Weight Distribution', 'Sleep Distribution'))

        fig.add_trace(go.Histogram(x=analytics_data['Weight'], name='Weight',
                                   marker_color='#667eea'), row=1, col=1)
        fig.add_trace(go.Histogram(x=analytics_data['Sleep_Hours'], name='Sleep',
                                   marker_color='#10b981'), row=1, col=2)

        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### 🎯 Health Goals")

        goal_weight = st.number_input("Target Weight (kg):", value=68.0)
        goal_steps = st.number_input("Daily Steps Goal:", value=10000)
        goal_sleep = st.number_input("Sleep Goal (hours):", value=8.0)

        current_weight = analytics_data['Weight'].iloc[-1]
        current_steps = analytics_data['Steps'].iloc[-1]
        current_sleep = analytics_data['Sleep_Hours'].iloc[-1]

        col1, col2, col3 = st.columns(3)

        with col1:
            weight_progress = min((current_weight / goal_weight) * 100, 100)
            st.progress(weight_progress / 100)
            st.markdown(
                f"**Weight:** {current_weight:.1f} / {goal_weight:.1f} kg")

        with col2:
            steps_progress = min((current_steps / goal_steps) * 100, 100)
            st.progress(steps_progress / 100)
            st.markdown(f"**Steps:** {current_steps} / {goal_steps}")

        with col3:
            sleep_progress = min((current_sleep / goal_sleep) * 100, 100)
            st.progress(sleep_progress / 100)
            st.markdown(
                f"**Sleep:** {current_sleep:.1f} / {goal_sleep:.1f} hrs")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== MEDICAL RECORDS ====================
elif page == "🏥 Medical Records":
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 🏥 Medical Records History")

    if st.session_state.medical_history:
        for idx, record in enumerate(reversed(st.session_state.medical_history)):
            with st.expander(f"📋 {record.get('diagnosis', 'N/A')} - {record.get('date', 'N/A')}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        f"**Diagnosis:** {record.get('diagnosis', 'N/A')}")
                    st.markdown(
                        f"**Symptoms:** {record.get('symptoms', 'N/A')}")
                    st.markdown(
                        f"**Confidence:** {record.get('confidence', 0)}%")

                with col2:
                    st.markdown(
                        f"**Severity:** {record.get('severity', 'N/A')}")
                    st.markdown(
                        f"**Duration:** {record.get('duration', 'N/A')}")
                    st.markdown(
                        f"**Temperature:** {record.get('temperature', 'N/A')}°F")

        # Export functionality
        if st.button("📥 Export All Records"):
            export_data = json.dumps(
                st.session_state.medical_history, indent=2)
            st.download_button(
                "Download JSON",
                export_data,
                file_name=f"medical_records_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    else:
        st.info(
            "No medical records available. Complete a symptom analysis to create records.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== APPOINTMENTS ====================
elif page == "📅 Appointments":
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 📅 Appointment Scheduler")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Schedule New Appointment")

        doctor_name = st.text_input("Doctor Name:")
        specialty = st.selectbox("Specialty:",
                                 ["General Physician", "Cardiologist", "Dermatologist", "Neurologist",
                                  "Orthopedic", "Pediatrician", "Psychiatrist"])

        appt_date = st.date_input("Date:", min_value=datetime.now().date())
        appt_time = st.time_input("Time:")

        reason = st.text_area("Reason for Visit:")

        if st.button("📅 Schedule Appointment"):
            if doctor_name:
                appointment = {
                    "doctor": doctor_name,
                    "specialty": specialty,
                    "date": appt_date.strftime("%Y-%m-%d"),
                    "time": appt_time.strftime("%H:%M"),
                    "reason": reason,
                    "status": "upcoming"
                }
                st.session_state.appointments.append(appointment)
                st.success(f"✅ Appointment scheduled with Dr. {doctor_name}")
            else:
                st.warning("Please enter doctor name")

    with col2:
        st.markdown("#### Upcoming Appointments")

        if st.session_state.appointments:
            for appt in st.session_state.appointments:
                st.markdown(f"""
                <div class='medical-record-card'>
                    <strong>Dr. {appt['doctor']}</strong> - {appt['specialty']}
                    <div style='font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;'>
                        📅 {appt['date']} at {appt['time']}
                    </div>
                    <div style='font-size: 0.85rem; margin-top: 0.5rem;'>
                        {appt.get('reason', 'No reason specified')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appointments scheduled")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== PROFILE SETTINGS ====================
elif page == "👤 Profile Settings":
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 👤 User Profile Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Personal Information")

        name = st.text_input(
            "Full Name:", value=st.session_state.user_profile['name'])
        age = st.number_input(
            "Age:", 1, 120, value=st.session_state.user_profile['age'])
        gender = st.selectbox("Gender:",
                              ["Male", "Female", "Other", "Prefer not to say"],
                              index=0 if st.session_state.user_profile['gender'] == "Not Specified" else 0)

        blood_group = st.selectbox("Blood Group:",
                                   ["A+", "A-", "B+", "B-", "AB+",
                                       "AB-", "O+", "O-", "Unknown"],
                                   index=8 if st.session_state.user_profile['blood_group'] == "Unknown" else 0)

        height = st.number_input("Height (cm):", 100, 250, 170)
        weight = st.number_input("Weight (kg):", 30, 200, 70)

    with col2:
        st.markdown("#### Medical Information")

        allergies = st.text_area("Allergies:",
                                 placeholder="List any allergies (e.g., Penicillin, Peanuts)")

        chronic_conditions = st.text_area("Chronic Conditions:",
                                          placeholder="List chronic conditions (e.g., Diabetes, Hypertension)")

        emergency_contact = st.text_input("Emergency Contact:",
                                          placeholder="Name and phone number")

        insurance = st.text_input("Insurance Provider:")
        insurance_id = st.text_input("Insurance ID:")

    if st.button("💾 Save Profile", type="primary"):
        st.session_state.user_profile.update({
            'name': name,
            'age': age,
            'gender': gender,
            'blood_group': blood_group,
            'height': height,
            'weight': weight,
            'allergies': allergies.split(',') if allergies else [],
            'chronic_conditions': chronic_conditions.split(',') if chronic_conditions else [],
            'emergency_contact': emergency_contact,
            'insurance': insurance,
            'insurance_id': insurance_id
        })
        st.success("✅ Profile updated successfully!")

    # Calculate BMI
    if height > 0 and weight > 0:
        bmi = weight / ((height/100) ** 2)
        st.markdown("---")
        st.markdown("### 📊 Health Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("BMI", f"{bmi:.1f}")

        with col2:
            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            st.metric("Category", category)

        with col3:
            ideal_weight = 22 * ((height/100) ** 2)
            st.metric("Ideal Weight", f"{ideal_weight:.1f} kg")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem; font-size: 0.9rem;'>
    <p>🏥 <strong>MediCare AI Pro</strong> - Advanced Medical Diagnosis & Health Assistant</p>
    <p>⚕️ This application provides AI-assisted medical information for educational purposes only.</p>
    <p>⚠️ Always consult qualified healthcare professionals for medical advice, diagnosis, and treatment.</p>
    <p>© 2025 MediCare AI Pro. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
