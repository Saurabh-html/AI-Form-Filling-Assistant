import re


# ---------------- CONSTANTS ----------------
PAN_REGEX = r"[A-Z]{5}[0-9]{4}[A-Z]"
NAME_BLACKLIST = {
    "INCOME", "TAX", "DEPARTMENT", "GOVERNMENT",
    "INDIA", "PERMANENT", "ACCOUNT", "NUMBER",
    "CARD", "SIGNATURE"
}


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def is_valid_pan_name(text: str) -> bool:
    words = text.split()

    if not (2 <= len(words) <= 4):
        return False

    for w in words:
        if not w.isalpha():
            return False
        if w.upper() in NAME_BLACKLIST:
            return False
        if not w[0].isupper():
            return False

    return True


def extract_pan_zone_based(raw_text: str) -> dict:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    upper_lines = [l.upper() for l in lines]

    data = {
        "document_type": "PAN",
        "name": {"value": "", "confidence": 0},
        "father_name": {"value": "", "confidence": 0},
        "date_of_birth": {"value": "", "confidence": 0},
        "pan_number": {"value": "", "confidence": 0},
    }

    # --------------------------------------------------
    # 1️⃣ PAN NUMBER (ABSOLUTE PRIORITY)
    # --------------------------------------------------
    for line in upper_lines:
        m = re.search(PAN_REGEX, line)
        if m:
            data["pan_number"]["value"] = m.group()
            data["pan_number"]["confidence"] = 0.99
            break

    # --------------------------------------------------
    # 2️⃣ NAME & FATHER NAME (LABEL-BASED)
    # --------------------------------------------------
    for i, line in enumerate(upper_lines):
        # Applicant Name
        if "NAME" == line or line.endswith("/NAME"):
            if i + 1 < len(lines) and is_valid_pan_name(lines[i + 1]):
                data["name"]["value"] = lines[i + 1]
                data["name"]["confidence"] = 0.95

        # Father Name
        if "FATHER" in line and "NAME" in line:
            if i + 1 < len(lines) and is_valid_pan_name(lines[i + 1]):
                data["father_name"]["value"] = lines[i + 1]
                data["father_name"]["confidence"] = 0.95

    # --------------------------------------------------
    # 3️⃣ FALLBACK NAME LOGIC (OLD PAN / OCR NOISE)
    # --------------------------------------------------
    if not data["name"]["value"]:
        for line in lines:
            if is_valid_pan_name(line):
                data["name"]["value"] = line
                data["name"]["confidence"] = 0.85
                break

    # --------------------------------------------------
    # 4️⃣ DATE OF BIRTH (STRICT CONTEXT)
    # --------------------------------------------------
    for i, line in enumerate(upper_lines):
        if "DATE OF BIRTH" in line or "DOB" in line:
            if i + 1 < len(lines):
                m = re.search(r"\d{2}/\d{2}/\d{4}", lines[i + 1])
                if m:
                    data["date_of_birth"]["value"] = m.group()
                    data["date_of_birth"]["confidence"] = 0.95
                    break

    return data
