                                                           Project overview
A Python-based healthcare interoperability proof of concept demonstrating retrieval of HL7 FHIR R4 clinical resources, visualization in a Streamlit glaucoma dashboard, and transfer of patient records from a public FHIR test server (Hospital A) to a separate local HTTP receiver (Hospital B).

The project uses fictional training data. Hospital B is a simplified local receiving service, not a real hospital or production FHIR server.
Features
- Retrieve FHIR R4 resources through REST API GET requests.
- Display patient demographics, right- and left-eye intraocular pressure, glaucoma diagnosis, medication, and encounter details in Streamlit.
- Retrieve and transfer six resources: one Patient, two Observations, one Condition, one MedicationRequest, and one Encounter.
- Send the resources to a separate local HTTP receiver using an HTTP POST containing a transaction-shaped FHIR JSON Bundle.
- Save the received records locally in hospital_b_records.json.
- Verify receipt by requesting the six resources from Hospital B's local HTTP endpoints.
- Technologies
Python · Streamlit · Requests · HL7 FHIR R4 · REST APIs · JSON · HTTP · HAPI FHIR · VS Code
Example clinical record
Field	Value
Patient	Amit Kumar (fictional training record)
FHIR Patient ID	789264
Right-eye IOP	24 mmHg
Left-eye IOP	22 mmHg
Diagnosis	Glaucoma
Medication	Latanoprost 0.005% eye drops
Encounter	Glaucoma follow-up


The example resources were created on the public HAPI FHIR R4 test server. Public test records can be reset or removed, so the fixed resource IDs used by this demo may eventually stop working.
Architecture
Public HAPI FHIR R4 server (Hospital A)
        |
        | HTTP GET: FHIR JSON resources
        |
        +----> Glaucoma Dashboard (Streamlit, port 8501)
        |
        v
Hospital Transfer application (Streamlit, port 8502)
        |
        | HTTP POST: transaction-shaped JSON Bundle
        v
Local HTTP receiver (Hospital B, 127.0.0.1:8765)
        |
        v
hospital_b_records.json
        |
        +----> HTTP GET verification of six stored resources

  Note: Port 8502 is the transfer application's user interface. Hospital B's local receiving endpoint runs on port 8765 and stores the records in a JSON file. The receiver accepts a transaction-shaped Bundle but does not implement full FHIR transaction processing.

  Project files
For a single GitHub repository, organize the files as follows:
HL7-FHIR-Glaucoma-Interoperability/
├── app.py
├── FHIR_Hospital_Transfer/
│   ├── hospital_transfer.py
│   └── README_Hospital_Transfer.txt
├── README.md
├── requirements.txt
└── demo/                        
hospital_b_records.json is generated after a successful transfer

Installation
Install Python and the required packages:
python -m pip install -r requirements.txt
Or install directly:
python -m pip install streamlit requests
Run the Glaucoma Dashboard
Open a terminal in the repository's main folder and run:
python -m streamlit run app.py --server.port 8501
Open: http://localhost:8501

Open: http://localhost:8501

The dashboard retrieves the example patient and clinical resources directly from the HAPI FHIR R4 test server.
Run the Hospital A → Hospital B Transfer
Open a second terminal in the FHIR_Hospital_Transfer folder and run:
python -m streamlit run hospital_transfer.py --server.port 8502

Open: http://localhost:8502
1. Click Transfer records from Hospital A to Hospital B.
2. The application retrieves six resources from the public FHIR server and posts them to the local Hospital B receiver.
3. Click Verify transfer.
4. Confirm that all six resources are available at Hospital B. The receiver writes them to FHIR_Hospital_Transfer/hospital_b_records.json.
Both Streamlit applications can run at the same time on different ports.
FHIR resources used
Resource	Example ID	Purpose
Patient	789264	Demographics
Observation	789321	Right-eye IOP
Observation	789322	Left-eye IOP
Condition	789323	Glaucoma diagnosis
MedicationRequest	789324	Latanoprost prescription
Encounter	789325	Glaucoma follow-up


FHIR server: https://hapi.fhir.org/baseR4

Demonstration
See the uploaded project demonstration video for the Streamlit dashboard, Python code, record transfer, and verification workflow. Screenshots can also be placed in the optional demo/ directory.
Outcome
Demonstrated retrieval, clinical display, HTTP transfer, local persistence, and verification of six FHIR R4 resources between a public test server and a separate local receiving service.

Limitations and privacy
- Educational purpose.
- Hospital B is a simplified Python HTTP receiver rather than a complete FHIR server.
- The transfer uses a transaction-shaped JSON Bundle
- The public HAPI server is not suitable for real patient information; do not upload real patient data.
  
Author
Project developed as a practical exercise in healthcare interoperability, FHIR APIs, Python, and Streamlit.

