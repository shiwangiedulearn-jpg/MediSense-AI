import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaHeartbeat,
  FaCloudUploadAlt,
  FaCheckCircle,
} from "react-icons/fa";

import "./HeartDisease.css";

const API_URL = "http://127.0.0.1:8000";

const defaultValues = {
  cp: 3,
  trestbps: 120,
  chol: 200,
  fbs: 0,
  restecg: 0,
  thalach: 150,
  exang: 0,
  oldpeak: 1,
  slope: 1,
  ca: 0,
  thal: 1,
};

export default function HeartDisease() {
  const navigate = useNavigate();

  // -------------------------
  // PERSONAL INFORMATION
  // -------------------------

  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("Male");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");

  // -------------------------
  // REPORT
  // -------------------------

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [reportUploaded, setReportUploaded] = useState(false);

  // -------------------------
  // MEDICAL VALUES
  // -------------------------

  const [values, setValues] = useState(defaultValues);

  // -------------------------
  // VERIFICATION
  // -------------------------

  const [verified, setVerified] = useState(false);

  // -------------------------
  // RESULT
  // -------------------------

  const [result, setResult] = useState(null);
  const [predicting, setPredicting] = useState(false);

  // -------------------------
  // AI CHATBOT
  // -------------------------

  const [chatMessages, setChatMessages] = useState([]);

  const [chatInput, setChatInput] = useState("");

  const [chatLoading, setChatLoading] = useState(false);

  // -------------------------
  // BMI
  // -------------------------

  const bmi =
    height && weight
      ? weight / Math.pow(height / 100, 2)
      : null;

  const getBmiCategory = () => {
    if (!bmi) return "--";

    if (bmi < 18.5) return "Underweight";
    if (bmi < 25) return "Normal";
    if (bmi < 30) return "Overweight";

    return "Obese";
  };

  // -------------------------
  // UPDATE MEDICAL VALUE
  // -------------------------

  const updateValue = (key, value) => {
    setValues((previous) => ({
      ...previous,
      [key]: value,
    }));

    // If user changes something,
    // require verification again.
    setVerified(false);
  };

  // -------------------------
  // REPORT UPLOAD
  // -------------------------

  const handleFileChange = async (selectedFile) => {
    if (!selectedFile) return;

    setFile(selectedFile);
    setReportUploaded(false);
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setUploading(true);

      const response = await fetch(
        `${API_URL}/heart/extract`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {

          const errorText = await response.text();

          console.error(
              "Chat API error:",
              errorText
          );

          throw new Error(
              `Chat API failed: ${response.status}`
          );

      }

      const data = await response.json();

      console.log("Extracted values:", data.values);

      // Start with defaults.
      // Extracted values overwrite defaults.
      setValues({
        ...defaultValues,
        ...data.values,
      });

      setReportUploaded(true);
      setVerified(false);

    } catch (error) {

        console.error(
            "Chatbot error:",
            error
        );

        setChatMessages((previous) => [
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

  // -------------------------
  // DRAG & DROP
  // -------------------------

  const handleDrop = (event) => {
    event.preventDefault();

    const droppedFile = event.dataTransfer.files[0];

    if (droppedFile) {
      handleFileChange(droppedFile);
    }
  };

  // -------------------------
  // PREDICT
  // -------------------------

  const handlePredict = async () => {
    if (!verified) return;

    if (!name || !age || !height || !weight) {
      alert("Please complete all personal details.");
      return;
    }

    try {
      setPredicting(true);

      const response = await fetch(
        `${API_URL}/heart/predict`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
            age: Number(age),
            gender,
            height: Number(height),
            weight: Number(weight),
            values,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const data = await response.json();

      setResult(data);

      setTimeout(() => {
        document
          .getElementById("prediction-result")
          ?.scrollIntoView({
            behavior: "smooth",
          });
      }, 100);

    } catch (error) {
      console.error(error);

      alert(
        "Prediction failed. Please make sure the backend is running."
      );
    } finally {
      setPredicting(false);
    }
  };
  // -------------------------
  // ASK MEDISENSE AI
  // -------------------------

  const handleChat = async () => {

      if (!chatInput.trim()) {
          return;
      }

      if (!result) {
          return;
      }

      const userMessage = {
          role: "user",
          content: chatInput.trim()
      };

      const updatedMessages = [
          ...chatMessages,
          userMessage
      ];

      setChatMessages(updatedMessages);

      setChatInput("");

      setChatLoading(true);

      try {

          // Build complete patient context
          const context = {

              module: "Heart Disease Prediction",

              patient: {
                  name,
                  age: Number(age),
                  gender,
                  height: Number(height),
                  weight: Number(weight),

                  bmi: bmi
                      ? Number(bmi.toFixed(2))
                      : null
              },

              medicalValues: values,

              prediction: {
                  result: result.prediction,

                  probability:
                      result.probability,

                  riskLabel:
                      result.riskLabel,

                  riskClass:
                      result.riskClass
              },

              contributingFactors:
                  result.factors || [],

              recommendations:
                  result.recommendations || []
          };


          const response = await fetch(
              `${API_URL}/heart/chat`,
              {
                  method: "POST",

                  headers: {
                      "Content-Type":
                          "application/json"
                  },

                  body: JSON.stringify({

                      message:
                          userMessage.content,

                      context,

                      history:
                          updatedMessages
                  })
              }
          );


          if (!response.ok) {

              throw new Error(
                  "Chat request failed"
              );

          }


          const data =
              await response.json();


          const assistantMessage = {

              role: "assistant",

              content:
                  data.answer ||
                  "I couldn't generate a response. Please try again."

          };


          setChatMessages(
              [
                  ...updatedMessages,
                  assistantMessage
              ]
          );


      } catch (error) {

          console.error(
              "Chatbot error:",
              error
          );


          setChatMessages(
              [
                  ...updatedMessages,

                  {
                      role: "assistant",

                      content:
                          "I'm sorry, I couldn't process your question right now. Please try again."
                  }
              ]
          );


      } finally {

          setChatLoading(false);

      }
  };

  const clearChat = () => {
      setChatMessages([]);
      setChatInput("");
  };

  return (
    <div className="heart-page">

      {/* =========================
          BACK BUTTON
      ========================= */}

      <button
        className="back-home"
        onClick={() => navigate("/")}
      >
        <FaArrowLeft />
        Back to Home
      </button>


      {/* =========================
          HEADER
      ========================= */}

      <header className="heart-header">

        <div className="heart-header-icon">
          <FaHeartbeat />
        </div>

        <div>
          <h1>Heart Disease Prediction</h1>

          <p>
            AI Powered Cardiovascular Risk Assessment
          </p>
        </div>

      </header>


      {/* =========================
          TOP SECTION
      ========================= */}

      <div className="top-grid">


        {/* =====================
            PATIENT INFORMATION
        ===================== */}

        <section className="glass-card patient-card">

          <h2>Patient Information</h2>

          <div className="form-grid">

            <div className="field">

              <label>Full Name</label>

              <input
                type="text"
                placeholder="Enter Name"
                value={name}
                onChange={(e) =>
                  setName(e.target.value)
                }
              />

            </div>


            <div className="field">

              <label>Age</label>

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


            <div className="field">

              <label>Gender</label>

              <select
                value={gender}
                onChange={(e) =>
                  setGender(e.target.value)
                }
              >
                <option>Male</option>
                <option>Female</option>
              </select>

            </div>


            <div className="field">

              <label>Height (cm)</label>

              <input
                type="number"
                min="50"
                max="250"
                value={height}
                onChange={(e) =>
                  setHeight(e.target.value)
                }
              />

            </div>


            <div className="field">

              <label>Weight (kg)</label>

              <input
                type="number"
                min="10"
                max="250"
                value={weight}
                onChange={(e) =>
                  setWeight(e.target.value)
                }
              />

            </div>


            <div className="field">

              <label>BMI</label>

              <div className="readonly-field">
                {bmi ? bmi.toFixed(2) : "--"}
              </div>

            </div>

          </div>

        </section>


        {/* =====================
            UPLOAD REPORT
        ===================== */}

        <section className="glass-card upload-card">

          <h2>Upload Medical Report</h2>

          <label
            className="upload-box"
            onDragOver={(e) =>
              e.preventDefault()
            }
            onDrop={handleDrop}
          >

            <FaCloudUploadAlt className="upload-icon" />

            <h3>
              {uploading
                ? "Analyzing Report..."
                : "Drag & Drop Report"}
            </h3>

            <p>
              Upload PDF, JPG or PNG report
            </p>

            <span className="browse-button">
              {uploading
                ? "Processing..."
                : "Browse Files"}
            </span>

            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              hidden
              disabled={uploading}
              onChange={(e) =>
                handleFileChange(
                  e.target.files[0]
                )
              }
            />

          </label>


          {file && !uploading && (
            <div className="uploaded-file">

              <FaCheckCircle />

              <span>
                {file.name}
              </span>

            </div>
          )}

        </section>

      </div>


      {/* =========================
          MEDICAL PARAMETERS
      ========================= */}

      <section className="glass-card parameters-card">

        <div className="section-heading">

          <div>
            <h2>Medical Parameters</h2>

            <p>
              Values extracted from your report are
              automatically filled. Review or correct
              them before prediction.
            </p>
          </div>

          {reportUploaded && (
            <span className="extracted-badge">
              ✓ Report Analyzed
            </span>
          )}

        </div>


        <div className="parameter-grid">


          {/* CHEST PAIN */}

          <div className="field">

            <label>Chest Pain Type</label>

            <select
              value={values.cp}
              onChange={(e) =>
                updateValue(
                  "cp",
                  Number(e.target.value)
                )
              }
            >
              <option value="0">
                Typical Angina
              </option>

              <option value="1">
                Atypical Angina
              </option>

              <option value="2">
                Non-Anginal Pain
              </option>

              <option value="3">
                I'm not sure
              </option>
            </select>

          </div>


          {/* BLOOD PRESSURE */}

          <div className="field">

            <label>
              Resting Blood Pressure (mmHg)
            </label>

            <input
              type="number"
              min="80"
              max="250"
              value={values.trestbps}
              onChange={(e) =>
                updateValue(
                  "trestbps",
                  Number(e.target.value)
                )
              }
            />

          </div>


          {/* CHOLESTEROL */}

          <div className="field">

            <label>
              Serum Cholesterol (mg/dL)
            </label>

            <input
              type="number"
              min="100"
              max="600"
              value={values.chol}
              onChange={(e) =>
                updateValue(
                  "chol",
                  Number(e.target.value)
                )
              }
            />

          </div>


          {/* FASTING BLOOD SUGAR */}

          <div className="field">

            <label>
              Fasting Blood Sugar &gt;120 mg/dL
            </label>

            <select
              value={values.fbs}
              onChange={(e) =>
                updateValue(
                  "fbs",
                  Number(e.target.value)
                )
              }
            >

              <option value="0">
                No
              </option>

              <option value="1">
                Yes
              </option>

            </select>

          </div>


          {/* ECG */}

          <div className="field">

            <label>Resting ECG Result</label>

            <select
              value={values.restecg}
              onChange={(e) =>
                updateValue(
                  "restecg",
                  Number(e.target.value)
                )
              }
            >

              <option value="0">
                Normal
              </option>

              <option value="1">
                ST-T Wave Abnormality
              </option>

              <option value="2">
                Left Ventricular Hypertrophy
              </option>

            </select>

          </div>


          {/* MAX HEART RATE */}

          <div className="field">

            <label>
              Maximum Heart Rate Achieved
            </label>

            <input
              type="number"
              min="60"
              max="220"
              value={values.thalach}
              onChange={(e) =>
                updateValue(
                  "thalach",
                  Number(e.target.value)
                )
              }
            />

          </div>


          {/* EXERCISE ANGINA */}

          <div className="field">

            <label>
              Exercise Induced Angina
            </label>

            <select
              value={values.exang}
              onChange={(e) =>
                updateValue(
                  "exang",
                  Number(e.target.value)
                )
              }
            >

              <option value="0">
                No
              </option>

              <option value="1">
                Yes
              </option>

            </select>

          </div>


          {/* OLDPEAK */}

          <div className="field">

            <label>
              ST Depression (Oldpeak)
            </label>

            <input
              type="number"
              min="0"
              max="7"
              step="0.1"
              value={values.oldpeak}
              onChange={(e) =>
                updateValue(
                  "oldpeak",
                  Number(e.target.value)
                )
              }
            />

          </div>


          {/* ST SLOPE */}

          <div className="field">

            <label>
              Slope of Peak Exercise ST Segment
            </label>

            <select
              value={values.slope}
              onChange={(e) =>
                updateValue(
                  "slope",
                  Number(e.target.value)
                )
              }
            >

              <option value="0">
                Upsloping
              </option>

              <option value="1">
                Flat
              </option>

              <option value="2">
                Downsloping
              </option>

            </select>

          </div>


          {/* MAJOR VESSELS */}

          <div className="field">

            <label>
              Number of Major Vessels
            </label>

            <select
              value={values.ca}
              onChange={(e) =>
                updateValue(
                  "ca",
                  Number(e.target.value)
                )
              }
            >

              <option value="0">0</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>

            </select>

          </div>


          {/* THAL */}

          <div className="field">

            <label>
              Thalassemia
            </label>

            <select
              value={values.thal}
              onChange={(e) =>
                updateValue(
                  "thal",
                  Number(e.target.value)
                )
              }
            >

              <option value="1">
                Normal
              </option>

              <option value="2">
                Fixed Defect
              </option>

              <option value="3">
                Reversible Defect
              </option>

            </select>

          </div>

        </div>

      </section>


      {/* =========================
          VERIFICATION
      ========================= */}

      <section className="verification-card">

        <label className="verification">

          <input
            type="checkbox"
            checked={verified}
            onChange={(e) =>
              setVerified(e.target.checked)
            }
          />

          <span className="checkmark"></span>

          <span>
            I have reviewed all the above values
            and confirm that they are correct.
          </span>

        </label>

      </section>


      {/* =========================
          PREDICT BUTTON
      ========================= */}

      <button
        className={`predict-button ${
          !verified ? "disabled" : ""
        }`}
        disabled={!verified || predicting}
        onClick={handlePredict}
      >

        {predicting
          ? "Analyzing..."
          : "Predict Heart Disease"}

      </button>


      {/* =========================
          RESULT
      ========================= */}

      {result && (
        <section
          id="prediction-result"
          className="result-card"
        >

          <h2>Prediction Result</h2>

          <div
            className={`risk-box ${result.riskClass}`}
          >

            <span>
              {result.riskLabel}
            </span>

            <strong>
              {result.probability.toFixed(2)}%
            </strong>

          </div>


          <div className="result-grid">

            <div>
              <span>Patient</span>
              <strong>{name}</strong>
            </div>

            <div>
              <span>Age</span>
              <strong>{age} years</strong>
            </div>

            <div>
              <span>BMI</span>
              <strong>
                {bmi ? bmi.toFixed(2) : "--"}
              </strong>
            </div>

            <div>
              <span>BMI Category</span>
              <strong>
                {getBmiCategory()}
              </strong>
            </div>

          </div>


          {result.factors?.length > 0 && (
            <div className="result-section">

              <h3>
                Possible Contributing Factors
              </h3>

              {result.factors.map(
                (factor, index) => (
                  <p key={index}>
                    • {factor}
                  </p>
                )
              )}

            </div>
          )}


          <div className="result-section">

            <h3>Recommendations</h3>

            {result.recommendations.map(
              (recommendation, index) => (
                <p key={index}>
                  ✓ {recommendation}
                </p>
              )
            )}

          </div>


          <div className="medical-disclaimer">

            This prediction is generated by a
            machine learning model and is not a
            medical diagnosis. Please consult a
            qualified healthcare professional.

          </div>

        </section>
      )}
      {result && (

        <section className="ai-chat-card">

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
                        Ask anything about your prediction,
                        report, symptoms, diet or lifestyle.
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


            {/* =========================
                CHAT MESSAGES
            ========================= */}

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

                                {String(message.content || "")
                                  .split("\n")
                                  .map(
                                      (line, lineIndex) => (
                                          <p key={lineIndex}>
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


            {/* =========================
                CHAT INPUT
            ========================= */}

            <div className="chat-input-area">

                <input
                    type="text"
                    placeholder="Ask a follow-up question..."
                    value={chatInput}
                    disabled={chatLoading}
                    onChange={(e) =>
                        setChatInput(e.target.value)
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