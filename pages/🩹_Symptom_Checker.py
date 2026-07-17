import streamlit as st
import joblib
import pandas as pd
import numpy as np
from utils.predictor import predict_symptom_disease
from utils.symptom_rules import analyze_symptom
from components.ai_assistant import show_ai_assistant
from components.ai_assistant import show_ai_assistant


model = joblib.load("models/symptom_model.pkl")
feature_order = joblib.load("models/symptom_feature_order.pkl")
symptom_mapping = {

    # =========================
    # General Symptoms
    # =========================
    "Itching": "itching",
    "Skin Rash": "skin_rash",
    "Skin Lumps or Eruptions": "nodal_skin_eruptions",
    "Continuous Sneezing": "continuous_sneezing",
    "Shivering": "shivering",
    "Chills": "chills",
    "Fatigue": "fatigue",
    "Weight Gain": "weight_gain",
    "Weight Loss": "weight_loss",
    "Anxiety": "anxiety",
    "Cold Hands and Feet": "cold_hands_and_feets",
    "Mood Swings": "mood_swings",
    "Restlessness": "restlessness",
    "Lethargy": "lethargy",
    "High Fever": "high_fever",
    "Mild Fever": "mild_fever",
    "Sweating": "sweating",
    "Dehydration": "dehydration",
    "Generally Feeling Unwell": "malaise",

    # =========================
    # Head & Nervous System
    # =========================
    "Headache": "headache",
    "Pain Behind the Eyes": "pain_behind_the_eyes",
    "Dizziness": "dizziness",
    "Spinning Sensation": "spinning_movements",
    "Loss of Balance": "loss_of_balance",
    "Unsteadiness": "unsteadiness",
    "Confusion or Unusual Behaviour": "altered_sensorium",
    "Slurred Speech": "slurred_speech",
    "Weakness on One Side of the Body": "weakness_of_one_body_side",
    "Weakness in Arms or Legs": "weakness_in_limbs",
    "Lack of Concentration": "lack_of_concentration",
    "Coma": "coma",

    # =========================
    # Nose, Ear & Throat
    # =========================
    "Runny Nose": "runny_nose",
    "Nasal Congestion": "congestion",
    "Sinus Pressure": "sinus_pressure",
    "Throat Irritation": "throat_irritation",
    "Patches in the Throat": "patches_in_throat",
    "Ulcers on the Tongue": "ulcers_on_tongue",
    "Cough": "cough",
    "Phlegm": "phlegm",
    "Mucus in Cough": "mucoid_sputum",
    "Rust-Coloured Sputum": "rusty_sputum",
    "Blood in Sputum": "blood_in_sputum",
    "Loss of Smell": "loss_of_smell",
    "Red Sore Around the Nose": "red_sore_around_nose",

    # =========================
    # Chest & Breathing
    # =========================
    "Difficulty Breathing": "breathlessness",
    "Chest Pain": "chest_pain",
    "Fast Heart Rate": "fast_heart_rate",
    "Palpitations": "palpitations",

    # =========================
    # Stomach & Digestion
    # =========================
    "Stomach Pain": "stomach_pain",
    "Abdominal Pain": "abdominal_pain",
    "Belly Pain": "belly_pain",
    "Acidity": "acidity",
    "Indigestion": "indigestion",
    "Nausea": "nausea",
    "Vomiting": "vomiting",
    "Loss of Appetite": "loss_of_appetite",
    "Increased Appetite": "increased_appetite",
    "Excessive Hunger": "excessive_hunger",
    "Diarrhoea": "diarrhoea",
    "Constipation": "constipation",
    "Passing Excess Gas": "passage_of_gases",
    "Swollen Stomach": "swelling_of_stomach",
    "Distended Abdomen": "distention_of_abdomen",
    "Stomach Bleeding": "stomach_bleeding",

    # =========================
    # Urinary Problems
    # =========================
    "Burning While Urinating": "burning_micturition",
    "Blood Spots While Urinating": "spotting_ urination",
    "Bladder Discomfort": "bladder_discomfort",
    "Bad-Smelling Urine": "foul_smell_of urine",
    "Feeling the Need to Urinate Again": "continuous_feel_of_urine",
    "Dark Urine": "dark_urine",
    "Yellow Urine": "yellow_urine",
    "Frequent Urination": "polyuria",

    # =========================
    # Skin & Hair
    # =========================
    "Yellowing of the Skin": "yellowish_skin",
    "Red Spots on the Body": "red_spots_over_body",
    "Pus-filled Pimples": "pus_filled_pimples",
    "Blackheads": "blackheads",
    "Scarring": "scurring",
    "Skin Peeling": "skin_peeling",
    "Silver-like Skin Scaling": "silver_like_dusting",
    "Blisters": "blister",
    "Yellow Crusts on Skin": "yellow_crust_ooze",
    "Discoloured Skin Patches": "dischromic _patches",
    "Internal Itching": "internal_itching",

    # =========================
    # Bones, Muscles & Joints
    # =========================
    "Joint Pain": "joint_pain",
    "Knee Pain": "knee_pain",
    "Hip Joint Pain": "hip_joint_pain",
    "Neck Pain": "neck_pain",
    "Back Pain": "back_pain",
    "Muscle Pain": "muscle_pain",
    "Muscle Weakness": "muscle_weakness",
    "Muscle Wasting": "muscle_wasting",
    "Swollen Joints": "swelling_joints",
    "Joint Stiffness": "movement_stiffness",
    "Stiff Neck": "stiff_neck",
    "Pain While Walking": "painful_walking",
    "Cramps": "cramps",

    # =========================
    # Heart & Blood
    # =========================
    "Swollen Legs": "swollen_legs",
    "Swollen Blood Vessels": "swollen_blood_vessels",
    "Prominent Veins in the Calf": "prominent_veins_on_calf",
    "Puffy Face and Eyes": "puffy_face_and_eyes",
    "Swollen Hands or Feet": "swollen_extremeties",
    "Bruising": "bruising",

    # =========================
    # Eye Problems
    # =========================
    "Sunken Eyes": "sunken_eyes",
    "Yellowing of the Eyes": "yellowing_of_eyes",
    "Red Eyes": "redness_of_eyes",
    "Watery Eyes": "watering_from_eyes",
    "Blurred or Distorted Vision": "blurred_and_distorted_vision",
    "Visual Disturbances": "visual_disturbances",

    # =========================
    # Additional Information (Optional)
    # =========================
    "Irregular Blood Sugar": "irregular_sugar_level",
    "Enlarged Thyroid": "enlarged_thyroid",
    "Brittle Nails": "brittle_nails",
    "Small Dents in Nails": "small_dents_in_nails",
    "Inflamed Nails": "inflammatory_nails",
    "Family History of Similar Illness": "family_history",
    "History of Alcohol Consumption": "history_of_alcohol_consumption",
    "Receiving Blood Transfusion": "receiving_blood_transfusion",
    "Receiving Unsterile Injections": "receiving_unsterile_injections",
    "Multiple Sexual Partners": "extra_marital_contacts",
    "Abnormal Menstrual Bleeding": "abnormal_menstruation",
    "Acute Liver Failure": "acute_liver_failure",
    "Very Ill Appearance": "toxic_look_(typhos)"
}


