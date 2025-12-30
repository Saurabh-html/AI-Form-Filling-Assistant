import streamlit as st
from PIL import Image
import sys
import os

sys.path.append(os.path.abspath("backend"))

# OCR
from ocr.google_docs_style_ocr import extract_text_google_docs_style

# Classification + extraction
from extraction.document_classifier import classify_document
from extraction.aadhaar_zone_extractor import extract_aadhaar_zone_based
from extraction.pan_zone_extractor import extract_pan_zone_based
from extraction.driving_license_zone_extractor import extract_driving_license_zone_based
from extraction.education_certificate_zone_extractor import extract_education_certificate_zone_based
from extraction.unified_extractor import extract_fields

# Forms + PDF
from forms.form_templates import FORMS
from forms.form_filler import fill_form
from forms.pdf_generator import generate_form_pdf

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="AI Government Form Auto-Filling",
    layout="wide"
)

st.markdown("""
<style>
h1 { color: #0f172a; }
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

st.title("🧾 AI-Powered Government Form Auto-Filling System")

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("extracted_documents", [])
st.session_state.setdefault("unified_data", None)
st.session_state.setdefault("filled_form", None)

# ---------------- UPLOAD ----------------
uploaded_files = st.file_uploader(
    "Upload Identity Documents (Aadhaar / PAN / DL / Certificates)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ---------------- OCR + EXTRACTION ----------------
if uploaded_files and st.button("🔍 Extract Information"):
    st.session_state.extracted_documents = []

    with st.spinner("Running OCR and extracting data..."):
        for file in uploaded_files:
            image = Image.open(file).convert("RGB")
            ocr_output = extract_text_google_docs_style(image)

            text = ocr_output.get("text", "")
            tokens = ocr_output.get("tokens", [])

            doc_type = classify_document(text)

            if doc_type == "AADHAAR":
                data = extract_aadhaar_zone_based(text, tokens)
            elif doc_type == "PAN":
                data = extract_pan_zone_based(text)
            elif doc_type == "DRIVING_LICENSE":
                data = extract_driving_license_zone_based(text)
            elif doc_type == "EDUCATION":
                data = extract_education_certificate_zone_based(text)
            else:
                continue

            st.session_state.extracted_documents.append({
                "document_type": doc_type,
                "data": data
            })

        st.session_state.unified_data = extract_fields(
            st.session_state.extracted_documents
        )

    st.success("Extraction completed successfully!")

# ---------------- SHOW UNIFIED DATA ----------------
if st.session_state.unified_data:
    st.subheader("📦 Extracted Unified Data")
    st.json(st.session_state.unified_data)

    # ---------------- FORM SELECTION ----------------
    st.subheader("📝 Select Government Form")

    form_key = st.selectbox(
        "Choose a form",
        list(FORMS.keys()),
        format_func=lambda k: FORMS[k]["title"]
    )

    if st.button("⚡ Auto-Fill Form"):
        st.session_state.filled_form = fill_form(
            FORMS[form_key],
            st.session_state.unified_data
        )

# ---------------- SHOW FORM + PDF ----------------
if st.session_state.filled_form:
    st.subheader("📄 Auto-Filled Form")

    filled = st.session_state.filled_form

    for field, value in filled["fields"].items():
        st.text_input(
            field.replace("_", " ").title(),
            value=value,
            key=f"form_{field}"
        )

    pdf_buffer = generate_form_pdf(filled)

    st.download_button(
        "⬇️ Download Filled Form (PDF)",
        data=pdf_buffer,
        file_name=f"{filled.get('form_id', 'government_form')}.pdf",
        mime="application/pdf"
    )
