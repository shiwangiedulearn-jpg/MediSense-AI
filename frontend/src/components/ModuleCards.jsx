import SoftAurora from "./SoftAurora";
import "../ModuleCards.css";
import { useNavigate } from "react-router-dom";

const modules = [
    {
        title: "Heart Disease",
        icon: "❤️",
        path: "/heart"
    },
    {
        title: "Diabetes",
        icon: "🩸",
        path: "/diabetes"
    },
    {
        title: "Liver Disease",
        icon: "🫀",
        path: "/liver"
    },
    {
        title: "Kidney Disease",
        icon: "🩺",
        path: "/kidney"
    },
    {
        title: "Lipid Profile",
        icon: "🧪",
        path: "/lipid"
    },
    {
        title: "Symptom Checker",
        icon: "🤖",
        path: "/symptom"
    }
];

export default function ModuleCards(){
    const navigate = useNavigate();

    return(

        <section className="cardsSection">

        
            <div className="cards">

                {

                    modules.map((item,index)=>(

                        <div
                            className="card"
                            key={index}
                            onClick={() => navigate(item.path)}
                        >

                            <div className="iconBox">

                                <span>{item.icon}</span>

                            </div>

                            <h2>{item.title}</h2>

                            <button>

                                Open Module →

                            </button>

                        </div>

                    ))

                }

            </div>

        </section>

    )

}