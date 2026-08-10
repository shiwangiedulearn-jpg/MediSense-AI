import { useEffect, useState } from "react";

export default function TypingText() {

  const messages = [
  "AI Powered Healthcare Intelligence Platform",
  "Analyze Medical Reports with AI",
  "Predict Disease Risk Instantly",
  "Personalized Health Insights",
  "Smarter Decisions. Better Healthcare."
];

  const [messageIndex, setMessageIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {

    const current = messages[messageIndex];
    let timer;

    if (!isDeleting) {

      if (displayText.length < current.length) {

        timer = setTimeout(() => {
          setDisplayText(current.substring(0, displayText.length + 1));
        }, 55);

      } else {

        timer = setTimeout(() => {
          setIsDeleting(true);
        }, 1800);

      }

    } else {

      if (displayText.length > 0) {

        timer = setTimeout(() => {
          setDisplayText(current.substring(0, displayText.length - 1));
        }, 25);

      } else {

        setIsDeleting(false);
        setMessageIndex((prev) => (prev + 1) % messages.length);

      }

    }

    return () => clearTimeout(timer);

  }, [displayText, isDeleting, messageIndex]);

  return (

    <h2 className="typing">

        <span className="prompt">&gt;</span>

        {displayText}

        <span className="cursor"></span>

    </h2>

 );
}