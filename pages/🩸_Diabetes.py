import streamlit as st
import joblib
import pandas as pd
from utils.extractor import extract_text
from utils.parser import extract_values
from utils.predictor import predict_diabetes
from utils.diabetes_rules import analyze_diabetes
from utils.diabetes_extractor import extract_diabetes_values
from components.ai_assistant import show_ai_assistant

model = joblib.load("models/diabetes_model.pkl")
feature_order = joblib.load("models/diabetes_feature_order.pkl")


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
    AI Powered Diabetes Prediction
    </div>

    <div class="main-desc">
    Upload your medical report, verify extracted values,
    and receive an AI-powered heart health assessment
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
uploaded_file = st.file_uploader(
    "Upload your medical report (PDF/Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    st.success("Report uploaded successfully!")

    st.progress(0.33)

    st.markdown("""
    <h3 style="color:white;">
    Step 2 of 4 • Review Extracted Values
    </h3>
    """, unsafe_allow_html=True)

    extracted_text = extract_text(uploaded_file)


    values = extract_diabetes_values(extracted_text)
    

    st.markdown("""
    <h1 style="color:white;">
    Review Extracted Values
    </h1>
    """, unsafe_allow_html=True)



    st.markdown("""
    <div style="
    background:#EAF6F6;
    padding:18px;
    border-radius:14px;
    border-left:6px solid #14746F;
    color:#0F4C5C;
    font-size:17px;
    font-weight:500;">
    Please review the extracted values below. Correct any value if OCR made a mistake.
    </div>
    """, unsafe_allow_html=True)

    st.divider()


    
    if "Pregnancies" not in values:
        values["Pregnancies"] = 0

    values["Pregnancies"] = st.number_input(
        "Number of Pregnancies",
        min_value=0,
        max_value=20,
        value=int(values["Pregnancies"])
    )


    
    if "Glucose" not in values:
        values["Glucose"] = 120

    values["Glucose"] = st.number_input(
        "Glucose (mg/dL)",
        min_value=40,
        max_value=400,
        value=int(values["Glucose"])
    )

    if values["Glucose"] <= 0:
        values["Glucose"] = 120



    if "BloodPressure" not in values:
        values["BloodPressure"] = 80

    values["BloodPressure"] = st.number_input(
        "Blood Pressure (mmHg)",
        min_value=40,
        max_value=200,
        value=int(values["BloodPressure"])
    )
    if values["BloodPressure"] <= 0:
        values["BloodPressure"] = 80



    if "SkinThickness" not in values:
        values["SkinThickness"] = 20

    values["SkinThickness"] = st.number_input(
        "Skin Thickness (mm)",
        min_value=0,
        max_value=100,
        value=int(values["SkinThickness"])
    )
    if values["SkinThickness"] < 0:
        values["SkinThickness"] = 20


    
    if "Insulin" not in values:
        values["Insulin"] = 80

    values["Insulin"] = st.number_input(
        "Insulin (μU/mL)",
        min_value=0,
        max_value=900,
        value=int(values["Insulin"])
    )
    if values["Insulin"] < 0:
        values["Insulin"] = 80


    if values["BMI"] <= 0:
        values["BMI"] = round(bmi, 2)

    values["BMI"] = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=70.0,
        value=float(values["BMI"]),
        step=0.1
    )

    if "DiabetesPedigreeFunction" not in values:
        values["DiabetesPedigreeFunction"] = 0.47

    values["DiabetesPedigreeFunction"] = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        max_value=3.0,
        value=float(values["DiabetesPedigreeFunction"]),
        step=0.01
    )
    if values["DiabetesPedigreeFunction"] <= 0:
        values["DiabetesPedigreeFunction"] = 0.47


    
    values["Age"] = age
    

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

    verified = st.checkbox(
        "I have reviewed all extracted values and confirm they are correct."
    )

    predict = st.button(
        "Predict Diabetes",
        use_container_width=True,
        disabled=not verified
    )

    if "diabetes_prediction_done" not in st.session_state:
        st.session_state.diabetes_prediction_done = False

    if predict:
        st.session_state.diabetes_prediction_done = True

    if st.session_state.diabetes_prediction_done:

        values["age"] = age
        values["sex"] = gender

        prediction, probability = predict_diabetes(
            values,
            model,
            feature_order
        )
        st.progress(1.0)

        st.caption("Step 4 of 4 • Analysis Completed")

        diabetes_probability = probability[1] * 100

        analysis = analyze_diabetes(
            prediction,
            diabetes_probability,
            values
        )

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
        margin-bottom:20px;
        ">
        Diabetes Prediction
        </h2>
        """, unsafe_allow_html=True)

        

        patient = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "BMI Category": bmi_category
        }

        chat_analysis = {
            "Module": "Diabetes",
            "Prediction": prediction,
            "Probability": diabetes_probability,
            "Values": values
        }
        
        st.markdown(f"""
        <div style="
        background:#DCEEEE;
        border-left:8px solid #14746F;
        padding:25px;
        border-radius:16px;
        margin-bottom:20px;
        ">

        <h2 style="
        color:#0F4C5C;
        margin:0;
        font-size:36px;
        font-weight:700;
        ">
        {analysis["overall"]}
        </h2>

        <p style="
        color:#516B6B;
        font-size:19px;
        margin-top:12px;
        ">
        {analysis["summary"]}
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.metric(
            "Diabetes Risk Probability",
            f"{diabetes_probability:.2f}%"
        )

        if analysis["health_effects"]:

            st.markdown(
                "<h2 style='color:white;'>Possible Health Effects</h2>",
                unsafe_allow_html=True
            )

            for effect in analysis["health_effects"]:

                st.markdown(
                    f"""
                    <div class="info-card">
                    ⚠ {effect}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if analysis["diet"]:

            st.markdown(
                "<h2 style='color:white;'>Diet Recommendations</h2>",
                unsafe_allow_html=True
            )

            for item in analysis["diet"]:

                st.markdown(
                    f"""
                    <div class="info-card">
                    ✓ {item}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if analysis["lifestyle"]:

            st.markdown(
                "<h2 style='color:white;'>Lifestyle Recommendations</h2>",
                unsafe_allow_html=True
            )

            for item in analysis["lifestyle"]:

                st.markdown(
                    f"""
                    <div class="info-card">
                    ✓ {item}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        if analysis["medical"]:

            st.markdown(
                "<h2 style='color:white;'>Medical Advice</h2>",
                unsafe_allow_html=True
            )

            for item in analysis["medical"]:

                st.markdown(
                    f"""
                    <div class="info-card">
                    🩺 {item}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # show_chatbot(patient, analysis)
        
        st.divider()
        st.info(
            "This prediction is generated by a machine learning model and is not a medical diagnosis. Please consult a qualified healthcare professional."
        )
        st.markdown("</div>", unsafe_allow_html=True)

        context = {

            "module":"Diabetes",

            "prediction":prediction,

            "confidence":probability,

            "glucose":values["Glucose"],

            "bmi":bmi,

            "age":age,

            "diet":analysis["diet"],

            "lifestyle":analysis["lifestyle"],

            "health effects":analysis["health_effects"]
            

        }
        module = context.get("module", "default")

        if (
            "current_module" not in st.session_state
            or st.session_state.current_module != module
        ):
            st.session_state.current_module = module
            st.session_state.assistant_messages = []

        show_ai_assistant(context)

else:
 st.markdown("""
 <div style="
 background:#EAF6F6;
 border-left:6px solid #14746F;
 padding:18px 22px;
 border-radius:14px;
 color:#0F4C5C;
 font-size:18px;
 font-weight:600;
 box-shadow:0 8px 20px rgba(0,0,0,0.12);
 ">
 Please upload a medical report to continue.
 </div>
 """, unsafe_allow_html=True)