st.markdown("""
<style>
.stTextInput,
.stNumberInput,
.stSelectbox,
.stFileUploader{
    background:#DCEEEE;
    padding:15px;
    border-radius:15px;
    border:1px solid #B8D9D8;
    margin-bottom:18px;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label{
    color:#0F4C5C;
    font-weight:600;
}

.stApp{
    background:linear-gradient(
        135deg,
        #0A2D35 0%,
        #114B5F 45%,
        #0F4C5C 100%
    );
}

.main-card{
    color:#0F4C5C !important;
    background:#DCEEEE;
    border-top:6px solid #14746F;
    border-radius:22px;
    padding:40px;
    box-shadow:0 12px 30px rgba(15,76,92,.15);
    margin-bottom:35px;
}

.main-title{
    font-size:54px;
    color:#0F4C5C !important;
    font-weight:700;
    margin-bottom:8px;
}

.main-subtitle{
    font-size:20px;
    font-size:22px;
    line-height:1.7;
    margin-bottom:40px;
}

.section-title{
    font-size:34px;
    color:#0F4C5C !important;
    font-size:42px;
    font-weight:700;
    margin-bottom:25px;
}

.section-title{
    color:#0F4C5C;
    font-size:28px;
    font-weight:600;
}

div.stButton > button{
    background:#14746F;
    color:white;
    border:none;
    border-radius:12px;
    height:52px;
    font-size:18px;
    font-weight:600;
}

div.stButton > button:hover{
    background:#0F5C59;

}
.main-card{
    background:#DCEEEE;
    border-top:6px solid #14746F;
    border-radius:24px;
    padding:45px;
    margin-bottom:40px;
    box-shadow:0 12px 30px rgba(0,0,0,.12);
}

.main-title{
    font-size:58px;
    font-weight:700;
    color:#0F4C5C;
    margin-bottom:8px;
}

.main-subtitle{
    font-size:30px;
    font-weight:600;
    color:#2E5663;
    margin-bottom:12px;
}

.main-desc{
    font-size:18px;
    color:#516B6B;
    line-height:1.8;
    margin-bottom:35px;
}

.section-title{
    font-size:34px;
    font-weight:700;
    color:#0F4C5C;
    margin-bottom:20px;
}


[data-testid="stMetricLabel"]{
    color:#D6ECEB !important;
    font-size:18px !important;
}

[data-testid="stMetricValue"]{
    color:white !important;
    font-size:42px !important;
    font-weight:700 !important;
}

div[data-testid="stAlert"]{
    background:#EAF6F6 !important;
    color:#0F4C5C !important;
    border-left:6px solid #2BB673 !important;
    border-radius:14px !important;
    border:none !important;
}

div[data-testid="stAlert"] *{
    color:#0F4C5C !important;
    font-weight:600 !important;
}

.stProgress > div > div{
    background:#14746F !important;
}

.main-card h1{
    color:#0F4C5C;
}

.main-card h2{
    color:#1E4E5F;
}

.main-card h3{
    color:#365F6D;
}

.stInfo{
    background:#EAF6F6 !important;
    color:#0F4C5C !important;
    border-left:6px solid #14746F !important;
}

.stInfo *{
    color:#0F4C5C !important;
}

/* Verification checkbox text */
.stCheckbox label,
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] p{
    color:#F5F8FA !important;
    font-size:18px !important;
    font-weight:500 !important;
}

/* Disabled button */
div.stButton > button:disabled{
    background:#5F7E88 !important;
    color:#EAF6F6 !important;
    border:none !important;
    opacity:0.8 !important;
}

/* Enabled button */
div.stButton > button{
    background:#14746F !important;
    color:white !important;
    font-weight:700 !important;
}

div.stButton > button:hover{
    background:#0F5C59 !important;
}


[data-testid="stCaptionContainer"]{
    color:#CFE8E8 !important;
}

[data-testid="stCaptionContainer"] p{
    color:#CFE8E8 !important;
}

[data-testid="stMetricValue"]{
    color:white !important;
    font-weight:700;
}

[data-testid="stMetricLabel"]{
    color:#CFE8E8 !important;
}

.recommendation-card{
    background:#DCEEEE;
    color:#0F4C5C;
    border-left:6px solid #14746F;
    border-radius:16px;
    padding:20px;
    font-size:20px;
    font-weight:600;
}


.dark-text{
    color:#EAF6F6 !important;
}

.dark-text p,
.dark-text li,
.dark-text span,
.dark-text h2,
.dark-text h3{
    color:#EAF6F6 !important;
}

.info-card{
    background:#DDEFE7;
    color:#0B4F6C;
    padding:14px 18px;
    border-radius:12px;
    margin-bottom:12px;
    font-size:18px;
    font-weight:500;
    border-left:6px solid #2A9D8F;

}

/* Selected symptom chips */

.stMultiSelect [data-baseweb="tag"]{
    background:#DCEEEE !important;
    color:#0F4C5C !important;
    border:2px solid #2EC4B6 !important;
    border-radius:8px !important;
}

.stMultiSelect [data-baseweb="tag"] span{
    color:#0F4C5C !important;
    font-weight:600;
}

.stMultiSelect [data-baseweb="tag"] svg{
    color:#0F4C5C !important;
}
/* Multiselect label */

.stMultiSelect label p{
    color:white !important;
    font-size:18px !important;
    font-weight:700 !important;
}
/* Expander */

.stExpander{
    border-radius:14px !important;
    overflow:hidden;
    margin-bottom:14px;
}

/* Header */

.stExpander details summary{
    background:#1E5A6D;
    border-radius:12px;
    padding:18px 20px !important;
}

/* Actual text */

.stExpander details summary p{
    font-size:28px !important;
    font-weight:800 !important;
    color:white !important;
    margin:0 !important;
    line-height:1.4;
}

/* Arrow */

.stExpander details summary svg{
    width:22px !important;
    height:22px !important;
    color:#2EC4B6 !important;
}

/* Hover */

.stExpander details summary:hover{
    background:#27697E;
}
/* User & assistant messages after sending */
.chatbot-container [data-testid="stChatMessage"] * {
    color: white !important;
}

/* Input box while typing */
.chatbot-container textarea {
    color: #222222 !important;
}

/* Placeholder */
.chatbot-container textarea::placeholder {
    color: #888888 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-card">

    <div class="main-title">
    MediSense AI
    </div>

    <div class="main-subtitle">
    AI Powered Symptom Based Disease Prediction
    </div>

    <div class="main-desc">
    Tell the symptoms you are facing
    and receive an AI-powered overall health assessment
    with personalized recommendations.
    </div>

    <div class="section-title">
    Patient Information
    </div>
     """, unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:

        name = st.text_input("Name")

        gender_text = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )
        gender = 1 if gender_text == "Male" else 0

        height = st.number_input(
            "Height (cm)",
            50,
            250,
            170
        )

