import { useMemo, useState } from "react";

export default function PatientInfo(){

    const [patient,setPatient]=useState({

        name:"",

        age:"",

        gender:"Male",

        height:"",

        weight:""

    });

    const bmi=useMemo(()=>{

        const h=Number(patient.height)/100;

        const w=Number(patient.weight);

        if(!h || !w) return "--";

        return (w/(h*h)).toFixed(1);

    },[patient]);

    function change(e){

        setPatient({

            ...patient,

            [e.target.name]:e.target.value

        });

    }

    return(

        <div className="glassCard">

            <h2>

                Patient Information

            </h2>

            <div className="grid2">

                <div>

                    <label>

                        Full Name

                    </label>

                    <input
                        name="name"
                        value={patient.name}
                        onChange={change}
                        placeholder="Enter Name"
                    />

                </div>

                <div>

                    <label>

                        Age

                    </label>

                    <input
                        name="age"
                        value={patient.age}
                        onChange={change}
                        type="number"
                    />

                </div>

                <div>

                    <label>

                        Gender

                    </label>

                    <select
                        name="gender"
                        value={patient.gender}
                        onChange={change}
                    >

                        <option>

                            Male

                        </option>

                        <option>

                            Female

                        </option>

                    </select>

                </div>

                <div>

                    <label>

                        Height (cm)

                    </label>

                    <input
                        name="height"
                        value={patient.height}
                        onChange={change}
                        type="number"
                    />

                </div>

                <div>

                    <label>

                        Weight (kg)

                    </label>

                    <input
                        name="weight"
                        value={patient.weight}
                        onChange={change}
                        type="number"
                    />

                </div>

                <div>

                    <label>

                        BMI

                    </label>

                    <input
                        value={bmi}
                        disabled
                    />

                </div>

            </div>

        </div>

    );

}