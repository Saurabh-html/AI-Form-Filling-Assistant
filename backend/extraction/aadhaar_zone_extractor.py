import re


# ---------------- CONSTANTS ----------------
NAME_BLACKLIST = {
    "INDIA", "GOVERNMENT", "UNIQUE", "IDENTIFICATION",
    "AUTHORITY", "AADHAAR", "OF"
}


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def is_valid_person_name(w1: str, w2: str) -> bool:
    if w1.upper() in NAME_BLACKLIST or w2.upper() in NAME_BLACKLIST:
        return False
    if not (w1.isalpha() and w2.isalpha()):
        return False
    if not (w1.istitle() and w2.istitle()):
        return False
    return True


def extract_aadhaar_zone_based(raw_text: str, tokens: list) -> dict:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    data = {
        "document_type": "AADHAAR",
        "name": {"value": "", "confidence": 0},
        "father_or_guardian": {"value": "", "confidence": 0},
        "date_of_birth": {"value": "", "confidence": 0},
        "gender": {"value": "", "confidence": 0},
        "mobile_number": {"value": "", "confidence": 0},
        "aadhaar_number": {"value": "", "confidence": 0},
        "address": {"value": "", "confidence": 0},
    }

    # --------------------------------------------------
    # 1️⃣ NAME (BLACKLISTED + ADJACENT TOKENS)
    # --------------------------------------------------
    for i in range(len(tokens) - 1):
        w1 = tokens[i]["text"].strip()
        w2 = tokens[i + 1]["text"].strip()

        if is_valid_person_name(w1, w2):
            data["name"]["value"] = f"{w1} {w2}"
            data["name"]["confidence"] = round(
                (tokens[i]["confidence"] + tokens[i + 1]["confidence"]) / 2, 2
            )
            break

    # --------------------------------------------------
    # 2️⃣ FATHER / GUARDIAN (MULTI-TOKEN)
    # --------------------------------------------------
    for i, token in enumerate(tokens):
        text = token["text"]

        if text.upper().startswith(("S/O", "D/O", "W/O")):
            parts = []

            clean = re.sub(r"^(S/O|D/O|W/O)\s*[:\-]?\s*", "", text, flags=re.I)
            parts.append(clean)

            if i + 1 < len(tokens):
                nxt = tokens[i + 1]["text"].replace(",", "")
                if nxt.isalpha():
                    parts.append(nxt)

            data["father_or_guardian"]["value"] = normalize_spaces(" ".join(parts))
            data["father_or_guardian"]["confidence"] = round(token["confidence"], 2)
            break

    # --------------------------------------------------
    # 3️⃣ DOB (FUZZY MATCH: DOB / D0B / DATE)
    # --------------------------------------------------
    for i, line in enumerate(lines):
        if re.search(r"(DOB|D0B|DATE\s*OF\s*BIRTH)", line.upper()):
            m = re.search(r"\d{2}/\d{2}/\d{4}", line)
            if not m and i + 1 < len(lines):
                m = re.search(r"\d{2}/\d{2}/\d{4}", lines[i + 1])
            if m:
                data["date_of_birth"]["value"] = m.group()
                data["date_of_birth"]["confidence"] = 0.95
                break

    # --------------------------------------------------
    # 4️⃣ GENDER
    # --------------------------------------------------
    for token in tokens:
        if token["text"].upper() in {"MALE", "FEMALE", "OTHER"}:
            data["gender"]["value"] = token["text"].upper()
            data["gender"]["confidence"] = 1.0
            break

    # --------------------------------------------------
    # 5️⃣ MOBILE NUMBER
    # --------------------------------------------------
    for token in tokens:
        m = re.search(r"\b[6-9]\d{9}\b", token["text"])
        if m:
            data["mobile_number"]["value"] = m.group()
            data["mobile_number"]["confidence"] = 1.0
            break

    # --------------------------------------------------
    # 6️⃣ AADHAAR NUMBER (MULTI-LINE SAFE)
    # --------------------------------------------------
    m = re.search(r"(\d{4})\s*(\d{4})\s*(\d{4})", raw_text)
    if m:
        data["aadhaar_number"]["value"] = "".join(m.groups())
        data["aadhaar_number"]["confidence"] = 0.98

    # --------------------------------------------------
    # 7️⃣ ADDRESS (CUT AFTER AADHAAR)
    # --------------------------------------------------
    address_lines = []
    collecting = False

    for line in lines:
        if "ADDRESS" in line.upper():
            collecting = True
            continue

        if collecting:
            if re.search(r"\d{4}\s*\d{4}\s*\d{4}", line):
                break
            address_lines.append(line)

    if address_lines:
        data["address"]["value"] = normalize_spaces(" ".join(address_lines))
        data["address"]["confidence"] = 0.95

    return data
