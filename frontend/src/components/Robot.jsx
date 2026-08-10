import Spline from "@splinetool/react-spline";

export default function Robot() {
  return(

<div className="robot">
    <div className="robotBeam"></div>
    <div className="robotBaseGlowOuter"></div>

    <div className="robotBaseGlow"></div>

    <Spline
        scene="https://prod.spline.design/dDYCNMsoLadTDea0/scene.splinecode?v=6"
    />

</div>

);
}