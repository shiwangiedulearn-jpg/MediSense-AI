from pathlib import Path

import joblib

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.extractor import extract_text
from utils.parser import extract_values
from utils.predictor import predict_heart_disease
from utils.chatbot import get_chat_response

from utils.diabetes_extractor import extract_diabetes_values
from utils.diabetes_rules import analyze_diabetes
from utils.predictor import predict_diabetes

from utils.liver_extractor import extract_liver_values
from utils.liver_rules import analyze_liver
from utils.predictor import predict_liver_disease

from utils.predictor import predict_kidney_disease
from utils.kidney_rules import analyze_kidney
from utils.kidney_extractor import extract_kidney_values

from utils.lipid_rules import analyze_lipid_profile
from utils.lipid_extractor import extract_lipid_values

from utils.predictor import predict_symptom_disease
from utils.symptom_rules import analyze_symptom

import numpy as np


app = FastAPI(
    title="MediSense AI API"
)
 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://medi-sense-ai-eight-nu.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "models" / "heart_model.pkl"
)

feature_order = joblib.load(
    BASE_DIR / "models" / "feature_order.pkl"
)

diabetes_model = joblib.load(
    BASE_DIR / "models" / "diabetes_model.pkl"
)

diabetes_feature_order = joblib.load(
    BASE_DIR / "models" / "diabetes_feature_order.pkl"
)

liver_model = joblib.load(
    BASE_DIR / "models" / "liver_model.pkl"
)

liver_feature_order = joblib.load(
    BASE_DIR / "models" / "liver_feature_order.pkl"
)

KIDNEY_MODEL = joblib.load(
    BASE_DIR / "models" / "kidney_model.pkl"
)

KIDNEY_FEATURE_ORDER = joblib.load(
    BASE_DIR / "models" / "kidney_feature_order.pkl"
)

symptom_model = joblib.load(
    BASE_DIR / "models" / "symptom_model.pkl"
)

symptom_feature_order = joblib.load(
    BASE_DIR / "models" / "symptom_feature_order.pkl"
)

DEFAULT_VALUES = {
    "cp": 3,
    "trestbps": 120,
    "chol": 200,
    "fbs": 0,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 1.0,
    "slope": 1,
    "ca": 0,
    "thal": 1,
}

DIABETES_DEFAULT_VALUES = {
    "Pregnancies": 0,
    "Glucose": 120,
    "BloodPressure": 80,
    "SkinThickness": 20,
    "Insulin": 80,
    "BMI": 22.0,
    "DiabetesPedigreeFunction": 0.47,
}

LIVER_DEFAULT_VALUES = {

    "tot_bilirubin": 1.0,

    "direct_bilirubin": 0.2,

    "alkphos": 150,

    "sgpt": 40,

    "sgot": 40,

    "tot_proteins": 7.0,

    "albumin": 4.0,

    "ag_ratio": 1.2

}

KIDNEY_DEFAULT_VALUES = {
    "bgr": 120,
    "bu": 20,
    "sc": 1.0,
    "sod": 140,
    "pot": 4.5,
    "hemo": 15.0,
    "pcv": 45,
    "wc": 8000,
    "rc": 5.0,
    "bp": 80,
    "sg": 1.015,
    "al": 0,
    "su": 0,
    "rbc": 0,
    "pc": 0,
    "pcc": 0,
    "ba": 0,
    "htn": 0,
    "dm": 0,
    "cad": 0,
    "appet": 0,
    "pe": 0,
    "ane": 0,
}

# =====================================================
# REQUEST MODEL
# =====================================================

class PredictionRequest(BaseModel):

    name: str
    age: int
    gender: str
    height: float
    weight: float
    values: dict

class ChatRequest(BaseModel):

    message: str

    context: dict

    history: list = []

class LipidPredictionRequest(BaseModel):

    name: str
    age: int
    gender: str
    height: float
    weight: float
    values: dict
# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {
        "message": "MediSense AI API is running"
    }


# =====================================================
# EXTRACT MEDICAL VALUES
# =====================================================

@app.post("/heart/extract")
async def extract_heart_report(
    file: UploadFile = File(...)
):

    try:

        # Read uploaded file
        contents = await file.read()

        # Create an object similar to
        # what your existing extractor expects.
        from io import BytesIO

        file_object = BytesIO(contents)

        # Make the object behave like Streamlit's UploadedFile
        file_object.name = file.filename
        file_object.type = file.content_type or ""

        extracted_text = extract_text(file_object)

        # Parse values
        extracted_values = extract_values(
            extracted_text
        )

        # Start with defaults
        final_values = DEFAULT_VALUES.copy()

        # Extracted values overwrite defaults
        if extracted_values:

            for key, value in extracted_values.items():

                if value is not None:

                    final_values[key] = value

        return {
            "success": True,
            "filename": file.filename,
            "values": final_values,
        }

    except Exception as error:

        print(
            "Extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/diabetes/extract")
async def extract_diabetes_report(
    file: UploadFile = File(...)
):

    try:

        contents = await file.read()

        from io import BytesIO

        file_object = BytesIO(contents)

        file_object.name = file.filename
        file_object.type = file.content_type or ""

        # Extract text from PDF/image
        extracted_text = extract_text(file_object)

        # Extract Diabetes-specific values
        extracted_values = extract_diabetes_values(
            extracted_text
        )

        # Start with defaults
        final_values = DIABETES_DEFAULT_VALUES.copy()

        # Replace defaults with extracted values
        if extracted_values:

            for key, value in extracted_values.items():

                if value is not None:

                    final_values[key] = value

        return {
            "success": True,
            "filename": file.filename,
            "values": final_values
        }

    except Exception as error:

        print(
            "Diabetes extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

# =====================================================
# LIVER REPORT EXTRACTION
# =====================================================

@app.post("/liver/extract")
async def extract_liver_report(
    file: UploadFile = File(...)
):

    try:

        contents = await file.read()

        from io import BytesIO

        file_object = BytesIO(contents)

        file_object.name = file.filename
        file_object.type = file.content_type or ""

        extracted_text = extract_text(
            file_object
        )

        extracted_values = extract_liver_values(
            extracted_text
        )

        final_values = (
            LIVER_DEFAULT_VALUES.copy()
        )

        if extracted_values:

            for key, value in extracted_values.items():

                if value is not None:

                    final_values[key] = value

        return {

            "success": True,

            "filename": file.filename,

            "values": final_values

        }

    except Exception as error:

        print(
            "Liver extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/kidney/extract")
async def extract_kidney_report(
    file: UploadFile = File(...)
):

    try:

        contents = await file.read()

        from io import BytesIO

        file_object = BytesIO(contents)

        file_object.name = file.filename
        file_object.type = file.content_type or ""

        extracted_text = extract_text(
            file_object
        )

        extracted_values = extract_kidney_values(
            extracted_text
        )

        final_values = (
            KIDNEY_DEFAULT_VALUES.copy()
        )

        if extracted_values:

            for key, value in extracted_values.items():

                if value is not None:

                    final_values[key] = value

        return {
            "success": True,
            "filename": file.filename,
            "values": final_values
        }

    except Exception as error:

        print(
            "Kidney extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/lipid/extract")
async def extract_lipid_report(
    file: UploadFile = File(...)
):

    try:

        contents = await file.read()

        from io import BytesIO

        file_object = BytesIO(contents)

        file_object.name = file.filename
        file_object.type = file.content_type or ""

        extracted_text = extract_text(
            file_object
        )

        extracted_values = extract_lipid_values(
            extracted_text
        )

        return {
            "success": True,
            "filename": file.filename,
            "values": extracted_values
        }

    except Exception as error:

        print(
            "Lipid extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/diabetes/predict")
def predict_diabetes_api(
    request: PredictionRequest
):

    try:

        values = DIABETES_DEFAULT_VALUES.copy()

        values.update(
            request.values
        )

        # Personal details
        values["Age"] = request.age

        values["Sex"] = (
            1
            if request.gender == "Male"
            else 0
        )

        # Predict
        prediction, probability = predict_diabetes(
            values,
            diabetes_model,
            diabetes_feature_order
        )

        diabetes_probability = (
            float(probability[1]) * 100
        )

        # BMI
        bmi = (
            request.weight
            / ((request.height / 100) ** 2)
        )

        # Diabetes analysis
        analysis = analyze_diabetes(
            prediction,
            diabetes_probability,
            values
        )

        return {

            "success": True,

            "prediction": int(prediction),

            "probability": diabetes_probability,

            "name": request.name,

            "age": request.age,

            "gender": request.gender,

            "height": request.height,

            "weight": request.weight,

            "bmi": bmi,

            "values": values,

            "overall": analysis["overall"],

            "summary": analysis["summary"],

            "health_effects": analysis["health_effects"],

            "diet": analysis["diet"],

            "lifestyle": analysis["lifestyle"],

            "medical": analysis["medical"]

        }

    except Exception as error:

        print(
            "Diabetes prediction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/liver/predict")
def predict_liver(
    request: PredictionRequest
):

    try:

        values = (
            LIVER_DEFAULT_VALUES.copy()
        )

        values.update(
            request.values
        )

        # Personal details
        values["age"] = request.age

        values["gender"] = (
            1
            if request.gender == "Male"
            else 0
        )

        # Existing model
        prediction, probability = (
            predict_liver_disease(
                values,
                liver_model,
                liver_feature_order
            )
        )

        liver_probability = (
            float(probability[1]) * 100
        )

        # BMI
        bmi = (
            request.weight
            / ((request.height / 100) ** 2)
        )

        # BMI category
        if bmi < 18.5:

            bmi_category = "Underweight"

        elif bmi < 25:

            bmi_category = "Normal"

        elif bmi < 30:

            bmi_category = "Overweight"

        else:

            bmi_category = "Obese"

        # Existing Liver analysis
        analysis = analyze_liver(
            prediction,
            liver_probability,
            values
        )

        return {

            "success": True,

            "prediction": int(
                prediction
            ),

            "probability":
                liver_probability,

            "name":
                request.name,

            "age":
                request.age,

            "gender":
                request.gender,

            "height":
                request.height,

            "weight":
                request.weight,

            "bmi":
                bmi,

            "bmiCategory":
                bmi_category,

            "values":
                values,

            "overall":
                analysis["overall"],

            "summary":
                analysis["summary"],

            "health_effects":
                analysis["health_effects"],

            "diet":
                analysis["diet"],

            "lifestyle":
                analysis["lifestyle"],

            "medical":
                analysis["medical"]

        }

    except Exception as error:

        print(
            "Liver prediction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/kidney/predict")
def predict_kidney(
    request: PredictionRequest
):

    try:

        values = (
            KIDNEY_DEFAULT_VALUES.copy()
        )

        values.update(
            request.values
        )

        # Age comes from personal details
        values["age"] = request.age

        prediction, probability = (
            predict_kidney_disease(
                values,
                KIDNEY_MODEL,
                KIDNEY_FEATURE_ORDER
            )
        )

        kidney_probability = (
            float(probability[1]) * 100
        )

        

        bmi = (
            request.weight
            / ((request.height / 100) ** 2)
        )

        if bmi < 18.5:

            bmi_category = "Underweight"

        elif bmi < 25:

            bmi_category = "Normal"

        elif bmi < 30:

            bmi_category = "Overweight"

        else:

            bmi_category = "Obese"



        analysis = analyze_kidney(
            prediction,
            kidney_probability,
            values
        )


        return {

            "success": True,

            "prediction":
                int(prediction),

            "probability":
                kidney_probability,

            "name":
                request.name,

            "age":
                request.age,

            "gender":
                request.gender,

            "height":
                request.height,

            "weight":
                request.weight,

            "bmi":
                bmi,

            "bmiCategory":
                bmi_category,

            "values":
                values,

            "overall":
                analysis["overall"],

            "summary":
                analysis["summary"],

            "health_effects":
                analysis["health_effects"],

            "diet":
                analysis["diet"],

            "lifestyle":
                analysis["lifestyle"],

            "medical":
                analysis["medical"]

        }

    except Exception as error:

        print(
            "Kidney prediction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/lipid/predict")
def predict_lipid(
    request: LipidPredictionRequest
):

    try:

        values = {
            "total_cholesterol":
                float(
                    request.values.get(
                        "total_cholesterol",
                        200
                    )
                ),

            "ldl":
                float(
                    request.values.get(
                        "ldl",
                        100
                    )
                ),

            "vldl":
                float(
                    request.values.get(
                        "vldl",
                        30
                    )
                ),

            "hdl":
                float(
                    request.values.get(
                        "hdl",
                        50
                    )
                ),

            "triglycerides":
                float(
                    request.values.get(
                        "triglycerides",
                        150
                    )
                ),

            "total_lipids":
                float(
                    request.values.get(
                        "total_lipids",
                        600
                    )
                )
        }


        gender = (
            1
            if request.gender == "Male"
            else 0
        )


        analysis = analyze_lipid_profile(
            {
                "gender": gender,
                **values
            }
        )


     

        bmi = (
            request.weight
            / ((request.height / 100) ** 2)
        )


        if bmi < 18.5:

            bmi_category = "Underweight"

        elif bmi < 25:

            bmi_category = "Normal"

        elif bmi < 30:

            bmi_category = "Overweight"

        else:

            bmi_category = "Obese"


        return {

            "success": True,

            "name":
                request.name,

            "age":
                request.age,

            "gender":
                request.gender,

            "height":
                request.height,

            "weight":
                request.weight,

            "bmi":
                bmi,

            "bmiCategory":
                bmi_category,

            "values":
                values,

            "overall":
                analysis["overall"],

            "summary":
                analysis["summary"],

            "results":
                analysis["results"],

            "health_effects":
                analysis["health_effects"],

            "diet":
                analysis["diet"],

            "lifestyle":
                analysis["lifestyle"],

            "medical":
                analysis["medical"]

        }


    except Exception as error:

        print(
            "Lipid prediction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/symptom/predict")
def predict_symptom(
    request: PredictionRequest
):

    try:

       
        values = {
            feature: 0
            for feature in symptom_feature_order
        }

        # Values selected from React
        if request.values:

            for key, value in request.values.items():

                if key in values:
                    values[key] = value

       
        prediction, probability = (
            predict_symptom_disease(
                values,
                symptom_model,
                symptom_feature_order
            )
        )

       
        confidence = (
            float(max(probability)) * 100
        )

        
        analysis = analyze_symptom(
            prediction,
            confidence,
            values
        )

        
        top3_indices = (
            np.argsort(probability)[::-1][:3]
        )

        top3 = []

        for index in top3_indices:

            top3.append({
                "disease": str(
                    symptom_model.classes_[index]
                ),
                "probability":
                    float(probability[index]) * 100
            })

       
        selected_symptoms = [
            key
            for key, value in values.items()
            if value == 1
        ]

       
        bmi = (
            request.weight
            / ((request.height / 100) ** 2)
        )

       
        if bmi < 18.5:

            bmi_category = "Underweight"

        elif bmi < 25:

            bmi_category = "Normal"

        elif bmi < 30:

            bmi_category = "Overweight"

        else:

            bmi_category = "Obese"

       
        return {

            "success": True,

            "prediction":
                str(prediction),

            "confidence":
                confidence,

            "name":
                request.name,

            "age":
                request.age,

            "gender":
                request.gender,

            "height":
                request.height,

            "weight":
                request.weight,

            "bmi":
                bmi,

            "bmiCategory":
                bmi_category,

            "values":
                values,

            "selectedSymptoms":
                selected_symptoms,

            "top3":
                top3,

            "summary":
                analysis["summary"],

            "health_effects":
                analysis["health_effects"],

            "diet":
                analysis["diet"],

            "lifestyle":
                analysis["lifestyle"],

            "medical":
                analysis["medical"]

        }

    except Exception as error:

        print(
            "Symptom prediction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


class LiverChatRequest(BaseModel):

    message: str

    context: dict

    history: list = []

class KidneyChatRequest(BaseModel):

    message: str

    context: dict

    history: list = []

class LipidChatRequest(BaseModel):

    message: str

    context: dict

    history: list = []


@app.post("/liver/chat")
def liver_chat(request: LiverChatRequest):

    try:

        # Convert React conversation history
        # into the format expected by chatbot.py

        history_text = ""

        for message in request.history:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            history_text += (
                f"{role}: {content}\n"
            )


        # Send complete prediction context
        # to the existing MediSense AI chatbot

        answer = get_chat_response(
            request.context,
            history_text
        )


        return {

            "success": True,

            "answer": answer

        }


    except Exception as error:

        print(
            "Liver chatbot error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/kidney/chat")
def kidney_chat(
    request: KidneyChatRequest
):

    try:

        history_text = ""

        for message in request.history:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            history_text += (
                f"{role}: {content}\n"
            )

        answer = get_chat_response(
            request.context,
            history_text
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as error:

        print(
            "Kidney chatbot error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/heart/predict")
def predict_heart(
    request: PredictionRequest
):

    try:

        values = DEFAULT_VALUES.copy()

        values.update(
            request.values
        )

        # Personal details required by the heart model
        values["age"] = request.age

        # Gender mapping
        values["sex"] = (
            1
            if request.gender == "Male"
            else 0
        )

        # Run existing model
        prediction, probability = (
            predict_heart_disease(
                values,
                model,
                feature_order
            )
        )

        heart_probability = (
            float(probability[1]) * 100
        )


        # -----------------------------------------
        # RISK
        # -----------------------------------------

        if heart_probability < 30:

            risk_label = (
                "Low Risk of Heart Disease"
            )

            risk_class = "low"

        elif heart_probability < 70:

            risk_label = (
                "Moderate Risk of Heart Disease"
            )

            risk_class = "moderate"

        else:

            risk_label = (
                "High Risk of Heart Disease"
            )

            risk_class = "high"


        # -----------------------------------------
        # BMI
        # -----------------------------------------

        bmi = (
            request.weight
            / ((request.height / 100) ** 2)
        )


        # -----------------------------------------
        # CONTRIBUTING FACTORS
        # -----------------------------------------

        factors = []

        if values["chol"] > 240:

            factors.append(
                "High cholesterol level"
            )

        if values["trestbps"] > 140:

            factors.append(
                "Elevated resting blood pressure"
            )

        if values["fbs"] == 1:

            factors.append(
                "Elevated fasting blood sugar level"
            )

        if values["oldpeak"] > 2:

            factors.append(
                "Abnormal ST depression (Oldpeak)"
            )

        if values["exang"] == 1:

            factors.append(
                "Exercise-induced angina present"
            )

        if bmi >= 25:

            factors.append(
                "BMI indicates overweight or obesity"
            )


        # -----------------------------------------
        # RECOMMENDATIONS
        # -----------------------------------------

        recommendations = []

        if heart_probability >= 70:

            recommendations.append(
                "Consult a cardiologist as soon as possible."
            )

            if values["chol"] > 240:

                recommendations.append(
                    "Reduce fried and fatty foods."
                )

                recommendations.append(
                    "Increase fibre-rich foods."
                )

            if values["trestbps"] > 140:

                recommendations.append(
                    "Reduce salt intake."
                )

                recommendations.append(
                    "Monitor blood pressure regularly."
                )

            if values["fbs"] == 1:

                recommendations.append(
                    "Control blood sugar through diet and exercise."
                )

            if bmi >= 25:

                recommendations.append(
                    "Engage in regular physical activity."
                )

                recommendations.append(
                    "Follow a balanced diet to manage weight."
                )

            recommendations.append(
                "Avoid smoking and excessive alcohol."
            )

            recommendations.append(
                "Exercise only after medical advice."
            )

            recommendations.append(
                "Take prescribed medicines regularly."
            )


        elif heart_probability >= 30:

            recommendations.extend([
                "Schedule a routine consultation with a healthcare professional.",
                "Exercise regularly.",
                "Eat a balanced diet.",
                "Maintain a healthy weight.",
                "Reduce stress.",
                "Get regular health check-ups.",
            ])


        else:

            recommendations.extend([
                "Continue maintaining a healthy lifestyle.",
                "Eat a balanced diet.",
                "Exercise regularly.",
                "Get adequate sleep.",
                "Continue regular health screenings.",
            ])


        return {

            "success": True,

            "prediction": int(prediction),

            "probability": heart_probability,

            "riskLabel": risk_label,

            "riskClass": risk_class,

            "bmi": bmi,

            "factors": factors,

            "recommendations": recommendations,

        }


    except Exception as error:

        print(
            "Prediction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/heart/chat")
def heart_chat(request: ChatRequest):

    try:

        # Convert React history into the format
        # expected by the existing chatbot
        history_text = ""

        for message in request.history:

            role = message.get("role", "")

            content = message.get(
                "content",
                ""
            )

            history_text += (
                f"{role}: {content}\n"
            )

        # Add the latest user question
        history_text += (
            f"user: {request.message}\n"
        )

        # Existing MediSense AI logic
        answer = get_chat_response(
            request.context,
            history_text
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as error:

        print(
            "Chatbot error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/diabetes/chat")
def diabetes_chat(request: ChatRequest):

    try:

        # Convert React history into text
        history_text = ""

        for message in request.history:

            role = message.get("role", "")

            content = message.get(
                "content",
                ""
            )

            history_text += (
                f"{role}: {content}\n"
            )

        # Add latest question
        history_text += (
            f"user: {request.message}\n"
        )

        # Use existing MediSense AI chatbot
        answer = get_chat_response(
            request.context,
            history_text
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as error:

        print(
            "Diabetes chatbot error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/diabetes/chat")
def diabetes_chat(request: ChatRequest):

    try:

        history_text = ""

        for message in request.history:

            role = message.get("role", "")

            content = message.get(
                "content",
                ""
            )

            history_text += (
                f"{role}: {content}\n"
            )

        history_text += (
            f"user: {request.message}\n"
        )

        answer = get_chat_response(
            request.context,
            history_text
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as error:

        print(
            "Diabetes chatbot error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/lipid/chat")
def lipid_chat(
    request: LipidChatRequest
):

    try:

        history_text = ""

        for message in request.history:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            history_text += (
                f"{role}: {content}\n"
            )


        answer = get_chat_response(
            request.context,
            history_text
        )


        return {

            "success": True,

            "answer": answer

        }


    except Exception as error:

        print(
            "Lipid chatbot error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/symptom/chat")
def symptom_chat(
    request: ChatRequest
):

    try:

       
        history_text = ""

        for message in request.history:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            history_text += (
                f"{role}: {content}\n"
            )


        history_text += (
            f"user: {request.message}\n"
        )

        
        answer = get_chat_response(
            request.context,
            history_text
        )

        return {

            "success": True,

            "answer": answer

        }

    except Exception as error:

        print(
            "Symptom chatbot error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )