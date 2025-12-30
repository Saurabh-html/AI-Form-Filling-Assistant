def map_to_form_1(extracted: dict) -> dict:
    """
    Maps extracted entities to Form 1 (Citizen Application).
    """
    return {
        "Applicant Name": extracted.get("name", ""),
        "Father / Spouse Name": extracted.get("father_name", ""),
        "Date of Birth": extracted.get("date_of_birth", ""),
        "PAN Number": extracted.get("pan_number", ""),
        "Aadhaar Number": extracted.get("aadhaar_number", ""),
    }


def map_to_form_2(extracted: dict) -> dict:
    """
    Maps extracted entities to Form 2 (Welfare Scheme).
    """
    identity = extracted.get("aadhaar_number") or extracted.get("pan_number")

    return {
        "Beneficiary Name": extracted.get("name", ""),
        "Guardian Name": extracted.get("father_name", ""),
        "Date of Birth": extracted.get("date_of_birth", ""),
        "Identity Proof Number": identity,
    }
