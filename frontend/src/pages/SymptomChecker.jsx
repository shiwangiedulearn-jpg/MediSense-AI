import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    FaArrowLeft,
    FaStethoscope,
    FaChevronDown
} from "react-icons/fa";

import "./SymptomChecker.css";


// =====================================================
// SYMPTOM CATEGORIES
// =====================================================

const symptomCategories = [

    {
        title: "General Symptoms",
        symptoms: [
            ["Fever", "fever"],
            ["Fatigue", "fatigue"],
            ["Weakness", "weakness"],
            ["Chills", "chills"],
            ["Sweating", "sweating"],
            ["Malaise", "malaise"],
            ["Weight Loss", "weight_loss"],
            ["Weight Gain", "weight_gain"],
            ["Dehydration", "dehydration"],
            ["High Fever", "high_fever"],
            ["Shivering", "shivering"]
        ]
    },

    {
        title: "Head & Nervous System",
        symptoms: [
            ["Headache", "headache"],
            ["Dizziness", "dizziness"],
            ["Loss of Balance", "loss_of_balance"],
            ["Confusion", "confusion"],
            ["Drowsiness", "drowsiness"],
            ["Blurred Vision", "blurred_vision"],
            ["Numbness", "numbness"],
            ["Tingling", "tingling"],
            ["Weakness in Limbs", "weakness_in_limbs"],
            ["Slurred Speech", "slurred_speech"],
            ["Seizures", "seizures"]
        ]
    },

    {
        title: "Nose, Ear & Throat",
        symptoms: [
            ["Runny Nose", "runny_nose"],
            ["Sneezing", "sneezing"],
            ["Nasal Congestion", "nasal_congestion"],
            ["Sore Throat", "sore_throat"],
            ["Cough", "cough"],
            ["Hoarseness", "hoarseness"],
            ["Loss of Smell", "loss_of_smell"],
            ["Loss of Taste", "loss_of_taste"],
            ["Ear Pain", "ear_pain"],
            ["Ear Discharge", "ear_discharge"]
        ]
    },

    {
        title: "Chest & Breathing",
        symptoms: [
            ["Chest Pain", "chest_pain"],
            ["Shortness of Breath", "shortness_of_breath"],
            ["Difficulty Breathing", "difficulty_breathing"],
            ["Wheezing", "wheezing"],
            ["Rapid Breathing", "rapid_breathing"],
            ["Chest Tightness", "chest_tightness"],
            ["Cough with Phlegm", "cough_with_phlegm"],
            ["Blood in Sputum", "blood_in_sputum"]
        ]
    },

    {
        title: "Stomach & Digestion",
        symptoms: [
            ["Abdominal Pain", "abdominal_pain"],
            ["Nausea", "nausea"],
            ["Vomiting", "vomiting"],
            ["Diarrhea", "diarrhea"],
            ["Constipation", "constipation"],
            ["Indigestion", "indigestion"],
            ["Bloating", "bloating"],
            ["Heartburn", "heartburn"],
            ["Loss of Appetite", "loss_of_appetite"],
            ["Stomach Discomfort", "stomach_discomfort"],
            ["Blood in Stool", "blood_in_stool"]
        ]
    },

    {
        title: "Urinary Problems",
        symptoms: [
            ["Frequent Urination", "frequent_urination"],
            ["Painful Urination", "painful_urination"],
            ["Burning Urination", "burning_urination"],
            ["Blood in Urine", "blood_in_urine"],
            ["Dark Urine", "dark_urine"],
            ["Reduced Urine", "reduced_urine"],
            ["Increased Urination", "increased_urination"]
        ]
    },

    {
        title: "Skin & Hair",
        symptoms: [
            ["Skin Rash", "skin_rash"],
            ["Itching", "itching"],
            ["Redness", "redness"],
            ["Dry Skin", "dry_skin"],
            ["Yellow Skin", "yellow_skin"],
            ["Pale Skin", "pale_skin"],
            ["Swelling", "swelling"],
            ["Hair Loss", "hair_loss"],
            ["Acne", "acne"],
            ["Skin Lesions", "skin_lesions"]
        ]
    },

    {
        title: "Bones, Muscles & Joints",
        symptoms: [
            ["Joint Pain", "joint_pain"],
            ["Muscle Pain", "muscle_pain"],
            ["Back Pain", "back_pain"],
            ["Neck Pain", "neck_pain"],
            ["Muscle Weakness", "muscle_weakness"],
            ["Joint Swelling", "joint_swelling"],
            ["Stiffness", "stiffness"],
            ["Difficulty Walking", "difficulty_walking"]
        ]
    },

    {
        title: "Heart & Blood",
        symptoms: [
            ["Palpitations", "palpitations"],
            ["Fast Heart Rate", "fast_heart_rate"],
            ["Low Blood Pressure", "low_blood_pressure"],
            ["High Blood Pressure", "high_blood_pressure"],
            ["Bleeding", "bleeding"],
            ["Easy Bruising", "easy_bruising"],
            ["Pale", "pale"],
            ["Cold Hands & Feet", "cold_hands_feet"]
        ]
    },

    {
        title: "Eye Problems",
        symptoms: [
            ["Eye Pain", "eye_pain"],
            ["Red Eyes", "red_eyes"],
            ["Watery Eyes", "watery_eyes"],
            ["Eye Discharge", "eye_discharge"],
            ["Vision Problems", "vision_problems"],
            ["Sensitivity to Light", "sensitivity_to_light"]
        ]
    }

];


