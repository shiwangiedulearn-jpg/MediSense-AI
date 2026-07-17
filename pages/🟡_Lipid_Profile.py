import streamlit as st
import joblib
import pandas as pd
from utils.extractor import extract_text
from utils.lipid_rules import analyze_lipid_profile
from utils.lipid_extractor import extract_lipid_values
from components.ai_assistant import show_ai_assistant

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

.lipid-table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}

.lipid-table th{
    color:white;
    font-size:20px;
    padding:14px;
    text-align:left;
    border-bottom:2px solid rgba(255,255,255,.15);
}

.lipid-table td{
    color:white;
    font-size:18px;
    padding:16px 14px;
    border-bottom:1px solid rgba(255,255,255,.08);

}

.pill{
    display:inline-block;
    min-width:110px;
    text-align:center;
    padding:8px 18px;
    border-radius:999px;
    font-weight:700;
}

.healthy{
    background:#DDF7E3;
    color:#1B5E20;
}

.borderline{
    background:#FFF3CD;
    color:#856404;
}

.high{
    background:#FDE2E2;
    color:#C62828;
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
    Lipid Profile Analysis
    </div>

    <div class="main-desc">
    Upload your medical report, verify extracted values,
    and receive an AI-powered lipid profile assessment
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

    values = extract_lipid_values(extracted_text)

    with st.expander("Extracted Lipid Values", expanded=True):

        st.markdown("""
        <h3 style="color:white;">
        Review Extracted Values
        </h3>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            values["total_cholesterol"] = st.number_input(
                "Total Cholesterol (mg/dL)",
                value=float(values["total_cholesterol"])
            )

            values["ldl"] = st.number_input(
                "LDL Cholesterol (mg/dL)",
                value=float(values["ldl"])
            )

            values["vldl"] = st.number_input(
                "VLDL Cholesterol (mg/dL)",
                value=float(values["vldl"])
            )

        with col2:

            values["hdl"] = st.number_input(
                "HDL Cholesterol (mg/dL)",
                value=float(values["hdl"])
            )

            values["triglycerides"] = st.number_input(
                "Triglycerides (mg/dL)",
                value=float(values["triglycerides"])
            )

            values["total_lipids"] = st.number_input(
                "Serum Total Lipids (mg/dL)",
                value=float(values["total_lipids"])
            )
    

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
        "Analyze Lipid Profile",
        use_container_width=True,
        disabled=not verified
    )

    if "lipid_prediction_done" not in st.session_state:
        st.session_state.lipid_prediction_done = False

    if predict:
        st.session_state.lipid_prediction_done = True

    if st.session_state.lipid_prediction_done:

        analysis = analyze_lipid_profile(
            {
                "gender": gender,
                **values
            }
        )


        st.caption("Step 4 of 4 • Analysis Completed")


        
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
        margin-bottom:10px;
        ">
        Lipid  Profile Prediction
        </h2>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
        background:#DCEEEE;
        border-left:8px solid #14746F;
        padding:25px;
        border-radius:16px;
        margin-bottom:10px;
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
        margin-top:8px;
        ">
        {analysis["summary"]}
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            """
            <h2 style="
            color:white;
            margin-bottom:20px;
            ">
            Lipid Profile Results
            </h2>
            """,
            unsafe_allow_html=True
        )
        col1, col2, col3, col4 = st.columns([4.5,2,2.5,1.5])

        with col1:
            st.markdown(
                "<p style='color:#B8C7D9;font-size:18px;font-weight:700;'>Test</p>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                "<p style='color:#B8C7D9;font-size:18px;font-weight:700;'>Value</p>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                "<p style='color:#B8C7D9;font-size:18px;font-weight:700;'>Clinical Range</p>",
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                "<p style='color:#B8C7D9;font-size:18px;font-weight:700;'>Status</p>",
                unsafe_allow_html=True
            )

        st.divider()
        for test, info in analysis["results"].items():
            
            col1, col2, col3, col4 = st.columns([4.5,2,2.5,1.5])

            with col1:

                st.markdown(
                    f"""
                    <p style="
                    color:white;
                    font-size:17px;
                    font-weight:600;
                    margin:0;
                    ">
                    {test}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                f"""
                <p style="
                color:white;
                font-size:17px;
                margin:0;
                ">
                {info["value"]} mg/dL
                </p>
                """,
                unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                f"""
                <p style="
                color:white;
                font-size:17px;
                margin:0;
                ">
                {info["range"]}
                </p>
                """,
                unsafe_allow_html=True
                )

            with col4:

                if info["status"] == "Healthy":

                    color = "#DDF7E3"
                    text = "#1B5E20"

                elif "Borderline" in info["status"]:

                    color = "#FFF3CD"
                    text = "#856404"

                else:

                    color = "#FDE2E2"
                    text = "#C62828"

                st.markdown(
                    f"""
                    <div style="
                    background:{color};
                    color:{text};
                    padding:6px 12px;
                    border-radius:20px;
                    min-width:110px;
                    display:inline-block;
                    text-align:center;
                    font-weight:700;
                    margin:auto;
                    ">
                    {info["status"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(
                "<hr style='border:1px solid rgba(255,255,255,.12); margin:8px 0;'>",
                unsafe_allow_html=True
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
            "<h2 style='color:white;'> Diet Recommendations</h2>",
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
                "<h2 style='color:white;'> Lifestyle Recommendations</h2>",
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
                "<h2 style='color:white;'>👨‍⚕ Medical Advice</h2>",
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

        context = {
            "module": "Lipid Profile",

            "prediction": "Rule-based Lipid Profile Analysis",

            "confidence": "Rule-based Analysis",

            "lipid_values": {
                "Total Cholesterol": values["total_cholesterol"],
                "Triglycerides": values["triglycerides"],
                "HDL": values["hdl"],
                "LDL": values["ldl"],
                "VLDL": values["vldl"]
            },

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