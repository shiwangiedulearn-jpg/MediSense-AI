import streamlit as st
import joblib
import pandas as pd
from utils.extractor import extract_text
from utils.predictor import predict_liver_disease
from utils.liver_rules import analyze_liver
from utils.liver_extractor import extract_liver_values
from components.ai_assistant import show_ai_assistant


model = joblib.load("models/liver_model.pkl")
feature_order = joblib.load("models/liver_feature_order.pkl")


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
    AI Powered Liver Disease Prediction
    </div>

    <div class="main-desc">
    Upload your medical report, verify extracted values,
    and receive an AI-powered liver  health assessment
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


    values = extract_liver_values(extracted_text)
    

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


    
    if "tot_bilirubin" not in values:
        values["tot_bilirubin"] = 1.0

    if values["tot_bilirubin"] <= 0:
        values["tot_bilirubin"] = 1.0

    values["tot_bilirubin"] = st.number_input(
        "Total Bilirubin (mg/dL)",
        min_value=0.0,
        max_value=50.0,
        value=float(values["tot_bilirubin"]),
        step=0.1
    )



    if "direct_bilirubin" not in values:
        values["direct_bilirubin"] = 0.2

    if values["direct_bilirubin"] < 0:
        values["direct_bilirubin"] = 0.2

    values["direct_bilirubin"] = st.number_input(
        "Direct Bilirubin (mg/dL)",
        min_value=0.0,
        max_value=25.0,
        value=float(values["direct_bilirubin"]),
        step=0.1
    )



    if "alkphos" not in values:
        values["alkphos"] = 150

    if values["alkphos"] <= 0:
        values["alkphos"] = 150

    values["alkphos"] = st.number_input(
        "Alkaline Phosphatase (IU/L)",
        min_value=20,
        max_value=2500,
        value=int(values["alkphos"])
    )



    if "sgpt" not in values:
        values["sgpt"] = 40

    if values["sgpt"] < 0:
        values["sgpt"] = 40

    values["sgpt"] = st.number_input(
        "SGPT (ALT) (IU/L)",
        min_value=0,
        max_value=3000,
        value=int(values["sgpt"])
    )




    if "sgot" not in values:
        values["sgot"] = 40

    if values["sgot"] < 0:
        values["sgot"] = 40

    values["sgot"] = st.number_input(
        "SGOT (AST) (IU/L)",
        min_value=0,
        max_value=3000,
        value=int(values["sgot"])
    )



    if "tot_proteins" not in values:
        values["tot_proteins"] = 7.0

    if values["tot_proteins"] <= 0:
        values["tot_proteins"] = 7.0

    values["tot_proteins"] = st.number_input(
        "Total Proteins (g/dL)",
        min_value=2.0,
        max_value=15.0,
        value=float(values["tot_proteins"]),
        step=0.1
    )




    if "albumin" not in values:
        values["albumin"] = 4.0

    if values["albumin"] <= 0:
        values["albumin"] = 4.0

    values["albumin"] = st.number_input(
        "Albumin (g/dL)",
        min_value=1.0,
        max_value=10.0,
        value=float(values["albumin"]),
        step=0.1
    )


    if "ag_ratio" not in values:
        values["ag_ratio"] = 1.2

    if values["ag_ratio"] <= 0:
        values["ag_ratio"] = 1.2

    values["ag_ratio"] = st.number_input(
        "Albumin / Globulin Ratio",
        min_value=0.1,
        max_value=5.0,
        value=float(values["ag_ratio"]),
        step=0.01
    )

    
    values["Age"] = age
    values["gender"] = gender
    

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
        "Analyze Liver Disease",
        use_container_width=True,
        disabled=not verified
    )
    if "liver_prediction_done" not in st.session_state:
        st.session_state.liver_prediction_done = False

    if predict:
        st.session_state.liver_prediction_done = True

    if st.session_state.liver_prediction_done:

        values["age"] = age
        values["sex"] = gender

        prediction, probability = predict_liver_disease(
            values,
            model,
            feature_order
        )
        st.progress(1.0)

        st.caption("Step 4 of 4 • Analysis Completed")

        liver_probability = probability[1] * 100

        analysis = analyze_liver(
            prediction,
            liver_probability,
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
        Liver Disease Prediction
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
            "Module": "Liver Disease",
            "Prediction": prediction,
            "Probability": liver_probability,
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
            "Liver Disease Risk Probability",
            f"{liver_probability:.2f}%"
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

            "module":"Liver Disease",

            "prediction":prediction,

            "confidence": probability,

            "patient":patient,

            "health_effects": analysis["health_effects"],
            "diet": analysis["diet"],
            "lifestyle": analysis["lifestyle"],
            "medical_advice": analysis["medical"]

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