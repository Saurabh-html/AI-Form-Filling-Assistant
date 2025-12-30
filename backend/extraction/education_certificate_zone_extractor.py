import re


YEAR_REGEX = r"\b(19|20)\d{2}\b"


def extract_education_certificate_zone_based(raw_text: str) -> dict:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    upper_lines = [l.upper() for l in lines]

    data = {
        "document_type": "EDUCATION_CERTIFICATE",
        "student_name": {"value": "", "confidence": 0},
        "father_name": {"value": "", "confidence": 0},
        "mother_name": {"value": "", "confidence": 0},
        "date_of_birth": {"value": "", "confidence": 0},
        "roll_number": {"value": "", "confidence": 0},
        "examination": {"value": "", "confidence": 0},
        "year_of_passing": {"value": "", "confidence": 0},
        "board": {"value": "", "confidence": 0},
        "school": {"value": "", "confidence": 0}
    }

    # --------------------------------------------------
    # 1️⃣ BOARD DETECTION
    # --------------------------------------------------
    for line in upper_lines:
        if any(b in line for b in ["CBSE", "ICSE", "STATE BOARD", "BOARD OF"]):
            data["board"]["value"] = line
            data["board"]["confidence"] = 0.95
            break

    # --------------------------------------------------
    # 2️⃣ EXAMINATION TYPE
    # --------------------------------------------------
    for line in upper_lines:
        if any(x in line for x in ["SECONDARY", "MATRIC", "SSC"]):
            data["examination"]["value"] = "SECONDARY"
            data["examination"]["confidence"] = 0.9

        if any(x in line for x in ["SENIOR SECONDARY", "INTERMEDIATE", "HSC"]):
            data["examination"]["value"] = "SENIOR SECONDARY"
            data["examination"]["confidence"] = 0.9

    # --------------------------------------------------
    # 3️⃣ ROLL NUMBER
    # --------------------------------------------------
    for i, line in enumerate(upper_lines):
        if "ROLL" in line and i + 1 < len(lines):
            data["roll_number"]["value"] = lines[i + 1]
            data["roll_number"]["confidence"] = 0.95
            break

    # --------------------------------------------------
    # 4️⃣ DATE OF BIRTH
    # --------------------------------------------------
    for line in lines:
        m = re.search(r"\d{2}/\d{2}/\d{4}", line)
        if m:
            data["date_of_birth"]["value"] = m.group()
            data["date_of_birth"]["confidence"] = 0.95
            break

    # --------------------------------------------------
    # 5️⃣ STUDENT NAME
    # --------------------------------------------------
    for i, line in enumerate(lines):
        if "NAME" in upper_lines[i] and i + 1 < len(lines):
            if re.fullmatch(r"[A-Z][A-Z ]{3,}", lines[i + 1]):
                data["student_name"]["value"] = lines[i + 1]
                data["student_name"]["confidence"] = 0.95
                break

    # --------------------------------------------------
    # 6️⃣ FATHER / MOTHER
    # --------------------------------------------------
    for i, line in enumerate(upper_lines):
        if "FATHER" in line and i + 1 < len(lines):
            data["father_name"]["value"] = lines[i + 1]
            data["father_name"]["confidence"] = 0.95

        if "MOTHER" in line and i + 1 < len(lines):
            data["mother_name"]["value"] = lines[i + 1]
            data["mother_name"]["confidence"] = 0.95

    # --------------------------------------------------
    # 7️⃣ YEAR OF PASSING
    # --------------------------------------------------
    for line in upper_lines:
        m = re.search(YEAR_REGEX, line)
        if m:
            data["year_of_passing"]["value"] = m.group()
            data["year_of_passing"]["confidence"] = 0.9
            break

    # --------------------------------------------------
    # 8️⃣ SCHOOL NAME (OPTIONAL)
    # --------------------------------------------------
    for line in lines:
        if "SCHOOL" in line.upper() and len(line) > 10:
            data["school"]["value"] = line
            data["school"]["confidence"] = 0.85
            break

    return data
