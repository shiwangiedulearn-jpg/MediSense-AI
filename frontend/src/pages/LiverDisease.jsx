import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    FaArrowLeft,
    FaHeartbeat,
    FaCloudUploadAlt
} from "react-icons/fa";

import "./LiverDisease.css";

export default function LiverDisease() {

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
    // LIVER VALUES
    // =====================================================

    const [values, setValues] = useState({
        tot_bilirubin: 1.0,
        direct_bilirubin: 0.2,
        alkphos: 150,
        sgpt: 40,
        sgot: 40,
        tot_proteins: 7.0,
        albumin: 4.0,
        ag_ratio: 1.2
    });

    // =====================================================
    // RESULT
    // =====================================================

    const [result, setResult] = useState(null);
    const [confirmed, setConfirmed] = useState(false);

    // =====================================================
    // CHATBOT
    // =====================================================

    const [chatInput, setChatInput] = useState("");
    const [chatMessages, setChatMessages] = useState([]);
    const [chatLoading, setChatLoading] = useState(false);

    // =====================================================
    // BMI
    // =====================================================

    const calculateBMI = () => {

        if (!height || !weight) {
            return "--";
        }

        const h = Number(height) / 100;
        const w = Number(weight);

        if (!h || !w) {
            return "--";
        }

        return (w / (h * h)).toFixed(2);
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
    // VALUE CHANGE
    // =====================================================

    const handleValueChange = (field, value) => {

        setValues(previous => ({
            ...previous,
            [field]: value
        }));

    };

    // =====================================================
    // REPORT UPLOAD + EXTRACTION
    // =====================================================

    const handleFileChange = async (selectedFile) => {

        if (!selectedFile) {
            return;
        }

        setFile(selectedFile);
        setUploading(true);

        try {

            const formData = new FormData();

            formData.append(
                "file",
                selectedFile
            );

            const response = await fetch(
                "https://medisense-ai-4zpl.onrender.com/liver/extract",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Report extraction failed"
                );

            }

            console.log(
                "Extracted Liver values:",
                data
            );

            if (data.values) {

                setValues(previous => ({
                    ...previous,
                    ...data.values
                }));

            }

        } catch (error) {

            console.error(
                "Liver extraction error:",
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
    // PREDICTION
    // =====================================================

    const handlePredict = async () => {

        if (!name.trim()) {

            alert("Please enter your name.");
            return;

        }

        if (!age) {

            alert("Please enter your age.");
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

            const response = await fetch(
                "https://medisense-ai-4zpl.onrender.com/liver/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name: name,

                        age: Number(age),

                        gender: gender,

                        height: Number(height),

                        weight: Number(weight),

                        values: {

                            tot_bilirubin:
                                Number(
                                    values.tot_bilirubin
                                ),

                            direct_bilirubin:
                                Number(
                                    values.direct_bilirubin
                                ),

                            alkphos:
                                Number(
                                    values.alkphos
                                ),

                            sgpt:
                                Number(
                                    values.sgpt
                                ),

                            sgot:
                                Number(
                                    values.sgot
                                ),

                            tot_proteins:
                                Number(
                                    values.tot_proteins
                                ),

                            albumin:
                                Number(
                                    values.albumin
                                ),

                            ag_ratio:
                                Number(
                                    values.ag_ratio
                                )

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
                "Liver prediction:",
                data
            );

            setResult(data);

            setTimeout(() => {

                document
                    .getElementById(
                        "prediction-result"
                    )
                    ?.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

            }, 100);

        } catch (error) {

            console.error(
                "Liver prediction error:",
                error
            );

            alert(
                "Prediction failed. Please make sure the backend is running."
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

        const question = chatInput.trim();

        const userMessage = {
            role: "user",
            content: question
        };

        const updatedMessages = [
            ...chatMessages,
            userMessage
        ];

        setChatMessages(updatedMessages);
        setChatInput("");
        setChatLoading(true);

        try {

            const context = {

                module: "Liver Disease",

                patient: {
                    name: name,
                    age: Number(age),
                    gender: gender,
                    height: Number(height),
                    weight: Number(weight)
                },

                bmi: result.bmi,

                bmiCategory:
                    result.bmiCategory,

                prediction: {
                    prediction:
                        result.prediction,

                    probability:
                        result.probability,

                    overall:
                        result.overall,

                    summary:
                        result.summary
                },

                values:
                    result.values || values,

                health_effects:
                    result.health_effects,

                diet:
                    result.diet,

                lifestyle:
                    result.lifestyle,

                medical:
                    result.medical

            };

            const response = await fetch(
                "https://medisense-ai-4zpl.onrender.com/liver/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        message: question,

                        context: context,

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

            setChatMessages(previous => [

                ...previous,

                {
                    role: "assistant",
                    content:
                        data.answer
                }

            ]);

        } catch (error) {

            console.error(
                "Liver chatbot error:",
                error
            );

            setChatMessages(previous => [

                ...previous,

                {
                    role: "assistant",
                    content:
                        "I'm sorry, I couldn't process your question right now. Please check that the AI backend is running."
                }

            ]);

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

        <div className="liver-page">

            {/* BACK */}

            <button
                className="back-home"
                onClick={() => navigate("/")}
            >

                <FaArrowLeft />

                Back to Home

            </button>


            {/* HEADER */}

            <header className="disease-header">

                <div className="disease-icon">
                    <FaHeartbeat />
                </div>

                <div>

                    <h1>
                        Liver Disease Prediction
                    </h1>

                    <p>
                        AI Powered Liver Health Assessment
                    </p>

                </div>

            </header>


            {/* =================================================
                PATIENT + UPLOAD
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
                                value={calculateBMI()}
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


                {/* UPLOAD */}

                <section className="glass-card">

                    <h2>
                        Upload Medical Report
                    </h2>

                    <div
                        className="upload-box"
                        onClick={() =>
                            document
                                .getElementById(
                                    "liver-file"
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
                            id="liver-file"
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
                MEDICAL PARAMETERS
            ================================================= */}

            <section className="glass-card parameters-card">

                <h2>
                    Liver Function Parameters
                </h2>

                <div className="form-grid">

                    <div className="form-group">

                        <label>
                            Total Bilirubin (mg/dL)
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="50"
                            step="0.1"
                            value={
                                values.tot_bilirubin
                            }
                            onChange={e =>
                                handleValueChange(
                                    "tot_bilirubin",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Direct Bilirubin (mg/dL)
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="25"
                            step="0.1"
                            value={
                                values.direct_bilirubin
                            }
                            onChange={e =>
                                handleValueChange(
                                    "direct_bilirubin",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Alkaline Phosphatase (IU/L)
                        </label>

                        <input
                            type="number"
                            min="20"
                            max="2500"
                            value={
                                values.alkphos
                            }
                            onChange={e =>
                                handleValueChange(
                                    "alkphos",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            SGPT / ALT (IU/L)
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="3000"
                            value={values.sgpt}
                            onChange={e =>
                                handleValueChange(
                                    "sgpt",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            SGOT / AST (IU/L)
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="3000"
                            value={values.sgot}
                            onChange={e =>
                                handleValueChange(
                                    "sgot",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Total Proteins (g/dL)
                        </label>

                        <input
                            type="number"
                            min="2"
                            max="15"
                            step="0.1"
                            value={
                                values.tot_proteins
                            }
                            onChange={e =>
                                handleValueChange(
                                    "tot_proteins",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Albumin (g/dL)
                        </label>

                        <input
                            type="number"
                            min="1"
                            max="10"
                            step="0.1"
                            value={values.albumin}
                            onChange={e =>
                                handleValueChange(
                                    "albumin",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Albumin / Globulin Ratio
                        </label>

                        <input
                            type="number"
                            min="0.1"
                            max="5"
                            step="0.01"
                            value={
                                values.ag_ratio
                            }
                            onChange={e =>
                                handleValueChange(
                                    "ag_ratio",
                                    e.target.value
                                )
                            }
                        />

                    </div>

                </div>

            </section>


            {/* CONFIRMATION */}

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
                        I confirm that all the above
                        values are correct.
                    </span>

                </label>

            </div>


            {/* PREDICT */}

            <button
                className="predict-btn"
                onClick={handlePredict}
            >

                Predict Liver Disease

            </button>


            {/* =================================================
                RESULT
            ================================================= */}

            {result && (

                <section
                    id="prediction-result"
                    className="glass-card prediction-result"
                >

                    <h2>
                        Prediction Result
                    </h2>


                    <div className="risk-banner">

                        <span>

                            {result.overall ||
                                (
                                    result.prediction === 1
                                        ? "Higher Risk of Liver Disease"
                                        : "Low Risk of Liver Disease"
                                )}

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
                                    result.bmiCategory ||
                                    getBMICategory()
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


                    {result.health_effects && (

                        <div className="result-section">

                            <h3>
                                Possible Health Effects
                            </h3>

                            {Array.isArray(
                                result.health_effects
                            )
                                ? result.health_effects.map(
                                    (item, index) => (
                                        <p key={index}>
                                            • {item}
                                        </p>
                                    )
                                )
                                : (
                                    <p>
                                        {
                                            result.health_effects
                                        }
                                    </p>
                                )}

                        </div>

                    )}


                    {result.diet && (

                        <div className="result-section">

                            <h3>
                                Diet Recommendations
                            </h3>

                            {Array.isArray(
                                result.diet
                            )
                                ? result.diet.map(
                                    (item, index) => (
                                        <p key={index}>
                                            ✓ {item}
                                        </p>
                                    )
                                )
                                : (
                                    <p>
                                        {result.diet}
                                    </p>
                                )}

                        </div>

                    )}


                    {result.lifestyle && (

                        <div className="result-section">

                            <h3>
                                Lifestyle Recommendations
                            </h3>

                            {Array.isArray(
                                result.lifestyle
                            )
                                ? result.lifestyle.map(
                                    (item, index) => (
                                        <p key={index}>
                                            ✓ {item}
                                        </p>
                                    )
                                )
                                : (
                                    <p>
                                        {result.lifestyle}
                                    </p>
                                )}

                        </div>

                    )}


                    {result.medical && (

                        <div className="result-section">

                            <h3>
                                Medical Advice
                            </h3>

                            {Array.isArray(
                                result.medical
                            )
                                ? result.medical.map(
                                    (item, index) => (
                                        <p key={index}>
                                            🩺 {item}
                                        </p>
                                    )
                                )
                                : (
                                    <p>
                                        {result.medical}
                                    </p>
                                )}

                        </div>

                    )}


                    <div className="disclaimer">

                        This prediction is generated by a
                        machine learning model and is not a
                        medical diagnosis. Please consult a
                        qualified healthcare professional.

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
                                prediction, report, symptoms,
                                diet or lifestyle.
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