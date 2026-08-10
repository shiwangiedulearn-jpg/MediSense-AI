import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    FaArrowLeft,
    FaTint,
    FaCloudUploadAlt
} from "react-icons/fa";

import "./LipidProfile.css";

export default function LipidProfile() {

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
    // LIPID VALUES
    // =====================================================

    const [values, setValues] = useState({
        total_cholesterol: 200,
        ldl: 100,
        vldl: 30,
        hdl: 50,
        triglycerides: 150,
        total_lipids: 600
    });

    // =====================================================
    // VERIFICATION
    // =====================================================

    const [verified, setVerified] = useState(false);

    // =====================================================
    // RESULT
    // =====================================================

    const [result, setResult] = useState(null);

    // =====================================================
    // CHAT
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
    // CHANGE VALUE
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
    // UPLOAD + EXTRACT
    // =====================================================

    const handleFileChange = async (
        selectedFile
    ) => {

        if (!selectedFile) {
            return;
        }

        setFile(selectedFile);
        setUploading(true);
        setResult(null);
        setVerified(false);

        try {

            const formData = new FormData();

            formData.append(
                "file",
                selectedFile
            );

            const response = await fetch(
                "http://127.0.0.1:8000/lipid/extract",
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
                "Lipid extraction error:",
                error
            );

            alert(
                error.message ||
                "Could not process the report."
            );

        } finally {

            setUploading(false);

        }

    };


    // =====================================================
    // ANALYZE
    // =====================================================

    const handleAnalyze = async () => {

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

        if (!verified) {

            alert(
                "Please confirm that all extracted values are correct."
            );

            return;

        }


        try {

            const response = await fetch(
                "http://127.0.0.1:8000/lipid/predict",
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

                            total_cholesterol:
                                Number(
                                    values.total_cholesterol
                                ),

                            ldl:
                                Number(
                                    values.ldl
                                ),

                            vldl:
                                Number(
                                    values.vldl
                                ),

                            hdl:
                                Number(
                                    values.hdl
                                ),

                            triglycerides:
                                Number(
                                    values.triglycerides
                                ),

                            total_lipids:
                                Number(
                                    values.total_lipids
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
                    "Lipid analysis failed"
                );

            }


            setResult(data);


            setTimeout(() => {

                document
                    .getElementById(
                        "lipid-result"
                    )
                    ?.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

            }, 100);


        } catch (error) {

            console.error(
                "Lipid analysis error:",
                error
            );

            alert(
                error.message ||
                "Analysis failed."
            );

        }

    };


    // =====================================================
    // CHATBOT
    // =====================================================

    const handleChat = async () => {

        if (!chatInput.trim() || !result) {
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
                    "Lipid Profile",

                prediction:
                    "Rule-based Lipid Profile Analysis",

                confidence:
                    "Rule-based Analysis",

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

                lipid_values: {

                    "Total Cholesterol":
                        values.total_cholesterol,

                    "Triglycerides":
                        values.triglycerides,

                    "HDL":
                        values.hdl,

                    "LDL":
                        values.ldl,

                    "VLDL":
                        values.vldl,

                    "Total Lipids":
                        values.total_lipids

                },

                overall:
                    result.overall,

                summary:
                    result.summary,

                results:
                    result.results,

                health_effects:
                    result.health_effects,

                diet:
                    result.diet,

                lifestyle:
                    result.lifestyle,

                medical_advice:
                    result.medical

            };


            const response = await fetch(
                "http://127.0.0.1:8000/lipid/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

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
                "Lipid chatbot error:",
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
    // STATUS CLASS
    // =====================================================

    const getStatusClass = (status) => {

        if (!status) {
            return "";
        }

        if (status === "Healthy") {
            return "healthy";
        }

        if (
            status
                .toLowerCase()
                .includes("borderline")
        ) {
            return "borderline";
        }

        return "high";
    };


    // =====================================================
    // RENDER
    // =====================================================

    return (

        <div className="lipid-page">


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

                    <FaTint />

                </div>

                <div>

                    <h1>
                        Lipid Profile Analysis
                    </h1>

                    <p>
                        AI-Powered Cholesterol & Lipid Health Assessment
                    </p>

                </div>

            </header>


            {/* =================================================
                PERSONAL INFORMATION
            ================================================= */}

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

                </div>


                {/* BMI */}

                <div className="bmi-grid">

                    <div className="bmi-card">

                        <span>
                            BMI
                        </span>

                        <strong>
                            {calculateBMI()}
                        </strong>

                    </div>


                    <div className="bmi-card">

                        <span>
                            BMI Category
                        </span>

                        <strong>
                            {getBMICategory()}
                        </strong>

                    </div>

                </div>

            </section>


            {/* =================================================
                UPLOAD
            ================================================= */}

            <section className="glass-card upload-card">

                <h2>
                    Upload Medical Report
                </h2>

                <div
                    className="upload-box"
                    onClick={() =>
                        document
                            .getElementById(
                                "lipid-file"
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
                            : "Upload Your Lipid Report"}

                    </h3>

                    <p>
                        PDF, JPG or PNG
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
                        id="lipid-file"
                        type="file"
                        accept=".pdf,.png,.jpg,.jpeg"
                        hidden
                        onChange={e =>
                            handleFileChange(
                                e.target.files?.[0]
                            )
                        }
                    />

                </div>

            </section>


            {/* =================================================
                EXTRACTED VALUES
            ================================================= */}

            {file && (

                <section className="glass-card values-card">

                    <h2>
                        Review Extracted Values
                    </h2>

                    <p className="section-description">

                        Values extracted from your medical
                        report are filled automatically.
                        You can correct any value before
                        continuing.

                    </p>


                    <div className="form-grid">

                        <div className="form-group">

                            <label>
                                Total Cholesterol (mg/dL)
                            </label>

                            <input
                                type="number"
                                min="0"
                                value={
                                    values.total_cholesterol
                                }
                                onChange={e =>
                                    handleValueChange(
                                        "total_cholesterol",
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                LDL Cholesterol (mg/dL)
                            </label>

                            <input
                                type="number"
                                min="0"
                                value={
                                    values.ldl
                                }
                                onChange={e =>
                                    handleValueChange(
                                        "ldl",
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                VLDL Cholesterol (mg/dL)
                            </label>

                            <input
                                type="number"
                                min="0"
                                value={
                                    values.vldl
                                }
                                onChange={e =>
                                    handleValueChange(
                                        "vldl",
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                HDL Cholesterol (mg/dL)
                            </label>

                            <input
                                type="number"
                                min="0"
                                value={
                                    values.hdl
                                }
                                onChange={e =>
                                    handleValueChange(
                                        "hdl",
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Triglycerides (mg/dL)
                            </label>

                            <input
                                type="number"
                                min="0"
                                value={
                                    values.triglycerides
                                }
                                onChange={e =>
                                    handleValueChange(
                                        "triglycerides",
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Serum Total Lipids (mg/dL)
                            </label>

                            <input
                                type="number"
                                min="0"
                                value={
                                    values.total_lipids
                                }
                                onChange={e =>
                                    handleValueChange(
                                        "total_lipids",
                                        e.target.value
                                    )
                                }
                            />

                        </div>

                    </div>

                </section>

            )}


            {/* =================================================
                VERIFICATION
            ================================================= */}

            {file && (

                <div className="confirmation-box">

                    <label>

                        <input
                            type="checkbox"
                            checked={verified}
                            onChange={e =>
                                setVerified(
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

            )}


            {/* =================================================
                ANALYZE
            ================================================= */}

            {file && (

                <button
                    className="analyze-btn"
                    disabled={!verified}
                    onClick={handleAnalyze}
                >

                    Analyze Lipid Profile

                </button>

            )}


            {/* =================================================
                RESULT
            ================================================= */}

            {result && (

                <section
                    id="lipid-result"
                    className="glass-card result-card"
                >

                    <div className="completed-label">
                        ✓ Analysis Completed
                    </div>


                    {/* Patient */}

                    <div className="patient-summary">

                        <div>
                            <span>Name</span>
                            <strong>
                                {result.name}
                            </strong>
                        </div>

                        <div>
                            <span>Age</span>
                            <strong>
                                {result.age} years
                            </strong>
                        </div>

                        <div>
                            <span>Gender</span>
                            <strong>
                                {result.gender}
                            </strong>
                        </div>

                        <div>
                            <span>Height</span>
                            <strong>
                                {result.height} cm
                            </strong>
                        </div>

                        <div>
                            <span>Weight</span>
                            <strong>
                                {result.weight} kg
                            </strong>
                        </div>

                        <div>
                            <span>BMI</span>
                            <strong>
                                {Number(
                                    result.bmi
                                ).toFixed(2)}
                            </strong>
                        </div>

                        <div>
                            <span>BMI Category</span>
                            <strong>
                                {result.bmiCategory}
                            </strong>
                        </div>

                    </div>


                    {/* Overall */}

                    <div className="overall-box">

                        <h2>
                            {result.overall}
                        </h2>

                        <p>
                            {result.summary}
                        </p>

                    </div>


                    {/* =================================================
                        RESULTS TABLE
                    ================================================= */}

                    <h2 className="result-heading">
                        Lipid Profile Results
                    </h2>


                    <div className="table-wrapper">

                        <table className="lipid-table">

                            <thead>

                                <tr>

                                    <th>
                                        Test
                                    </th>

                                    <th>
                                        Value
                                    </th>

                                    <th>
                                        Clinical Range
                                    </th>

                                    <th>
                                        Status
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {result.results &&
                                    Object.entries(
                                        result.results
                                    ).map(
                                        (
                                            [
                                                test,
                                                info
                                            ],
                                            index
                                        ) => (

                                            <tr
                                                key={
                                                    index
                                                }
                                            >

                                                <td>
                                                    {test}
                                                </td>

                                                <td>
                                                    {
                                                        info.value
                                                    }{" "}
                                                    mg/dL
                                                </td>

                                                <td>
                                                    {
                                                        info.range
                                                    }
                                                </td>

                                                <td>

                                                    <span
                                                        className={`status-pill ${getStatusClass(
                                                            info.status
                                                        )}`}
                                                    >

                                                        {
                                                            info.status
                                                        }

                                                    </span>

                                                </td>

                                            </tr>

                                        )
                                    )}

                            </tbody>

                        </table>

                    </div>


                    {/* =================================================
                        HEALTH EFFECTS
                    ================================================= */}

                    {result.health_effects?.length > 0 && (

                        <ResultList
                            title="Possible Health Effects"
                            items={
                                result.health_effects
                            }
                            icon="⚠"
                        />

                    )}


                    {/* =================================================
                        DIET
                    ================================================= */}

                    {result.diet?.length > 0 && (

                        <ResultList
                            title="Diet Recommendations"
                            items={
                                result.diet
                            }
                            icon="✓"
                        />

                    )}


                    {/* =================================================
                        LIFESTYLE
                    ================================================= */}

                    {result.lifestyle?.length > 0 && (

                        <ResultList
                            title="Lifestyle Recommendations"
                            items={
                                result.lifestyle
                            }
                            icon="✓"
                        />

                    )}


                    {/* =================================================
                        MEDICAL
                    ================================================= */}

                    {result.medical?.length > 0 && (

                        <ResultList
                            title="Medical Advice"
                            items={
                                result.medical
                            }
                            icon="🩺"
                        />

                    )}


                    <div className="disclaimer">

                        This is a rule-based lipid profile
                        analysis and is not a confirmed
                        medical diagnosis. Please consult
                        a qualified healthcare professional
                        for medical interpretation.

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
                                Ask anything about your lipid
                                profile, diet, lifestyle or
                                health recommendations.
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
// RESULT LIST COMPONENT
// =========================================================

function ResultList({
    title,
    items,
    icon
}) {

    return (

        <div className="result-section">

            <h3>
                {title}
            </h3>

            {items.map(
                (item, index) => (

                    <div
                        className="info-card"
                        key={index}
                    >

                        <span className="info-icon">
                            {icon}
                        </span>

                        {item}

                    </div>

                )
            )}

        </div>

    );
}