def aggregate_fields(extracted_documents: list) -> dict:
    """
    Combine multiple document extraction outputs into one unified profile
    """

    # ---------------- PRIORITY RULES ----------------
    PRIORITY = {
        "name": ["PAN", "AADHAAR", "DRIVING_LICENSE", "EDUCATION_CERTIFICATE"],
        "father_name": ["PAN", "AADHAAR", "DRIVING_LICENSE"],
        "father_or_guardian": ["PAN", "AADHAAR", "DRIVING_LICENSE"],
        "date_of_birth": ["AADHAAR", "PAN", "DRIVING_LICENSE", "EDUCATION_CERTIFICATE"],
        "gender": ["AADHAAR", "DRIVING_LICENSE"],
        "address": ["AADHAAR", "DRIVING_LICENSE"],
        "aadhaar_number": ["AADHAAR"],
        "pan_number": ["PAN"],
        "dl_number": ["DRIVING_LICENSE"],
        "roll_number": ["EDUCATION_CERTIFICATE"],
        "year_of_passing": ["EDUCATION_CERTIFICATE"],
        "board": ["EDUCATION_CERTIFICATE"]
    }

    unified = {}

    # ---------------- HELPER ----------------
    def get_value(field_data):
        if isinstance(field_data, dict):
            return field_data.get("value", "").strip()
        return str(field_data).strip()

    # ---------------- AGGREGATION ----------------
    for field, sources in PRIORITY.items():
        for doc in extracted_documents:
            doc_type = doc.get("document_type")

            if doc_type not in sources:
                continue

            if field not in doc:
                continue

            value = get_value(doc[field])

            if value:
                unified[field] = value
                break

        if field not in unified:
            unified[field] = ""

    return unified
