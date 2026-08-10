import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./Home";
import HeartDisease from "./pages/HeartDisease";
import Diabetes from "./pages/Diabetes";
import LiverDisease from "./pages/LiverDisease";
import KidneyDisease from "./pages/KidneyDisease";
import LipidProfile from "./pages/LipidProfile";
import SymptomChecker from "./pages/SymptomChecker";
import "./App.css";

import Sidebar from "./components/Sidebar";

export default function App() {

    return (

        <BrowserRouter>

            <Sidebar />

            <main className="app-content">

                <Routes>

                    <Route
                        path="/"
                        element={<Home />}
                    />

                    <Route
                        path="/heart"
                        element={<HeartDisease />}
                    />

                    <Route
                        path="/diabetes"
                        element={<Diabetes />}
                    />

                    <Route
                        path="/liver"
                        element={<LiverDisease />}
                    />

                    <Route
                        path="/kidney"
                        element={<KidneyDisease />}
                    />

                    <Route
                        path="/lipid"
                        element={<LipidProfile />}
                    />

                    <Route
                        path="/symptom"
                        element={<SymptomChecker />}
                    />

                </Routes>

            </main>

        </BrowserRouter>

    );

}