// =====================================================
// COMPONENT
// =====================================================

export default function SymptomChecker() {

    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("Male");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");

    const [openCategory, setOpenCategory] = useState(null);

    const [selectedSymptoms, setSelectedSymptoms] =
        useState({});

    const [additionalInfo, setAdditionalInfo] =
        useState("");

    const [verified, setVerified] =
        useState(false);

    const [result, setResult] =
        useState(null);

    const [loading, setLoading] =
        useState(false);

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
    // TOGGLE SYMPTOM
    // =====================================================

    const toggleSymptom = (key) => {

        setSelectedSymptoms(
            previous => ({

                ...previous,

                [key]:
                    previous[key] ? 0 : 1

            })
        );

    };


    // =====================================================
    // SELECTED COUNT
    // =====================================================

    const selectedCount =
        Object.values(
            selectedSymptoms
        ).filter(
            value => value === 1
        ).length;


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

        if (selectedCount === 0) {

            alert(
                "Please select at least one symptom."
            );

            return;
        }

        if (!verified) {

            alert(
                "Please confirm that the selected symptoms and information are correct."
            );

            return;
        }


        setLoading(true);


        try {

            const values = {
                ...selectedSymptoms
            };


            const response = await fetch(
                "https://medisense-ai-4zpl.onrender.com/symptom/predict",
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

                        values

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


            setResult(data);


            setTimeout(() => {

                document
                    .getElementById(
                        "symptom-result"
                    )
                    ?.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

            }, 100);


        } catch (error) {

            console.error(
                "Symptom prediction error:",
                error
            );

            alert(
                error.message ||
                "Could not predict the disease."
            );

        } finally {

            setLoading(false);

        }

    };


    // =====================================================
    // CHATBOT
    // =====================================================

    const handleChat = async () => {

        if (
            !chatInput.trim() ||
            !result
        ) {
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
                    "Symptom Based Disease Prediction",

                prediction:
                    result.prediction,

                confidence:
                    result.confidence,

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

                selectedSymptoms:
                    result.selectedSymptoms,

                top3:
                    result.top3,

                summary:
                    result.summary,

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
                "https://medisense-ai-4zpl.onrender.com/symptom/chat",
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
                "Symptom chatbot error:",
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

        <div className="symptom-page">


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

                    <FaStethoscope />

                </div>

                <div>

                    <h1>
                        Symptom Checker
                    </h1>

                    <p>
                        AI-Powered Disease Prediction from Your Symptoms
                    </p>

                </div>

            </header>


            {/* =================================================
                PERSONAL DETAILS
            ================================================= */}

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

                </div>


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
                SYMPTOMS
            ================================================= */}

            <section className="glass-card symptoms-card">

                <div className="symptoms-header">

                    <div>

                        <h2>
                            Select Your Symptoms
                        </h2>

                        <p>
                            Select all symptoms you are currently experiencing.
                        </p>

                    </div>


                    <div className="selected-counter">

                        {selectedCount}

                        <span>
                            selected
                        </span>

                    </div>

                </div>


                <div className="categories">

                    {symptomCategories.map(
                        (
                            category,
                            categoryIndex
                        ) => {

                            const isOpen =
                                openCategory ===
                                categoryIndex;


                            const categorySelected =
                                category.symptoms.filter(
                                    ([, key]) =>
                                        selectedSymptoms[key] === 1
                                ).length;


                            return (

                                <div
                                    className="symptom-category"
                                    key={
                                        categoryIndex
                                    }
                                >

                                    <button
                                        className={`category-header ${
                                            isOpen
                                                ? "active"
                                                : ""
                                        }`}
                                        onClick={() =>
                                            setOpenCategory(
                                                isOpen
                                                    ? null
                                                    : categoryIndex
                                            )
                                        }
                                    >

                                        <span>

                                            {category.title}

                                            {categorySelected >
                                                0 && (

                                                <b>
                                                    {
                                                        categorySelected
                                                    }
                                                </b>

                                            )}

                                        </span>

                                        <FaChevronDown
                                            className={
                                                isOpen
                                                    ? "rotate"
                                                    : ""
                                            }
                                        />

                                    </button>


                                    {isOpen && (

                                        <div className="symptom-grid">

                                            {category.symptoms.map(
                                                (
                                                    [
                                                        label,
                                                        key
                                                    ]
                                                ) => (

                                                    <label
                                                        className={`symptom-option ${
                                                            selectedSymptoms[key]
                                                                ? "selected"
                                                                : ""
                                                        }`}
                                                        key={key}
                                                    >

                                                        <input
                                                            type="checkbox"
                                                            checked={
                                                                selectedSymptoms[key] === 1
                                                            }
                                                            onChange={() =>
                                                                toggleSymptom(
                                                                    key
                                                                )
                                                            }
                                                        />

                                                        <span>
                                                            {label}
                                                        </span>

                                                    </label>

                                                )
                                            )}

                                        </div>

                                    )}

                                </div>

                            );

                        }
                    )}

                </div>


                {/* Additional information */}

                <div className="additional-info">

                    <label>
                        Additional Information
                        <span>
                            Optional
                        </span>
                    </label>

                    <textarea
                        placeholder="Describe any other symptoms or health information..."
                        value={additionalInfo}
                        onChange={e =>
                            setAdditionalInfo(
                                e.target.value
                            )
                        }
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
                        checked={verified}
                        onChange={e =>
                            setVerified(
                                e.target.checked
                            )
                        }
                    />

                    <span>
                        I confirm that the selected symptoms
                        and personal information are correct.
                    </span>

                </label>

            </div>


            {/* =================================================
                PREDICT BUTTON
            ================================================= */}

            <button
                className="predict-btn"
                disabled={
                    !verified ||
                    selectedCount === 0 ||
                    loading
                }
                onClick={handlePredict}
            >

                {loading
                    ? "Analyzing Symptoms..."
                    : "Predict Disease"}

            </button>


            {/* =================================================
                RESULT
            ================================================= */}

            {result && (

                <section
                    id="symptom-result"
                    className="glass-card result-card"
                >

                    <div className="completed-label">
                        ✓ Analysis Completed
                    </div>


                    {/* Patient summary */}

                    <div className="patient-summary">

                        <div>
                            <span>
                                Name
                            </span>

                            <strong>
                                {result.name}
                            </strong>
                        </div>

                        <div>
                            <span>
                                Age
                            </span>

                            <strong>
                                {result.age} years
                            </strong>
                        </div>

                        <div>
                            <span>
                                Gender
                            </span>

                            <strong>
                                {result.gender}
                            </strong>
                        </div>

                        <div>
                            <span>
                                BMI
                            </span>

                            <strong>
                                {Number(
                                    result.bmi
                                ).toFixed(2)}
                            </strong>
                        </div>

                    </div>


                    {/* Main prediction */}

                    <div className="prediction-box">

                        <span>
                            Most Likely Prediction
                        </span>

                        <h2>
                            {result.prediction}
                        </h2>

                        <div className="confidence">

                            Confidence:

                            <strong>
                                {" "}
                                {Number(
                                    result.confidence
                                ).toFixed(1)}
                                %
                            </strong>

                        </div>

                    </div>


                    {/* Top 3 */}

                    {result.top3?.length > 0 && (

                        <div className="top-diseases">

                            <h2>
                                Other Possible Conditions
                            </h2>

                            <div className="top-disease-grid">

                                {result.top3.map(
                                    (
                                        item,
                                        index
                                    ) => (

                                        <div
                                            className="disease-result"
                                            key={index}
                                        >

                                            <div className="disease-rank">

                                                #{index + 1}

                                            </div>

                                            <div>

                                                <h3>
                                                    {
                                                        item.disease
                                                    }
                                                </h3>

                                                <div className="probability-bar">

                                                    <span
                                                        style={{
                                                            width:
                                                                `${Math.min(
                                                                    item.probability,
                                                                    100
                                                                )}%`
                                                        }}
                                                    />

                                                </div>

                                                <p>
                                                    {Number(
                                                        item.probability
                                                    ).toFixed(1)}
                                                    % probability
                                                </p>

                                            </div>

                                        </div>

                                    )
                                )}

                            </div>

                        </div>

                    )}


                    {/* Summary */}

                    {result.summary && (

                        <div className="result-section">

                            <h3>
                                What This Means
                            </h3>

                            <div className="info-card">

                                {result.summary}

                            </div>

                        </div>

                    )}


                    {/* Selected symptoms */}

                    {result.selectedSymptoms?.length > 0 && (

                        <div className="result-section">

                            <h3>
                                Selected Symptoms
                            </h3>

                            <div className="selected-symptoms-list">

                                {result.selectedSymptoms.map(
                                    (
                                        symptom,
                                        index
                                    ) => (

                                        <span
                                            key={index}
                                            className="selected-symptom-tag"
                                        >
                                            {symptom.replace(
                                                /_/g,
                                                " "
                                            )}
                                        </span>

                                    )
                                )}

                            </div>

                        </div>

                    )}


                    {/* Health effects */}

                    {result.health_effects?.length > 0 && (

                        <ResultList
                            title="Possible Health Effects"
                            items={
                                result.health_effects
                            }
                            icon="⚠"
                        />

                    )}


                    {/* Diet */}

                    {result.diet?.length > 0 && (

                        <ResultList
                            title="Diet Recommendations"
                            items={
                                result.diet
                            }
                            icon="✓"
                        />

                    )}


                    {/* Lifestyle */}

                    {result.lifestyle?.length > 0 && (

                        <ResultList
                            title="Lifestyle Recommendations"
                            items={
                                result.lifestyle
                            }
                            icon="✓"
                        />

                    )}


                    {/* Medical */}

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

                        This prediction is generated by an
                        AI/ML model and is not a confirmed
                        medical diagnosis. Please consult a
                        qualified healthcare professional for
                        proper medical evaluation.

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
                                Ask anything about your symptoms,
                                prediction, diet, lifestyle or health.
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
                            (
                                message,
                                index
                            ) => (

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


// =====================================================
// RESULT LIST
// =====================================================

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
                (
                    item,
                    index
                ) => (

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