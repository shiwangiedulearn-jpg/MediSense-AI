import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

import {
    FaHome,
    FaHeart,
    FaTint,
    FaLungs,
    FaFlask,
    FaStethoscope,
    FaBars,
    FaTimes
} from "react-icons/fa";

import "./Sidebar.css";


export default function Sidebar() {

    const navigate = useNavigate();
    const location = useLocation();

    const [open, setOpen] = useState(true);


    const menuItems = [

        {
            name: "Home",
            path: "/",
            icon: <FaHome />
        },

        {
            name: "Heart Disease",
            path: "/heart",
            icon: <FaHeart />
        },

        {
            name: "Diabetes",
            path: "/diabetes",
            icon: <FaTint />
        },

        {
            name: "Liver Disease",
            path: "/liver",
            icon: <FaLungs />
        },

        {
            name: "Kidney Disease",
            path: "/kidney",
            icon: <FaFlask />
        },

        {
            name: "Lipid Profile",
            path: "/lipid",
            icon: <FaFlask />
        },

        {
            name: "Symptom Checker",
            path: "/symptom",
            icon: <FaStethoscope />
        }

    ];


    return (

        <>

            {/* Sidebar Toggle */}

            <button
                className={`sidebar-toggle ${
                    open ? "toggle-open" : "toggle-closed"
                }`}
                onClick={() => setOpen(!open)}
            >
                {open ? <FaTimes /> : <FaBars />}
            </button>


            {/* Sidebar */}

            <aside
                className={`sidebar ${
                    open
                        ? "sidebar-open"
                        : ""
                }`}
            >


                {/* Logo */}

                <div className="sidebar-logo">

                    <div className="sidebar-logo-icon">
                        🩺
                    </div>


                    <div>

                        <h2>
                            MediSense
                        </h2>

                        <span>
                            AI Healthcare
                        </span>

                    </div>

                </div>


                {/* Menu */}

                <div className="sidebar-menu">

                    <p className="sidebar-label">
                        MAIN MENU
                    </p>


                    {menuItems.map(
                        (item) => (

                            <button
                                key={item.path}

                                className={`sidebar-item ${
                                    location.pathname ===
                                    item.path
                                        ? "active"
                                        : ""
                                }`}

                                onClick={() => {
                                    navigate(item.path);
                                    setOpen(false);
                                }}
                            >


                                <span className="sidebar-icon">

                                    {item.icon}

                                </span>


                                <span className="sidebar-text">

                                    {item.name}

                                </span>


                            </button>

                        )
                    )}

                </div>


                {/* Bottom AI Badge */}

                <div className="sidebar-bottom">

                    <div className="ai-badge">

                        <span>
                            🤖
                        </span>


                        <div>

                            <strong>
                                MediSense AI
                            </strong>

                            <small>
                                Smart Health Assistant
                            </small>

                        </div>

                    </div>

                </div>


            </aside>

        </>

    );

}