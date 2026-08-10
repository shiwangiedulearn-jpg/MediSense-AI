import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft, FaHeartbeat, FaCloudUploadAlt } from "react-icons/fa";
import "./Diabetes.css";

export default function Diabetes() {

    const navigate = useNavigate();

    // -----------------------------
    // PERSONAL DETAILS
    // -----------------------------

    const [name, setName] = useState("");
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("Male");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");

    // -----------------------------
    // REPORT
    // -----------------------------

    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);

    // -----------------------------
    // DIABETES VALUES
    // -----------------------------

    const [values, setValues] = useState({
        Pregnancies: 0,
        Glucose: 120,
        BloodPressure: 80,
        SkinThickness: 20,
        Insulin: 80,
        BMI: 22.0,
        DiabetesPedigreeFunction: 0.47,
    });

    // -----------------------------
    // RESULT
    // -----------------------------

    const [result, setResult] = useState(null);

    const [confirmed, setConfirmed] = useState(false);

    // -----------------------------
    // CHATBOT
    // -----------------------------

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

    // =====================================================
    // PERSONAL DETAILS CHANGE
    // =====================================================

    const handleHeightChange = (value) => {

        setHeight(value);

        const h = Number(value) / 100;
        const w = Number(weight);

        if (h && w) {

            setValues((previous) => ({
                ...previous,
                BMI: Number((w / (h * h)).toFixed(2))
            }));

        }
    };


    const handleWeightChange = (value) => {

        setWeight(value);

        const h = Number(height) / 100;
        const w = Number(value);

        if (h && w) {

            setValues((previous) => ({
                ...previous,
                BMI: Number((w / (h * h)).toFixed(2))
            }));

        }
    };

    // =====================================================
    // INPUT CHANGE
    // =====================================================

    const handleValueChange = (field, value) => {

        setValues((previous) => ({
            ...previous,
            [field]: value
        }));

    };

    // =====================================================
    // REPORT UPLOAD
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
                "http://127.0.0.1:8000/diabetes/extract",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {

                const errorText =
                    await response.text();

                console.error(
                    "Diabetes extraction error:",
                    errorText
                );

                throw new Error(
                    "Report extraction failed"
                );
            }

            const data =
                await response.json();

            console.log(
                "Extracted diabetes values:",
                data
            );

            if (data.values) {

                setValues((previous) => ({
                    ...previous,
                    ...data.values
                }));

            }

        } catch (error) {

            console.error(
                "Report processing error:",
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
    // PREDICT
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

            const response = await fetch(
                "http://127.0.0.1:8000/diabetes/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name,

                        age: Number(age),

                        gender,

                        height: Number(height),

                        weight: Number(weight),

                        values: {

                            Pregnancies:
                                Number(values.Pregnancies),

                            Glucose:
                                Number(values.Glucose),

                            BloodPressure:
                                Number(values.BloodPressure),

                            SkinThickness:
                                Number(values.SkinThickness),

                            Insulin:
                                Number(values.Insulin),

                            BMI:
                                Number(values.BMI),

                            DiabetesPedigreeFunction:
                                Number(
                                    values.DiabetesPedigreeFunction
                                )

                        }

                    })
                }
            );

            if (!response.ok) {

                const errorText =
                    await response.text();

                console.error(
                    "Diabetes prediction error:",
                    errorText
                );

                throw new Error(
                    "Prediction failed"
                );
            }

            const data =
                await response.json();

            console.log(
                "Diabetes prediction:",
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
                "Prediction error:",
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

        const userMessage = {
            role: "user",
            content: chatInput
        };

        const updatedMessages = [
            ...chatMessages,
            userMessage
        ];

        setChatMessages(updatedMessages);
        setChatInput("");
        setChatLoading(true);

        try {

            const history =
                updatedMessages
                    .map(
                        (message) =>
                            `${message.role}: ${message.content}`
                    )
                    .join("\n");

            const context = {

                module:
                    "Diabetes Prediction",

                patient: {
                    name,
                    age: Number(age),
                    gender,
                    height: Number(height),
                    weight: Number(weight)
                },

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

                bmi:
                    result.bmi,

                values:
                    result.values || values,

                health_effects:
                    result.health_effects,

                diet:
                    result.diet,

                lifestyle:
                    result.lifestyle,

                medical:
                    result.medical,

                factors:
                    result.factors || []

            };

            const response = await fetch(
                "http://127.0.0.1:8000/diabetes/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        message: chatInput,

                        context: context,

                        history: updatedMessages

                    })
                }
            );

            if (!response.ok) {

                const errorText =
                    await response.text();

                console.error(
                    "Chat API error:",
                    errorText
                );

                throw new Error(
                    `Chat API failed: ${response.status}`
                );
            }

            const data =
                await response.json();

            const assistantMessage = {

                role: "assistant",

                content:
                    data.answer ||
                    data.response ||
                    "I couldn't generate a response. Please try again."

            };

            setChatMessages(
                (previous) => [
                    ...previous,
                    assistantMessage
                ]
            );

        } catch (error) {

            console.error(
                "Chatbot error:",
                error
            );

            setChatMessages(
                (previous) => [
                    ...previous,

                    {
                        role: "assistant",

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

        <div className="diabetes-page">

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
                        Diabetes Prediction
                    </h1>

                    <p>
                        AI Powered Diabetes Risk Assessment
                    </p>

                </div>

            </header>


            {/* =================================================
                TOP SECTION
            ================================================= */}

            <div className="top-grid">

                {/* PATIENT */}

                <section className="glass-card patient-card">

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
                                onChange={(e) =>
                                    setName(e.target.value)
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
                                onChange={(e) =>
                                    setAge(e.target.value)
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Gender
                            </label>

                            <select
                                value={gender}
                                onChange={(e) =>
                                    setGender(e.target.value)
                                }
                            >
                                <option>
                                    Male
                                </option>

                                <option>
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
                                onChange={(e) =>
                                    handleHeightChange(
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
                                max="300"
                                value={weight}
                                onChange={(e) =>
                                    handleWeightChange(
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

                    </div>

                </section>


                {/* UPLOAD */}

                <section className="glass-card upload-card">

                    <h2>
                        Upload Medical Report
                    </h2>

                    <div
                        className="upload-box"
                        onClick={() =>
                            document
                                .getElementById(
                                    "diabetes-file"
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
                            id="diabetes-file"
                            type="file"
                            accept=".pdf,.jpg,.jpeg,.png"
                            hidden
                            onChange={(e) =>
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
                    Medical Parameters
                </h2>

                <div className="form-grid">

                    <div className="form-group">

                        <label>
                            Pregnancies
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="20"
                            value={values.Pregnancies}
                            onChange={(e) =>
                                handleValueChange(
                                    "Pregnancies",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Glucose
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="500"
                            value={values.Glucose}
                            onChange={(e) =>
                                handleValueChange(
                                    "Glucose",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Blood Pressure
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="250"
                            value={values.BloodPressure}
                            onChange={(e) =>
                                handleValueChange(
                                    "BloodPressure",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Skin Thickness
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="100"
                            value={values.SkinThickness}
                            onChange={(e) =>
                                handleValueChange(
                                    "SkinThickness",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Insulin
                        </label>

                        <input
                            type="number"
                            min="0"
                            max="1000"
                            value={values.Insulin}
                            onChange={(e) =>
                                handleValueChange(
                                    "Insulin",
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
                            type="number"
                            step="0.01"
                            min="0"
                            max="100"
                            value={values.BMI}
                            onChange={(e) =>
                                handleValueChange(
                                    "BMI",
                                    e.target.value
                                )
                            }
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Diabetes Pedigree Function
                        </label>

                        <input
                            type="number"
                            step="0.01"
                            min="0"
                            max="3"
                            value={
                                values.DiabetesPedigreeFunction
                            }
                            onChange={(e) =>
                                handleValueChange(
                                    "DiabetesPedigreeFunction",
                                    e.target.value
                                )
                            }
                        />

                    </div>

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
                        onChange={(e) =>
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


            {/* =================================================
                PREDICT BUTTON
            ================================================= */}

            <button
                className="predict-btn"
                onClick={handlePredict}
            >
                Predict Diabetes
            </button>


            {/* =================================================
                RESULT
            ================================================= */}

            {result && (

                <section
                    id="prediction-result"
                    className="prediction-result glass-card"
                >

                    <h2>
                        Prediction Result
                    </h2>

                    <div className="risk-banner">

                        <span>
                            {result.overall ||
                                (result.prediction === 1
                                    ? "Higher Risk of Diabetes"
                                    : "Low Risk of Diabetes")}
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
                                    result.bmi || values.BMI
                                ).toFixed(2)}
                            </strong>

                        </div>


                        <div className="result-item">

                            <span>
                                Glucose
                            </span>

                            <strong>
                                {values.Glucose}
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
                                        {result.health_effects}
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
                                Medical Guidance
                            </h3>

                            {Array.isArray(
                                result.medical
                            )
                                ? result.medical.map(
                                    (item, index) => (
                                        <p key={index}>
                                            • {item}
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

                <section
                    id="ai-chat"
                    className="ai-chat-card glass-card"
                >

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

                        {chatMessages.length === 0 && (

                            <div className="chat-empty">

                                <div className="chat-empty-icon">
                                    🤖
                                </div>

                                <h3>
                                    How can I help you?
                                </h3>

                                <p>
                                    Ask about your prediction,
                                    medical values, diet,
                                    lifestyle or symptoms.
                                </p>

                            </div>

                        )}


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
                            onChange={(e) =>
                                setChatInput(
                                    e.target.value
                                )
                            }
                            onKeyDown={(e) => {

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