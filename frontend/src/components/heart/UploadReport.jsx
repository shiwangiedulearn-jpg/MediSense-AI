import { FaCloudUploadAlt } from "react-icons/fa";

export default function UploadReport(){

    return(

        <div className="glassCard">

            <h2>

                Upload Medical Report

            </h2>

            <div className="uploadArea">

                <FaCloudUploadAlt className="uploadIcon"/>

                <h3>

                    Drag & Drop Report

                </h3>

                <p>

                    Upload PDF, JPG or PNG report

                </p>

                <button>

                    Browse Files

                </button>

            </div>

        </div>

    );

}