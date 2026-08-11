import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    FaArrowLeft,
    FaHeartbeat,
    FaCloudUploadAlt
} from "react-icons/fa";

import "./KidneyDisease.css";

export default function KidneyDisease() {

    const navigate = useNavigate();

    // =====================================================
    // PERSONAL DETAILS
    // =====================================================

    const [name, setName] = useState("");
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("Male");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");

    // =====================================================
    // REPORT
    // =====================================================

    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);

    // =====================================================
    // KIDNEY VALUES
    // =====================================================

    const [values, setValues] = useState({
        bgr: 120,
        bu: 20,
        sc: 1.0,
        sod: 140,
        pot: 4.5,
        hemo: 15.0,
        pcv: 45,
        wc: 8000,
        rc: 5.0
    });

    // =====================================================
    // USER SELECTED VALUES
    // =====================================================

    const [bp, setBp] = useState(80);
    const [sg, setSg] = useState(1.015);

    const [protein, setProtein] =
        useState("No");

    const [sugar, setSugar] =
        useState("No");

    const [rbc, setRbc] =
        useState("No");

    const [pc, setPc] =
        useState("No");

    const [pcc, setPcc] =
        useState("No");

    const [ba, setBa] =
        useState("No");

    const [htn, setHtn] =
        useState("No");

    const [dm, setDm] =
        useState("No");

    const [cad, setCad] =
        useState("No");

    const [appet, setAppet] =
        useState("No");

    const [pe, setPe] =
        useState("No");

    const [ane, setAne] =
        useState("No");

    // =====================================================
    // CONFIRMATION
    // =====================================================

    const [confirmed, setConfirmed] =
        useState(false);

    // =====================================================
    // RESULT
    // =====================================================

    const [result, setResult] =
        useState(null);

    // =====================================================
    // CHATBOT
    // =====================================================

    const [chatInput, setChatInput] =
        useState("");

    const [chatMessages, setChatMessages] =
        useState([]);

    const [chatLoading, setChatLoading] =
        useState(false);


    // =====================================================
    // BMI
    // =====================================================

    const calculateBMI = () => {

        if (!height || !weight) {
            return "--";
        }

        const h =
            Number(height) / 100;

        const w =
            Number(weight);

        if (!h || !w) {
            return "--";
        }

        return (
            w / (h * h)
        ).toFixed(2);
    };


    const getBMICategory = () => {

        if (!height || !weight) {
            return "--";
        }

        const bmi =
            Number(weight) /
            ((Number(height) / 100) ** 2);

        if (bmi < 18.5) {
            return "Underweight";
        }

        if (bmi < 25) {
            return "Normal";
        }

        if (bmi < 30) {
            return "Overweight";
        }

        return "Obese";
    };


    // =====================================================
    // CHANGE LAB VALUE
    // =====================================================

    const handleValueChange = (
        field,
        value
    ) => {

        setValues(previous => ({
            ...previous,
            [field]: value
        }));

    };


    // =====================================================
    // REPORT EXTRACTION
    // =====================================================

    const handleFileChange = async (
        selectedFile
    ) => {

        if (!selectedFile) {
            return;
        }

        setFile(selectedFile);
        setUploading(true);

        try {

            const formData =
                new FormData();

            formData.append(
                "file",
                selectedFile
            );

            const response =
                await fetch(
                    "https://medisense-ai-4zpl.onrender.com/kidney/extract",
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Report extraction failed"
                );

            }

            if (data.values) {

                setValues(previous => ({
                    ...previous,
                    ...data.values
                }));

            }

        } catch (error) {

            console.error(
                "Kidney extraction error:",
                error
            );

            alert(
                "Could not process the report. Please make sure the backend is running."
            );

        } finally {

            setUploading(false);

        }

    };


    // =====================================================
    // CONVERT SELECTED VALUES
    // =====================================================

    const yesNo = value =>
        value === "Yes" ? 1 : 0;


    const amountValue = value => {

        const mapping = {

            "No": 0,

            "A small amount": 1,

            "A moderate amount": 2,

            "A large amount": 3,

            "A very large amount": 4,

            "I don't know": 5

        };

        return mapping[value];

    };


    // =====================================================
    // PREDICTION
    // =====================================================

    const handlePredict = async () => {

        if (!name.trim()) {

            alert(
                "Please enter your name."
            );

            return;
        }

        if (!age) {

            alert(
                "Please enter your age."
            );

            return;
        }

        if (!height || !weight) {

            alert(
                "Please enter your height and weight."
            );

            return;
        }

        if (!confirmed) {

            alert(
                "Please confirm that all the above values are correct."
            );

            return;
        }


        try {

            const response =
                await fetch(
                    "https://medisense-ai-4zpl.onrender.com/kidney/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            name,

                            age:
                                Number(age),

                            gender,

                            height:
                                Number(height),

                            weight:
                                Number(weight),

                            values: {

                                bgr:
                                    Number(values.bgr),

                                bu:
                                    Number(values.bu),

                                sc:
                                    Number(values.sc),

                                sod:
                                    Number(values.sod),

                                pot:
                                    Number(values.pot),

                                hemo:
                                    Number(values.hemo),

                                pcv:
                                    Number(values.pcv),

                                wc:
                                    Number(values.wc),

                                rc:
                                    Number(values.rc),

                                bp:
                                    Number(bp),

                                sg:
                                    Number(sg),

                                al:
                                    amountValue(
                                        protein
                                    ),

                                su:
                                    amountValue(
                                        sugar
                                    ),

                                rbc:
                                    yesNo(rbc),

                                pc:
                                    yesNo(pc),

                                pcc:
                                    yesNo(pcc),

                                ba:
                                    yesNo(ba),

                                htn:
                                    yesNo(htn),

                                dm:
                                    yesNo(dm),

                                cad:
                                    yesNo(cad),

                                appet:
                                    yesNo(appet),

                                pe:
                                    yesNo(pe),

                                ane:
                                    yesNo(ane)

                            }

                        })

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Prediction failed"
                );

            }


            console.log(
                "Kidney prediction:",
                data
            );


            setResult(data);


            setTimeout(() => {

                document
                    .getElementById(
                        "kidney-prediction-result"
                    )
                    ?.scrollIntoView({
                        behavior:
                            "smooth",
                        block:
                            "start"
                    });

            }, 100);


        } catch (error) {

            console.error(
                "Kidney prediction error:",
                error
            );

            alert(
                error.message ||
                "Prediction failed."
            );

        }

    };


    // =====================================================
    // CHATBOT
    // =====================================================

    const handleChat = async () => {

        if (!chatInput.trim()) {
            return;
        }

        if (!result) {
            return;
        }

        const question =
            chatInput.trim();


        const userMessage = {

            role: "user",

            content: question

        };


        const updatedMessages = [

            ...chatMessages,

            userMessage

        ];


        setChatMessages(
            updatedMessages
        );

        setChatInput("");

        setChatLoading(true);


        try {

            const context = {

                module:
                    "Kidney Disease",

                prediction:
                    result.prediction,

                probability:
                    result.probability,

                overall:
                    result.overall,

                summary:
                    result.summary,

                patient: {

                    name,

                    age:
                        Number(age),

                    gender,

                    height:
                        Number(height),

                    weight:
                        Number(weight),

                    bmi:
                        result.bmi,

                    bmiCategory:
                        result.bmiCategory

                },

                values:
                    result.values,

                health_effects:
                    result.health_effects,

                diet:
                    result.diet,

                lifestyle:
                    result.lifestyle,

                medical_advice:
                    result.medical

            };


            const response =
                await fetch(
                    "https://medisense-ai-4zpl.onrender.com/kidney/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                message:
                                    question,

                                context,

                                history:
                                    updatedMessages

                            })

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Chatbot request failed"
                );

            }


            setChatMessages(
                previous => [

                    ...previous,

                    {
                        role:
                            "assistant",

                        content:
                            data.answer
                    }

                ]
            );


        } catch (error) {

            console.error(
                "Kidney chatbot error:",
                error
            );


            setChatMessages(
                previous => [

                    ...previous,

                    {
                        role:
                            "assistant",

                        content:
                            "I'm sorry, I couldn't process your question right now. Please check that the AI backend is running."
                    }

                ]
            );


        } finally {

            setChatLoading(false);

        }

    };


    // =====================================================
    // CLEAR CHAT
    // =====================================================

    const clearChat = () => {

        setChatMessages([]);

        setChatInput("");

    };


    // =====================================================
    // RENDER
    // =====================================================

    return (

        <div className="kidney-page">


            {/* =================================================
                BACK
            ================================================= */}

            <button
                className="back-home"
                onClick={() =>
                    navigate("/")
                }
            >

                <FaArrowLeft />

                Back to Home

            </button>


            {/* =================================================
                HEADER
            ================================================= */}

            <header className="disease-header">

                <div className="disease-icon">

                    <FaHeartbeat />

                </div>


                <div>

                    <h1>
                        Kidney Disease Prediction
                    </h1>

                    <p>
                        AI Powered Kidney Health Assessment
                    </p>

                </div>

            </header>


            {/* =================================================
                PERSONAL + REPORT
            ================================================= */}

            <div className="top-grid">


                {/* PATIENT */}

                <section className="glass-card">

                    <h2>
                        Patient Information
                    </h2>


                    <div className="form-grid">


                        <div className="form-group">

                            <label>
                                Full Name
                            </label>

                            <input
                                type="text"
                                placeholder="Enter Name"
                                value={name}
                                onChange={e =>
                                    setName(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Age
                            </label>

                            <input
                                type="number"
                                min="1"
                                max="120"
                                value={age}
                                onChange={e =>
                                    setAge(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Gender
                            </label>

                            <select
                                value={gender}
                                onChange={e =>
                                    setGender(
                                        e.target.value
                                    )
                                }
                            >

                                <option value="Male">
                                    Male
                                </option>

                                <option value="Female">
                                    Female
                                </option>

                            </select>

                        </div>


                        <div className="form-group">

                            <label>
                                Height (cm)
                            </label>

                            <input
                                type="number"
                                min="50"
                                max="250"
                                value={height}
                                onChange={e =>
                                    setHeight(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Weight (kg)
                            </label>

                            <input
                                type="number"
                                min="10"
                                max="250"
                                value={weight}
                                onChange={e =>
                                    setWeight(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                BMI
                            </label>

                            <input
                                value={
                                    calculateBMI()
                                }
                                readOnly
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                BMI Category
                            </label>

                            <input
                                value={
                                    getBMICategory()
                                }
                                readOnly
                            />

                        </div>

                    </div>

                </section>


                {/* REPORT */}

                <section className="glass-card">

                    <h2>
                        Upload Medical Report
                    </h2>


                    <div
                        className="upload-box"
                        onClick={() =>
                            document
                                .getElementById(
                                    "kidney-file"
                                )
                                ?.click()
                        }
                    >

                        <FaCloudUploadAlt
                            className="upload-icon"
                        />

                        <h3>

                            {uploading
                                ? "Processing Report..."
                                : "Drag & Drop Report"}

                        </h3>


                        <p>
                            Upload PDF, JPG or PNG report
                        </p>


                        <button
                            type="button"
                            className="browse-btn"
                        >

                            {file
                                ? file.name
                                : "Browse Files"}

                        </button>


                        <input
                            id="kidney-file"
                            type="file"
                            accept=".pdf,.jpg,.jpeg,.png"
                            hidden
                            onChange={e =>
                                handleFileChange(
                                    e.target.files?.[0]
                                )
                            }
                        />

                    </div>

                </section>

            </div>


            {/* =================================================
                EXTRACTED LAB VALUES
            ================================================= */}

            <section className="glass-card parameters-card">

                <h2>
                    Kidney Health Parameters
                </h2>


                <p className="section-description">

                    Values extracted from your report are
                    filled automatically. Please correct
                    them if necessary.

                </p>


                <div className="form-grid">


                    <div className="form-group">

                        <label>
                            Random Blood Sugar (mg/dL)
                        </label>

                        <input
                            type="number"
                            min="40"
                            max="600"
                            value={values.bgr}
                            onChange={e =>
                                handleValueChange(
                                    "bgr",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Blood Urea (mg/dL)
                        </label>

                        <input
                            type="number"
                            min="1"
                            max="300"
                            value={values.bu}
                            onChange={e =>
                                handleValueChange(
                                    "bu",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Serum Creatinine (mg/dL)
                        </label>

                        <input
                            type="number"
                            min="0.1"
                            max="20"
                            step="0.1"
                            value={values.sc}
                            onChange={e =>
                                handleValueChange(
                                    "sc",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Sodium (mEq/L)
                        </label>

                        <input
                            type="number"
                            min="100"
                            max="180"
                            value={values.sod}
                            onChange={e =>
                                handleValueChange(
                                    "sod",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Potassium (mEq/L)
                        </label>

                        <input
                            type="number"
                            min="1"
                            max="10"
                            step="0.1"
                            value={values.pot}
                            onChange={e =>
                                handleValueChange(
                                    "pot",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Hemoglobin (g/dL)
                        </label>

                        <input
                            type="number"
                            min="1"
                            max="25"
                            step="0.1"
                            value={values.hemo}
                            onChange={e =>
                                handleValueChange(
                                    "hemo",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Packed Cell Volume (%)
                        </label>

                        <input
                            type="number"
                            min="10"
                            max="70"
                            value={values.pcv}
                            onChange={e =>
                                handleValueChange(
                                    "pcv",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            White Blood Cell Count
                        </label>

                        <input
                            type="number"
                            min="1000"
                            max="50000"
                            value={values.wc}
                            onChange={e =>
                                handleValueChange(
                                    "wc",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Red Blood Cell Count
                        </label>

                        <input
                            type="number"
                            min="1"
                            max="10"
                            step="0.1"
                            value={values.rc}
                            onChange={e =>
                                handleValueChange(
                                    "rc",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    {/* BP */}

                    <div className="form-group">

                        <label>
                            Blood Pressure (mmHg)
                        </label>

                        <input
                            type="number"
                            min="40"
                            max="250"
                            value={bp}
                            onChange={e =>
                                setBp(
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    {/* SG */}

                    <div className="form-group">

                        <label>
                            Urine Specific Gravity
                        </label>

                        <select
                            value={sg}
                            onChange={e =>
                                setSg(
                                    e.target.value
                                )
                            }
                        >

                            <option value="1.005">
                                1.005
                            </option>

                            <option value="1.010">
                                1.010
                            </option>

                            <option value="1.015">
                                1.015
                            </option>

                            <option value="1.020">
                                1.020
                            </option>

                            <option value="1.025">
                                1.025
                            </option>

                        </select>

                    </div>


                    {/* PROTEIN */}

                    <div className="form-group">

                        <label>
                            Protein in Urine
                        </label>

                        <select
                            value={protein}
                            onChange={e =>
                                setProtein(
                                    e.target.value
                                )
                            }
                        >

                            <option>
                                No
                            </option>

                            <option>
                                A small amount
                            </option>

                            <option>
                                A moderate amount
                            </option>

                            <option>
                                A large amount
                            </option>

                            <option>
                                A very large amount
                            </option>

                            <option>
                                I don't know
                            </option>

                        </select>

                    </div>


                    {/* SUGAR */}

                    <div className="form-group">

                        <label>
                            Sugar in Urine
                        </label>

                        <select
                            value={sugar}
                            onChange={e =>
                                setSugar(
                                    e.target.value
                                )
                            }
                        >

                            <option>
                                No
                            </option>

                            <option>
                                A small amount
                            </option>

                            <option>
                                A moderate amount
                            </option>

                            <option>
                                A large amount
                            </option>

                            <option>
                                A very large amount
                            </option>

                            <option>
                                I don't know
                            </option>

                        </select>

                    </div>


                    {/* YES / NO FIELDS */}

                    <YesNoField
                        label="Abnormal Red Blood Cells in Urine"
                        value={rbc}
                        setValue={setRbc}
                    />

                    <YesNoField
                        label="Pus Cells in Urine"
                        value={pc}
                        setValue={setPc}
                    />

                    <YesNoField
                        label="Clumps of Pus Cells"
                        value={pcc}
                        setValue={setPcc}
                    />

                    <YesNoField
                        label="Bacteria in Urine"
                        value={ba}
                        setValue={setBa}
                    />

                    <YesNoField
                        label="High Blood Pressure"
                        value={htn}
                        setValue={setHtn}
                    />

                    <YesNoField
                        label="Diabetes"
                        value={dm}
                        setValue={setDm}
                    />

                    <YesNoField
                        label="Heart Problem"
                        value={cad}
                        setValue={setCad}
                    />

                    <YesNoField
                        label="Reduced Appetite"
                        value={appet}
                        setValue={setAppet}
                    />

                    <YesNoField
                        label="Swelling of Feet or Ankles"
                        value={pe}
                        setValue={setPe}
                    />

                    <YesNoField
                        label="Anemia"
                        value={ane}
                        setValue={setAne}
                    />

                </div>

            </section>


            {/* =================================================
                CONFIRMATION
            ================================================= */}

            <div className="confirmation-box">

                <label>

                    <input
                        type="checkbox"
                        checked={confirmed}
                        onChange={e =>
                            setConfirmed(
                                e.target.checked
                            )
                        }
                    />

                    <span>
                        I have reviewed all extracted
                        values and confirm they are correct.
                    </span>

                </label>

            </div>


            {/* =================================================
                PREDICT
            ================================================= */}

            <button
                className="predict-btn"
                disabled={!confirmed}
                onClick={handlePredict}
            >

                Analyze Kidney Disease

            </button>


            {/* =================================================
                RESULT
            ================================================= */}

            {result && (

                <section
                    id="kidney-prediction-result"
                    className="glass-card prediction-result"
                >

                    <h2>
                        Kidney Disease Prediction
                    </h2>


                    <div className="risk-banner">

                        <span>
                            {result.overall}
                        </span>

                        <strong>

                            {Number(
                                result.probability || 0
                            ).toFixed(2)}
                            %

                        </strong>

                    </div>


                    <div className="result-grid">


                        <div className="result-item">

                            <span>
                                Patient
                            </span>

                            <strong>
                                {name}
                            </strong>

                        </div>


                        <div className="result-item">

                            <span>
                                Age
                            </span>

                            <strong>
                                {age} years
                            </strong>

                        </div>


                        <div className="result-item">

                            <span>
                                BMI
                            </span>

                            <strong>
                                {Number(
                                    result.bmi || 0
                                ).toFixed(2)}
                            </strong>

                        </div>


                        <div className="result-item">

                            <span>
                                BMI Category
                            </span>

                            <strong>
                                {
                                    result.bmiCategory
                                }
                            </strong>

                        </div>

                    </div>


                    {result.summary && (

                        <div className="result-section">

                            <h3>
                                Summary
                            </h3>

                            <p>
                                {result.summary}
                            </p>

                        </div>

                    )}


                    {result.health_effects?.length > 0 && (

                        <div className="result-section">

                            <h3>
                                Possible Health Effects
                            </h3>

                            {result.health_effects.map(
                                (item, index) => (

                                    <p key={index}>
                                        ⚠ {item}
                                    </p>

                                )
                            )}

                        </div>

                    )}


                    {result.diet?.length > 0 && (

                        <div className="result-section">

                            <h3>
                                Diet Recommendations
                            </h3>

                            {result.diet.map(
                                (item, index) => (

                                    <p key={index}>
                                        ✓ {item}
                                    </p>

                                )
                            )}

                        </div>

                    )}


                    {result.lifestyle?.length > 0 && (

                        <div className="result-section">

                            <h3>
                                Lifestyle Recommendations
                            </h3>

                            {result.lifestyle.map(
                                (item, index) => (

                                    <p key={index}>
                                        ✓ {item}
                                    </p>

                                )
                            )}

                        </div>

                    )}


                    {result.medical?.length > 0 && (

                        <div className="result-section">

                            <h3>
                                Medical Advice
                            </h3>

                            {result.medical.map(
                                (item, index) => (

                                    <p key={index}>
                                        🩺 {item}
                                    </p>

                                )
                            )}

                        </div>

                    )}


                    <div className="disclaimer">

                        This prediction is generated by
                        a machine learning model and is
                        not a medical diagnosis. Please
                        consult a qualified healthcare
                        professional.

                    </div>

                </section>

            )}


            {/* =================================================
                AI ASSISTANT
            ================================================= */}

            {result && (

                <section className="glass-card ai-chat-card">

                    <div className="ai-chat-header">

                        <div>

                            <div className="ai-chat-title">

                                <span className="ai-bot-icon">
                                    🤖
                                </span>

                                <h2>
                                    Ask MediSense AI
                                </h2>

                            </div>

                            <p>
                                Ask anything about your
                                prediction, report,
                                symptoms, diet or lifestyle.
                            </p>

                        </div>


                        {chatMessages.length > 0 && (

                            <button
                                className="clear-chat"
                                onClick={clearChat}
                            >
                                🗑 Clear Conversation
                            </button>

                        )}

                    </div>


                    <div className="chat-messages">

                        {chatMessages.map(
                            (message, index) => (

                                <div
                                    key={index}
                                    className={
                                        message.role === "user"
                                            ? "chat-message user-message"
                                            : "chat-message ai-message"
                                    }
                                >

                                    {message.role ===
                                        "assistant" && (

                                        <div className="message-avatar">
                                            🤖
                                        </div>

                                    )}


                                    <div className="message-content">

                                        {String(
                                            message.content || ""
                                        )
                                            .split("\n")
                                            .map(
                                                (
                                                    line,
                                                    lineIndex
                                                ) => (

                                                    <p
                                                        key={
                                                            lineIndex
                                                        }
                                                    >
                                                        {line}
                                                    </p>

                                                )
                                            )}

                                    </div>

                                </div>

                            )
                        )}


                        {chatLoading && (

                            <div className="chat-message ai-message">

                                <div className="message-avatar">
                                    🤖
                                </div>

                                <div className="typing-indicator">

                                    <span></span>
                                    <span></span>
                                    <span></span>

                                    <label>
                                        Thinking...
                                    </label>

                                </div>

                            </div>

                        )}

                    </div>


                    <div className="chat-input-area">

                        <input
                            type="text"
                            placeholder="Ask a follow-up question..."
                            value={chatInput}
                            disabled={chatLoading}
                            onChange={e =>
                                setChatInput(
                                    e.target.value
                                )
                            }
                            onKeyDown={e => {

                                if (
                                    e.key === "Enter" &&
                                    !e.shiftKey
                                ) {

                                    e.preventDefault();

                                    handleChat();

                                }

                            }}
                        />


                        <button
                            onClick={handleChat}
                            disabled={
                                chatLoading ||
                                !chatInput.trim()
                            }
                        >

                            Send

                        </button>

                    </div>

                </section>

            )}

        </div>

    );
}


// =========================================================
// YES / NO COMPONENT
// =========================================================

function YesNoField({
    label,
    value,
    setValue
}) {

    return (

        <div className="form-group">

            <label>
                {label}
            </label>

            <select
                value={value}
                onChange={e =>
                    setValue(
                        e.target.value
                    )
                }
            >

                <option value="No">
                    No
                </option>

                <option value="Yes">
                    Yes
                </option>

            </select>

        </div>

    );

}