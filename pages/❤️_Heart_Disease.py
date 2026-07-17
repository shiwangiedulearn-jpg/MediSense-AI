import streamlit as st
import joblib
import pandas as pd
from utils.extractor import extract_text
from utils.parser import extract_values
from utils.predictor import predict_heart_disease
from components.ai_assistant import show_ai_assistant


model = joblib.load("models/heart_model.pkl")
feature_order = joblib.load("models/feature_order.pkl")


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
    AI Powered Heart Disease Prediction
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

    values = extract_values(extracted_text)

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

    if "chol" in values:
        values["chol"] = st.number_input(
            "Serum Cholesterol (mg/dL)",
            value=float(values["chol"])
        )

    if "trestbps" in values:
        values["trestbps"] = st.number_input(
            "Resting Blood Pressure (mmHg)",
            value=float(values["trestbps"])
        )

    if "restecg" in values:
        restecg_options = [
            "Normal",
            "ST-T Wave Abnormality",
            "Left Ventricular Hypertrophy"
        ]

        restecg = st.selectbox(
            "Resting ECG Result",
            restecg_options,
            index=values["restecg"]
        )

        values["restecg"] = {
            "Normal": 0,
            "ST-T Wave Abnormality": 1,
            "Left Ventricular Hypertrophy": 2
        }[restecg]

    if "thalach" in values:
        values["thalach"] = st.number_input(
            "Maximum Heart Rate (bpm)",
            value=float(values["thalach"])
        )

    if "exang" in values:
        exang = st.selectbox(
            "Exercise Induced Angina",
            ["No", "Yes"],
            index=values["exang"]
        )

        values["exang"] = {
            "No": 0,
            "Yes": 1
        }[exang]

    if "oldpeak" in values:

        if values["oldpeak"] > 7:
            values["oldpeak"] = values["oldpeak"] / 10

        values["oldpeak"] = st.number_input(
            "ST Depression (Oldpeak)",
            value=float(values["oldpeak"])
        )

    if "slope" in values:

        slope_options = [
            "Upsloping",
            "Flat",
            "Downsloping"
        ]

        slope = st.selectbox(
            "Slope of Peak Exercise ST Segment",
            slope_options,
            index=values["slope"]
        )

        values["slope"] = {
            "Upsloping": 0,
            "Flat": 1,
            "Downsloping": 2
        }[slope]

    if "ca" in values:

        values["ca"] = st.selectbox(
            "Number of Major Vessels Colored by Fluoroscopy",
            [0, 1, 2, 3],
            index=values["ca"]
        )

    if "thal" in values:

        thal_options = [
            "Normal",
            "Fixed Defect",
            "Reversible Defect"
        ]

        thal = st.selectbox(
            "Thalassemia",
            thal_options,
            index=values["thal"] - 1
        )

        values["thal"] = {
            "Normal": 1,
            "Fixed Defect": 2,
            "Reversible Defect": 3
        }[thal]

    if "cp" in values:

        cp_options = [
            "Pressure/tightness in the center of the chest (Typical Angina)",
            "Chest pain different from typical angina (Atypical Angina)",
            "Pain not related to the heart (Non-Anginal Pain)",
            "I'm not sure"
        ]

        cp = st.selectbox(
            "Chest Pain Type",
            cp_options,
            index=values["cp"]
        )

        values["cp"] = {
            "Pressure/tightness in the center of the chest (Typical Angina)": 0,
            "Chest pain different from typical angina (Atypical Angina)": 1,
            "Pain not related to the heart (Non-Anginal Pain)": 2,
            "I'm not sure": 3
        }[cp]

    if "cp" not in values:

        has_cp = st.selectbox(
            "Are you experiencing chest pain?",
            ["No", "Yes"]
        )

        if has_cp == "Yes":

            cp = st.selectbox(
                "Which best describes your chest pain?",
                [
                    "Pressure/tightness in the center of the chest (Typical Angina)",
                    "Chest pain different from typical angina (Atypical Angina)",
                    "Pain not related to the heart (Non-Anginal Pain)",
                    "I'm not sure"
                ]
            )

            values["cp"] = {
                "Pressure/tightness in the center of the chest (Typical Angina)": 0,
                "Chest pain different from typical angina (Atypical Angina)": 1,
                "Pain not related to the heart (Non-Anginal Pain)": 2,
                "I'm not sure": 3
            }[cp]

        else:
            values["cp"] = 3

    if "trestbps" not in values:
        values["trestbps"] = st.number_input(
            "Resting Blood Pressure (mmHg)",
            min_value=80,
            max_value=250,
            value=120
        )

    if "chol" not in values:
        values["chol"] = st.number_input(
            "Serum Cholesterol (mg/dL)",
            min_value=100,
            max_value=600,
            value=200
        )

    if "fbs" not in values:

        fbs = st.selectbox(
            "Fasting Blood Sugar >120 mg/dL",
            ["Yes", "No"]
        )

        values["fbs"] = {
            "Yes": 1,
            "No": 0
        }[fbs]

    if "restecg" not in values:

        restecg = st.selectbox(
            "Resting ECG Result",
            [
                "Normal",
                "ST-T Wave Abnormality",
                "Left Ventricular Hypertrophy"
            ]
        )

        values["restecg"] = {
            "Normal": 0,
            "ST-T Wave Abnormality": 1,
            "Left Ventricular Hypertrophy": 2
        }[restecg]

    if "thalach" not in values:
        values["thalach"] = st.number_input(
            "Maximum Heart Rate Achieved",
            min_value=60,
            max_value=220,
            value=150
        )

    if "exang" not in values:

        exang = st.selectbox(
            "Do you experience chest pain during exercise?",
            ["Yes", "No"]
        )

        values["exang"] = {
            "Yes": 1,
            "No": 0
        }[exang]

    if "oldpeak" not in values:
        values["oldpeak"] = st.number_input(
            "ST Depression (Oldpeak)",
            min_value=0.0,
            max_value=7.0,
            value=1.0
        )

    if "slope" not in values:

        slope = st.selectbox(
            "Slope of Peak Exercise ST Segment",
            [
                "Upsloping",
                "Flat",
                "Downsloping"
            ]
        )

        values["slope"] = {
            "Upsloping": 0,
            "Flat": 1,
            "Downsloping": 2
        }[slope]

    if "ca" not in values:

        ca = st.selectbox(
            "Number of Major Vessels Colored by Fluoroscopy",
            [0, 1, 2, 3]
        )

        values["ca"] = ca

    if "thal" not in values:

        thal = st.selectbox(
            "Thalassemia",
            [
                "Normal",
                "Fixed Defect",
                "Reversible Defect"
            ]
        )

        values["thal"] = {
            "Normal": 1,
            "Fixed Defect": 2,
            "Reversible Defect": 3
        }[thal]

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
        "Predict Heart Disease",
        use_container_width=True,
        disabled=not verified
    )

    if "heart_prediction_done" not in st.session_state:
        st.session_state.heart_prediction_done = False

    if predict:
        st.session_state.heart_prediction_done = True

    if st.session_state.heart_prediction_done:

        values["age"] = age
        values["sex"] = gender

        prediction, probability = predict_heart_disease(
            values,
            model,
            feature_order
        )
        st.progress(1.0)

        st.caption("Step 4 of 4 • Analysis Completed")

        heart_probability = probability[1] * 100

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
        Heart Disease Prediction
        </h2>
        """, unsafe_allow_html=True)

        if heart_probability < 30:
            st.markdown("""
            <div style="
            background:#E8F5E9;
            border-left:8px solid #2E7D32;
            padding:18px 22px;
            border-radius:12px;
            margin-bottom:20px;
            ">
            <h3 style="color:#2E7D32;margin:0;font-weight:700;">
            Low Risk of Heart Disease
            </h3>
            </div>
            """, unsafe_allow_html=True)
        elif heart_probability < 70:
            st.markdown("""
            <div style="
            background:#FB8C00;
            padding:22px 28px;
            border-radius:14px;
            margin-bottom:20px;
            ">
            <div style="
            color:white;
            font-size:38px;
            font-weight:700;
            ">
            Medium Risk of Heart Disease
            </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
            background:red;
            padding:22px;
            border-radius:14px;
            margin-bottom:20px;
            ">
            <span style="
            color:white;
            font-size:40px;
            font-weight:bold;
            ">
            High Risk of Heart Disease
            </span>

            </div>
            """, unsafe_allow_html=True)
        st.metric(
            "Heart Disease Risk Probability",
            f"{heart_probability:.2f}%"
        )
        st.markdown("""
        <h2 style="
        color:#F8FAFC;
        font-size:36px;
        font-weight:700;
        margin-top:35px;
        margin-bottom:20px;
        ">
        Possible Contributing Factors
        </h2>
        """, unsafe_allow_html=True)

        if values["chol"] > 240:
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• High Cholesterol Level.</p>",
          unsafe_allow_html=True
)
        if values["trestbps"] > 140:
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Elevated resting blood pressure.</p>",
                unsafe_allow_html=True
                )
        if values["fbs"] == 1:
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Elevated fasting blood sugar level.</p>",
                unsafe_allow_html=True
                )
        if values["oldpeak"] > 2:
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Abnormal ST depression (Oldpeak).</p>",
                unsafe_allow_html=True
                )
        if values["exang"] == 1:
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Exercise-induced angina present.</p>",
               unsafe_allow_html=True
           )
        if bmi >= 25:
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• BMI indicates Overweight or Obesity.</p>",
                unsafe_allow_html=True
            )


        if heart_probability >= 70:

            st.error("Consult a cardiologist as soon as possible.")

            if values["chol"] > 240:
                st.markdown(
                    "<p style='color:#F8FAFC;font-size:18px;'>• Reduce fried and fatty foods.</p>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    "<p style='color:#F8FAFC;font-size:18px;'>• Increase fibre-rich foods.</p>",
                    unsafe_allow_html=True
                )

            if values["trestbps"] > 140:
                st.markdown(
                    "<p style='color:#F8FAFC;font-size:18px;'>• Reduce salt intake.</p>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    "<p style='color:#F8FAFC;font-size:18px;'>• Monitor blood pressure regularly.</p>",
                    unsafe_allow_html=True
                )

            if values["fbs"] == 1:
                st.markdown(
                    "<p style='color:#F8FAFC;font-size:18px;'>• Control blood sugar through diet and exercise.</p>",
                    unsafe_allow_html=True
                )

            if bmi >= 25:
                st.markdown(
                    "<p style='color:#F8FAFC;font-size:18px;'>• Engage in regular physical activity.</p>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    "<p style='color:#F8FAFC;font-size:18px;'>• Follow a balanced diet to manage weight.</p>",
                    unsafe_allow_html=True
                )

            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Avoid smoking and excessive alcohol.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Exercise only after medical advice.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Take prescribed medicines regularly.</p>",
                unsafe_allow_html=True
            )

        elif heart_probability >= 30:

            st.warning("Schedule a routine consultation with a healthcare professional.")

            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Exercise regularly.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Eat a balanced diet.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Maintain a healthy weight.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Reduce stress.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Get regular health check-ups.</p>",
                unsafe_allow_html=True
            )

        else:

            st.success("Continue maintaining a healthy lifestyle.")

            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Eat a balanced diet.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Exercise regularly.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Get adequate sleep.</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color:#F8FAFC;font-size:18px;'>• Continue regular health screenings.</p>",
                unsafe_allow_html=True
            )
        
        st.markdown("<br><br>")

        patient = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "BMI Category": bmi_category
        }

        analysis = {
            "Module": "Heart Disease",
            "Prediction": prediction,
            "Probability": heart_probability,
            "Values": values
        }
        
        

        st.info(
            "This prediction is generated by a machine learning model and is not a medical diagnosis. Please consult a qualified healthcare professional."
        )
        st.markdown("</div>", unsafe_allow_html=True)

        context = {

            "module":"Heart Disease",

            "prediction":prediction,

            "confidence":probability,

            "age":age,

            "gender":gender,


            "cholesterol":values["chol"],

            "heart_rate":values["thalach"],

            "ecg":values["restecg"],


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