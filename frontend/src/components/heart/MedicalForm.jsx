export default function MedicalForm(){

    const fields=[

        "Chest Pain",

        "Blood Pressure",

        "Cholesterol",

        "Fasting Blood Sugar",

        "ECG Result",

        "Maximum Heart Rate",

        "Exercise Angina",

        "Old Peak",

        "ST Slope",

        "Major Vessels",

        "Thal"

    ];

    return(

        <div className="glassCard">

            <h2>

                Medical Parameters

            </h2>

            <div className="grid2">

                {

                    fields.map((item,index)=>(

                        <div key={index}>

                            <label>

                                {item}

                            </label>

                            <input placeholder={item}/>

                        </div>

                    ))

                }

            </div>

        </div>

    );

}