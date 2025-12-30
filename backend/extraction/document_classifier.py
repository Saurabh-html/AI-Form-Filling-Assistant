def classify_document(text: str) -> str:
    """
    Classifies document type based on keywords.
    Returns one of:
    AADHAAR, PAN, DRIVING_LICENSE, EDUCATION, UNKNOWN
    """

    if not text:
        return "UNKNOWN"

    t = text.upper()

    # Aadhaar
    if any(k in t for k in [
        "UNIQUE IDENTIFICATION",
        "AADHAAR",
        "UIDAI"
    ]):
        return "AADHAAR"

    # PAN
    if any(k in t for k in [
        "INCOME TAX DEPARTMENT",
        "PERMANENT ACCOUNT NUMBER",
        "PAN"
    ]):
        return "PAN"

    # Driving License
    if any(k in t for k in [
        "DRIVING LICENCE",
        "DRIVING LICENSE",
        "DL NO"
    ]):
        return "DRIVING_LICENSE"

    # Education Certificates
    if any(k in t for k in [
        "SECONDARY SCHOOL",
        "SENIOR SECONDARY",
        "MARKSHEET",
        "BOARD OF",
        "CERTIFICATE"
    ]):
        return "EDUCATION"

    return "UNKNOWN"
