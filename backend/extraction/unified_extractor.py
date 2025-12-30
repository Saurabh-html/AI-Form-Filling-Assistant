from schemas.unified_schema import UNIFIED_SCHEMA
from utils.name import clean_name
from utils.address import clean_address
from utils.dob import parse_dob


def get_value(field):
    """
    Safely extract value from:
    - string
    - { value, confidence }
    """
    if isinstance(field, dict):
        return field.get("value", "")
    if isinstance(field, str):
        return field
    return ""


def choose_better(existing, new):
    """
    Golden rule:
    Never replace a good value with a worse one
    """
    if not new:
        return existing
    if not existing:
        return new
    if len(new) > len(existing):
        return new
    return existing


def extract_fields(extracted_documents: list) -> dict:
    """
    extracted_documents = [
        {
            "document_type": "AADHAAR",
            "data": { ... }
        },
        {
            "document_type": "PAN",
            "data": { ... }
        }
    ]
    """

    unified = UNIFIED_SCHEMA.copy()

    # Ensure list fields are fresh
    unified["education"] = []
    unified["documents_used"] = []

    for doc in extracted_documents:
        if not isinstance(doc, dict):
            continue

        dtype = doc.get("document_type")
        data = doc.get("data", {})

        if not dtype or not isinstance(data, dict):
            continue

        unified["documents_used"].append(dtype)

        # ---------------- NAME ----------------
        unified["name"] = choose_better(
            unified["name"],
            clean_name(get_value(data.get("name")))
        )

        # ---------------- FATHER / GUARDIAN ----------------
        unified["father_or_guardian"] = choose_better(
            unified["father_or_guardian"],
            get_value(data.get("father_or_guardian"))
        )

        # ---------------- DOB ----------------
        unified["date_of_birth"] = choose_better(
            unified["date_of_birth"],
            parse_dob(get_value(data.get("date_of_birth")))
        )

        # ---------------- GENDER ----------------
        unified["gender"] = choose_better(
            unified["gender"],
            get_value(data.get("gender"))
        )

        # ---------------- MOBILE ----------------
        unified["mobile_number"] = choose_better(
            unified["mobile_number"],
            get_value(data.get("mobile_number"))
        )

        # ---------------- AADHAAR ----------------
        unified["aadhaar_number"] = choose_better(
            unified["aadhaar_number"],
            get_value(data.get("aadhaar_number"))
        )

        # ---------------- PAN ----------------
        unified["pan_number"] = choose_better(
            unified["pan_number"],
            get_value(data.get("pan_number"))
        )

        # ---------------- ADDRESS ----------------
        unified["address"] = choose_better(
            unified["address"],
            clean_address(get_value(data.get("address")))
        )

        # ---------------- EDUCATION ----------------
        if isinstance(data.get("education"), list):
            unified["education"].extend(data["education"])

    return unified