with col2:

        age = st.number_input(
            "Age",
            1,
            120,
            30
        )

        weight = st.number_input(
            "Weight (kg)",
            10,
            250,
            70
        )

bmi = weight / ((height / 100) ** 2)

if bmi < 18.5:
        bmi_category = "Underweight"
elif bmi>=18.5 and bmi < 25:
        bmi_category = "Normal"
elif bmi>=25 and bmi < 30:
        bmi_category = "Overweight"
else:
        bmi_category = "Obese"

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="margin-top:15px;">
        <div style="color:#D6ECEB;font-size:18px;">BMI</div>
        <div style="color:white;font-size:48px;font-weight:700;">
            {bmi:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="margin-top:15px;">
        <div style="color:#D6ECEB;font-size:18px;">BMI Category</div>
        <div style="color:white;font-size:48px;font-weight:700;">
            {bmi_category}
        </div>
    </div>
    """, unsafe_allow_html=True)
# Initialize all symptom values
values = {feature: 0 for feature in feature_order}

st.markdown("""
<h2 style="
color:#EAF6F6;
font-size:34px;
font-weight:700;
margin-top:20px;
margin-bottom:15px;">
Select Your Symptoms
</h2>
""", unsafe_allow_html=True)

st.info("Select all symptoms you are currently experiencing. Leave unselected if you don't have them.")

with st.expander("🤒 General Symptoms", expanded=True):

    general = st.multiselect(
        "Choose all that apply",
        [
            "Itching",
            "Skin Rash",
            "Skin Lumps or Eruptions",
            "Continuous Sneezing",
            "Shivering",
            "Chills",
            "Fatigue",
            "Weight Gain",
            "Weight Loss",
            "Anxiety",
            "Cold Hands and Feet",
            "Mood Swings",
            "Restlessness",
            "Lethargy",
            "High Fever",
            "Mild Fever",
            "Sweating",
            "Dehydration",
            "Generally Feeling Unwell"
        ],
        key="general"
    )

    for symptom in general:
        values[symptom_mapping[symptom]] = 1

with st.expander("🤕 Head & Nervous System"):

    head = st.multiselect(
        "Choose all that apply",
        [
            "Headache",
            "Pain Behind the Eyes",
            "Dizziness",
            "Spinning Sensation",
            "Loss of Balance",
            "Unsteadiness",
            "Confusion or Unusual Behaviour",
            "Slurred Speech",
            "Weakness on One Side of the Body",
            "Weakness in Arms or Legs",
            "Lack of Concentration",
            "Coma"
        ],
        key="head"
    )

    for symptom in head:
        values[symptom_mapping[symptom]] = 1

with st.expander("👃 Nose, Ear & Throat"):

    ent = st.multiselect(
        "Choose all that apply",
        [
            "Runny Nose",
            "Nasal Congestion",
            "Sinus Pressure",
            "Throat Irritation",
            "Patches in the Throat",
            "Ulcers on the Tongue",
            "Cough",
            "Phlegm",
            "Mucus in Cough",
            "Rust-Coloured Sputum",
            "Blood in Sputum",
            "Loss of Smell",
            "Red Sore Around the Nose"
        ],
        key="ent"
    )

    for symptom in ent:
        values[symptom_mapping[symptom]] = 1

with st.expander("🫁 Chest & Breathing"):

    chest = st.multiselect(
        "Choose all that apply",
        [
            "Difficulty Breathing",
            "Chest Pain",
            "Fast Heart Rate",
            "Palpitations"
        ],
        key="chest"
    )

    for symptom in chest:
        values[symptom_mapping[symptom]] = 1

with st.expander("🍽️ Stomach & Digestion"):

    stomach = st.multiselect(
        "Choose all that apply",
        [
            "Stomach Pain",
            "Abdominal Pain",
            "Belly Pain",
            "Acidity",
            "Indigestion",
            "Nausea",
            "Vomiting",
            "Loss of Appetite",
            "Increased Appetite",
            "Excessive Hunger",
            "Diarrhoea",
            "Constipation",
            "Passing Excess Gas",
            "Swollen Stomach",
            "Distended Abdomen",
            "Stomach Bleeding"
        ],
        key="stomach"
    )

    for symptom in stomach:
        values[symptom_mapping[symptom]] = 1

with st.expander("🚽 Urinary Problems"):

    urinary = st.multiselect(
        "Choose all that apply",
        [
            "Burning While Urinating",
            "Blood Spots While Urinating",
            "Bladder Discomfort",
            "Bad-Smelling Urine",
            "Feeling the Need to Urinate Again",
            "Dark Urine",
            "Yellow Urine",
            "Frequent Urination"
        ],
        key="urinary"
    )

    for symptom in urinary:
        values[symptom_mapping[symptom]] = 1

with st.expander("🩹 Skin & Hair"):

    skin = st.multiselect(
        "Choose all that apply",
        [
            "Yellowing of the Skin",
            "Red Spots on the Body",
            "Pus-filled Pimples",
            "Blackheads",
            "Scarring",
            "Skin Peeling",
            "Silver-like Skin Scaling",
            "Blisters",
            "Yellow Crusts on Skin",
            "Discoloured Skin Patches",
            "Internal Itching"
        ],
        key="skin"
    )

    for symptom in skin:
        values[symptom_mapping[symptom]] = 1

with st.expander("🦴 Bones, Muscles & Joints"):

    bones = st.multiselect(
        "Choose all that apply",
        [
            "Joint Pain",
            "Knee Pain",
            "Hip Joint Pain",
            "Neck Pain",
            "Back Pain",
            "Muscle Pain",
            "Muscle Weakness",
            "Muscle Wasting",
            "Swollen Joints",
            "Joint Stiffness",
            "Stiff Neck",
            "Pain While Walking",
            "Cramps"
        ],
        key="bones"
    )

    for symptom in bones:
        values[symptom_mapping[symptom]] = 1

with st.expander("❤️ Heart & Blood"):

    heart = st.multiselect(
        "Choose all that apply",
        [
            "Swollen Legs",
            "Swollen Blood Vessels",
            "Prominent Veins in the Calf",
            "Puffy Face and Eyes",
            "Swollen Hands or Feet",
            "Bruising"
        ],
        key="heart"
    )

    for symptom in heart:
        values[symptom_mapping[symptom]] = 1

with st.expander("👁️ Eye Problems"):

    eyes = st.multiselect(
        "Choose all that apply",
        [
            "Sunken Eyes",
            "Yellowing of the Eyes",
            "Red Eyes",
            "Watery Eyes",
            "Blurred or Distorted Vision",
            "Visual Disturbances"
        ],
        key="eyes"
    )

    for symptom in eyes:
        values[symptom_mapping[symptom]] = 1

with st.expander("📋 Additional Information (Optional)"):

    other = st.multiselect(
        "Select only if applicable",
        [
            "Irregular Blood Sugar",
            "Enlarged Thyroid",
            "Brittle Nails",
            "Small Dents in Nails",
            "Inflamed Nails",
            "Family History of Similar Illness",
            "History of Alcohol Consumption",
            "Receiving Blood Transfusion",
            "Receiving Unsterile Injections",
            "Multiple Sexual Partners",
            "Abnormal Menstrual Bleeding",
            "Acute Liver Failure",
            "Very Ill Appearance"
        ],
        key="other"
    )

    for symptom in other:
        values[symptom_mapping[symptom]] = 1

st.divider()

st.markdown("""
<h2 style="
color:#EAF6F6;
font-size:34px;
font-weight:700;
margin-top:20px;
margin-bottom:10px;">
Verification
</h2>
""", unsafe_allow_html=True)

selected_count = sum(values.values())
selected_symptoms = (
    general +
    head +
    ent +
    chest +
    stomach +
    urinary +
    skin +
    bones +
    heart +
    eyes +
    other
)
st.markdown(
    f"<h2 style='color:white;'>Selected Symptoms ({len(selected_symptoms)})</h2>",
    unsafe_allow_html=True
)
if selected_count == 0:
    st.warning("Please select at least one symptom before continuing.")

verified = st.checkbox(
    "I have selected all the symptoms that I am currently experiencing."
)


predict = st.button(
    "Predict Disease",
    use_container_width=True
)

if "symptom_prediction_done" not in st.session_state:
    st.session_state.symptom_prediction_done = False

if predict:
    st.session_state.symptom_prediction_done = True

if st.session_state.symptom_prediction_done:

    prediction, probability = predict_symptom_disease(
        values,
        model,
        feature_order
    )

    confidence = max(probability) * 100

    analysis = analyze_symptom(
        prediction,
        confidence,
        values
    )

    st.progress(1.0)

    st.caption("Analysis Completed")

    st.markdown('<div class="dark-text">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"""
        <p style="color:#F8FAFC;font-size:20px;">
        <b>Name:</b> {name}
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="color:#F8FAFC;font-size:20px;">
        <b>Age:</b> {age} years
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="color:#F8FAFC;font-size:20px;">
        <b>Gender:</b> {gender_text}
        </p>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <p style="color:#F8FAFC;font-size:20px;">
        <b>Height:</b> {height} cm
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="color:#F8FAFC;font-size:20px;">
        <b>Weight:</b> {weight} kg
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="color:#F8FAFC;font-size:20px;">
        <b>BMI:</b> {bmi:.2f} kg/m²
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style="color:#F8FAFC;font-size:20px;">
        <b>BMI Category:</b> {bmi_category}
        </p>
        """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style="
    color:#F8FAFC;
    font-size:40px;
    font-weight:700;
    margin-top:30px;
    margin-bottom:20px;">
    Symptom Analysis
    </h2>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
    background:#DCEEEE;
    border-left:8px solid #14746F;
    padding:25px;
    border-radius:16px;
    margin-bottom:20px;">

    <h2 style="
    color:#0F4C5C;
    margin:0;
    font-size:36px;
    font-weight:700;">
    {prediction}
    </h2>

    <p style="
    color:#516B6B;
    font-size:19px;
    margin-top:12px;">
    {analysis["summary"]}
    </p>

    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
    <h3 style="margin:0;">Prediction Confidence</h3>
    <p style="font-size:32px;font-weight:bold;color:#14746F;">
    {confidence:.2f}%
    </p>
    </div>
    """, unsafe_allow_html=True)

    top3 = np.argsort(probability)[::-1][:3]

    st.markdown(
        "<h2 style='color:white;'>Selected Symptoms</h2>",
        unsafe_allow_html=True
    )

    symptom_html = ""

    for symptom in selected_symptoms:
        symptom_html += f"""
        <span style="
        display:inline-block;
        background:#DCEEEE;
        color:#0F4C5C;
        border:2px solid #2EC4B6;
        border-radius:20px;
        padding:8px 16px;
        margin:6px;
        font-size:16px;
        font-weight:600;">
        {symptom}
        </span>
        """

    st.markdown(symptom_html, unsafe_allow_html=True)

    st.markdown(
        "<h2 style='color:white;'>Top 3 Possible Diseases</h2>",
        unsafe_allow_html=True
    )

    for i in top3:

        disease = model.classes_[i]
        prob = probability[i] * 100

        st.markdown(f"""
        <div class="info-card">
        <b>{disease}</b> — {prob:.2f}%
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<h2 style='color:white;'>Possible Health Effects</h2>",
        unsafe_allow_html=True
    )

    for item in analysis["health_effects"]:
        st.markdown(
            f"<div class='info-card'>• {item}</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<h2 style='color:white;'>Diet Recommendations</h2>",
        unsafe_allow_html=True
    )

    for item in analysis["diet"]:
        st.markdown(
            f"<div class='info-card'>🥗 {item}</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<h2 style='color:white;'>Lifestyle Recommendations</h2>",
        unsafe_allow_html=True
    )

    for item in analysis["lifestyle"]:
        st.markdown(
            f"<div class='info-card'>🏃 {item}</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<h2 style='color:white;'>Medical Advice</h2>",
        unsafe_allow_html=True
    )

    for item in analysis["medical"]:
        st.markdown(
            f"<div class='info-card'>💊 {item}</div>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div style="
    background:#FFF8E6;
    border-left:8px solid #F4A261;
    padding:20px;
    border-radius:15px;
    margin-top:25px;">

    <h3 style="color:#8B5E00;">⚠ Disclaimer</h3>

    <p style="color:#444;font-size:16px;">

    This prediction is generated using an AI model and is intended for
    educational and informational purposes only.

    It is <b>not a substitute for professional medical diagnosis,
    treatment, or advice.</b>

    Always consult a qualified healthcare professional for proper evaluation.

    </p>

    </div>
    """, unsafe_allow_html=True)
    top3_names = [
        f"{model.classes_[i]} ({probability[i] * 100:.2f}%)"
        for i in top3
    ]

    context = f"""
    Patient Details

    Name: {name}
    Age: {age}
    Gender: {gender}

    Prediction: {prediction}
    Confidence: {confidence:.2f}%

    Selected Symptoms:
    {", ".join(selected_symptoms)}

    Top 3 Possible Diseases:
    {chr(10).join(top3_names)}

    Possible Health Effects:
    {chr(10).join(analysis["health_effects"])}

    Diet Recommendations:
    {chr(10).join(analysis["diet"])}

    Lifestyle Recommendations:
    {chr(10).join(analysis["lifestyle"])}

    Medical Advice:
    {chr(10).join(analysis["medical"])}
    """

    show_ai_assistant(context)