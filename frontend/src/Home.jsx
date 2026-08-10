import TypingText from "./components/TypingText";
import SoftAurora from "./components/SoftAurora";
import ModuleCards from "./components/ModuleCards";
import Robot from "./components/Robot";
import { FaHeartbeat } from "react-icons/fa";
import "./Home.css";
import { useRef } from "react";

export default function Home() {
  const cardsRef = useRef(null);
  const scrollToCards = () => {
    cardsRef.current?.scrollIntoView({
        behavior: "smooth"
    });
  };

  return (
    <>
      <section className="home">

        <SoftAurora
          speed={0.6}
          scale={1.5}
          brightness={1}
          color1="#7DEBFF"
          color2="#00CFFF"
          noiseFrequency={2.5}
          noiseAmplitude={1}
          bandHeight={0.55}
          bandSpread={1}
          octaveDecay={0.1}
          layerOffset={0}
          colorSpeed={1}
          enableMouseInteraction={true}
          mouseInfluence={0.25}
        />

        {/* ---------- NAVBAR ---------- */}

        <nav className="navbar">

          <div className="logoSection">

            <FaHeartbeat className="logoIcon"/>

            <h2>

              <span className="white">MEDISENSE</span>

              <span className="blue"> AI</span>

            </h2>

          </div>

          <div className="navButtons">

            <button className="loginBtn">

              Login

            </button>

            <button className="signupBtn">

              Get Started

            </button>

          </div>

        </nav>

        {/* ---------- HERO ---------- */}

        <div className="heroContent">

          <div className="leftHero">

            <h1 className="heroTitle">
                <span className="white">MEDISENSE</span>{" "}
                <span className="blue">AI</span>
            </h1>

            <TypingText/>
            <p className="heroDescription">

            Upload your medical reports, predict diseases, and
            receive AI-powered health insights in seconds.

  

            </p>
            

            <button onClick={scrollToCards}>
                Explore Modules
            </button>

          </div>

          <div className="rightHero">

            <Robot/>

          </div>

        </div>

      </section>

      <div ref={cardsRef}>
          <ModuleCards />
      </div>
    </>
  );
}