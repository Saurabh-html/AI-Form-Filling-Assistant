import re


DL_REGEX = r"[A-Z]{2}\s?\d{2}\s?\d{11}"
RELATION_PREFIX = ("S/O", "D/O", "W/O")


def extract_driving_license_zone_based(raw_text: str) -> dict:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    upper_lines = [l.upper() for l in lines]

    data = {
        "document_type": "DRIVING_LICENSE",
        "name": {"value": "", "confidence": 0},
        "father_or_spouse": {"value": "", "confidence": 0},
        "date_of_birth": {"value": "", "confidence": 0},
        "dl_number": {"value": "", "confidence": 0},
        "issue_date": {"value": "", "confidence": 0},
        "valid_till": {"value": "", "confidence": 0},
        "address": {"value": "", "confidence": 0}
    }

    # --------------------------------------------------
    # 1️⃣ DL NUMBER (ABSOLUTE PRIORITY)
    # --------------------------------------------------
    for line in upper_lines:
        m = re.search(DL_REGEX, line)
        if m:
            data["dl_number"]["value"] = m.group().replace(" ", "")
            data["dl_number"]["confidence"] = 0.99
            break

    # --------------------------------------------------
    # 2️⃣ DATE EXTRACTION
    # --------------------------------------------------
    dates = re.findall(r"\d{2}/\d{2}/\d{4}", raw_text)

    if len(dates) >= 1:
        data["date_of_birth"]["value"] = dates[0]
        data["date_of_birth"]["confidence"] = 0.95

    if len(dates) >= 2:
        data["issue_date"]["value"] = dates[1]
        data["issue_date"]["confidence"] = 0.9

    if len(dates) >= 3:
        data["valid_till"]["value"] = dates[2]
        data["valid_till"]["confidence"] = 0.9

    # --------------------------------------------------
    # 3️⃣ NAME + RELATION
    # --------------------------------------------------
    for i, line in enumerate(lines):
        if re.fullmatch(r"[A-Z][A-Z ]{3,}", line) and "GOVT" not in line.upper():
            data["name"]["value"] = line
            data["name"]["confidence"] = 0.9

            if i + 1 < len(lines) and lines[i + 1].startswith(RELATION_PREFIX):
                data["father_or_spouse"]["value"] = lines[i + 1]
                data["father_or_spouse"]["confidence"] = 0.95
            break

    # --------------------------------------------------
    # 4️⃣ ADDRESS ZONE
    # --------------------------------------------------
    address_lines = []
    collecting = False

    for line in lines:
        if "ADDRESS" in line.upper():
            collecting = True
            continue

        if collecting:
            if re.search(DL_REGEX, line):
                break
            address_lines.append(line)

    if address_lines:
        data["address"]["value"] = " ".join(address_lines)
        data["address"]["confidence"] = 0.9

    return data
