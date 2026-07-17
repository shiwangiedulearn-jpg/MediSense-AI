import streamlit as st
import base64

st.set_page_config(
    page_title="MediSense AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>



section.main{
    margin-left:0rem !important;
}

</style>
""",unsafe_allow_html=True)


def get_base64(file_path):
    with open(file_path, "rb") as image:
        return base64.b64encode(image.read()).decode()


bg_image = get_base64("assets/background.jpg")

st.markdown(
    f"""
<style>

.stApp {{
    background:white;
}}

.block-container{{
    max-width:100% !important;
    padding-top:0rem;
    padding-left:0rem;
    padding-right:0rem;
    padding-bottom:2rem;
}}

.hero{{
    position:relative;
    background-image:url("data:image/jpg;base64,{bg_image}");
    background-size:cover;
    background-position:center;
    height:450px;
    width:100%;
    border-radius:0px;
    overflow:hidden;
    display:flex;
    align-items:center;
    padding-left:8%;
    margin-bottom:50px;
}}

.hero::before{{
    content:"";
    position:absolute;
    top:0;
    left:0;
    right:0;
    bottom:0;
    background:linear-gradient(
        90deg,
        rgba(8,27,41,0.82) 0%,
        rgba(8,27,41,0.55) 40%,
        rgba(8,27,41,0.15) 100%
    );
}}
.hero-text{{
    position:relative;
    z-index:2;
    width:42%;
    color:white;
}}

.hero-content{{
    position:relative;
    z-index:5;
}}

.hero-content h1{{
    color:white;
    font-size:68px;
    font-weight:700;
    margin-bottom:20px;
}}

.hero-content h3{{
    color:white;
    font-size:30px;
    font-weight:500;
    margin-top:18px;
    margin-bottom:25px;
}}

.hero-content p{{
    color:white;
    font-size:20px;
    line-height:1.8;
    max-width:520px;
}}


.card{{
    background:#DCEEEE;
    border:1px solid #BFD8D7;
    border-radius:20px;
    overflow:hidden;
    box-shadow:0 10px 25px rgba(15,76,92,.10);
    transition:.35s ease;
    margin-bottom:0px;
}}

.card:hover{{
    transform:translateY(-8px);
    box-shadow:0 20px 40px rgba(15,76,92,.20);
}}

.card-body{{
    padding:45px 30px;
    min-height:260px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    border-top:6px solid #14746F;
}}

.card-footer{{
    background:#14746F;
    color:white;
    text-align:center;
    padding:16px;
    font-size:17px;
    font-weight:600;
}}

.card h2{{
    color:#0F4C5C;
    font-size:38px;
    font-weight:700;
    margin-bottom:25px;
    text-align:center;
}}

.card p{{
    color:#516B6B;
    font-size:17px;
    text-align:center;
    line-height:1.7;
}}

div.stButton > button{{
    width:100%;
    height:64px;
    margin-top:-8px;
    border:none;
    border-radius:0px 0px 20px 20px;
    background:#14746F;
    color:white;
    font-size:18px;
    font-weight:600;
    box-shadow:none;
    transition:0.3s;
}}

div.stButton > button:hover{{
    background:#0F5C59;
}}



</style>
""",
    unsafe_allow_html=True
)
st.markdown(
    """
<div class="hero">
    <div class="hero-text">
        <div class="hero-content">
            <h1>MediSense AI</h1>
            <h3>AI-Powered Healthcare Intelligence Platform</h3>
            <p>
                Upload medical reports and receive AI-driven disease prediction,
                personalized recommendations and intelligent health guidance.
            </p>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True
)



st.markdown(
"""
<h2 style='text-align:center;color:#0F4C5C'>
Medical Analysis Modules
</h2>

<p style='text-align:center;color:#516B6B;font-size:17px'>
Select the diagnostic module based on your medical report.
</p>
""",
unsafe_allow_html=True
)
col1,col2,col3=st.columns(3)
col4,col5,col6=st.columns(3)

with col1:

    st.markdown("""
<div class="card">

<div class="card-body">

<h2>Symptom Checker</h2>

<p>
Tell us about your symptoms and receive an AI-powered assessment
of the most likely health condition.
</p>

</div>

</div>
""", unsafe_allow_html=True)

    if st.button("Open Module →", key="symptom_checker", use_container_width=True):
        st.switch_page("pages/🩹_Symptom_Checker.py")

with col2:

    st.markdown("""
<div class="card">

<div class="card-body">

<h2>Lipid Profile</h2>

<p>
HDL, LDL, Cholesterol and
Triglyceride Analysis.
</p>

</div>

</div>
""", unsafe_allow_html=True)

    if st.button("Open Module →", key="lipid", use_container_width=True):
        st.switch_page("pages/🟡_Lipid_Profile.py")

with col3:

    st.markdown("""
<div class="card">

<div class="card-body">

<h2>Diabetes</h2>

<p>
Blood Sugar, HbA1c and
Diabetes Risk Prediction.
</p>

</div>

</div>
""", unsafe_allow_html=True)

    if st.button("Open Module →", key="diabetes", use_container_width=True):
        st.switch_page("pages/🩸_Diabetes.py")

with col4:

    st.markdown("""
<div class="card">

<div class="card-body">

<h2>Kidney Disease</h2>

<p>
Kidney Function Assessment
using Laboratory Reports.
</p>

</div>

</div>
""", unsafe_allow_html=True)

    if st.button("Open Module →", key="kidney", use_container_width=True):
        st.switch_page("pages/🟤_Kidney_Disease.py")

with col5:

    st.markdown("""
<div class="card">

<div class="card-body">

<h2>Liver Disease</h2>

<p>
Liver Function Analysis using
SGOT, SGPT and Bilirubin.
</p>

</div>

</div>
""", unsafe_allow_html=True)

    if st.button("Open Module →", key="liver", use_container_width=True):
        st.switch_page("pages/🟢_Liver_Disease.py")


with col6:
    st.markdown("""
<div class="card">
    <div class="card-body">
        <h2>Heart Disease</h2>
        <p>
        ECG Analysis, Cardiac Risk Prediction and
        Heart Health Assessment.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    if st.button("Open Module →", key="heart", use_container_width=True):
        st.switch_page("pages/❤️_Heart_Disease.py")

st.divider()

st.markdown(
"""
<div style='text-align:center;color:gray'>

© 2026 MediSense AI

Artificial Intelligence Powered Healthcare Assistant

</div>
""",
unsafe_allow_html=True
)