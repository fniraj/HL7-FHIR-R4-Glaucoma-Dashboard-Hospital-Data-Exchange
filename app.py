import requests
import streamlit as st

st.set_page_config(page_title="FHIR Glaucoma Dashboard", page_icon="👁️", layout="wide")
BASE_URL = "https://hapi.fhir.org/baseR4"
PATIENT_ID = "789264"

@st.cache_data(ttl=60)
def get_resource(resource_type, resource_id):
    response = requests.get(f"{BASE_URL}/{resource_type}/{resource_id}", headers={"Accept": "application/fhir+json"}, timeout=20)
    response.raise_for_status()
    return response.json()

st.title("FHIR Glaucoma Patient Dashboard")
st.caption("FHIR R4 • HAPI FHIR public test server • Training data")

try:
    patient = get_resource("Patient", PATIENT_ID)
    name = patient.get("name", [{}])[0]
    full_name = " ".join(name.get("given", []) + [name.get("family", "")]).strip()
    st.subheader("Patient information")
    a, b, c = st.columns(3)
    a.metric("Patient", full_name or "Unknown")
    b.metric("Gender", patient.get("gender", "Unknown"))
    c.metric("Date of birth", patient.get("birthDate", "Unknown"))

    st.subheader("Intraocular pressure")
    a, b = st.columns(2)
    for column, eye, obs_id in [(a, "Right eye", "789321"), (b, "Left eye", "789322")]:
        obs = get_resource("Observation", obs_id)
        quantity = obs.get("valueQuantity", {})
        column.metric(eye, f"{quantity.get('value', 'N/A')} {quantity.get('unit', 'mmHg')}")

    condition = get_resource("Condition", "789323")
    medication = get_resource("MedicationRequest", "789324")
    encounter = get_resource("Encounter", "789325")
    st.subheader("Clinical information")
    a, b = st.columns(2)
    with a:
        st.write("**Diagnosis:**", condition.get("code", {}).get("text", "Unknown"))
        st.write("**Medication:**", medication.get("medicationCodeableConcept", {}).get("text", "Unknown"))
    with b:
        st.write("**Encounter status:**", encounter.get("status", "Unknown"))
        reasons = encounter.get("reasonCode", [])
        st.write("**Visit reason:**", reasons[0].get("text", "Unknown") if reasons else "Unknown")
    st.success("FHIR resources retrieved successfully.")
except requests.RequestException as exc:
    st.error(f"Could not retrieve FHIR data: {exc}. Public test records may expire or be removed.")
except (KeyError, IndexError, TypeError, ValueError) as exc:
    st.error(f"Unexpected FHIR response: {exc}")
