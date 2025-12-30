import re
from utils.confidence import aggregate_confidence

RELATION_PATTERN = re.compile(r"^(S/O|D/O|W/O)\s*[:\-]?\s*(.*)$", re.IGNORECASE)

ADDRESS_KEYWORDS = {
    "WARD", "DIST", "DISTRICT", "PO", "PIN", "STATE",
    "BIHAR", "UTTAR", "PRADESH", "KATHAUR", "ROAD"
}


def is_address_line(text):
    upper = text.upper()
    return any(word in upper for word in ADDRESS_KEYWORDS)


def extract_guardian(tokens):
    """
    tokens: OCR tokens list (ordered)

    Returns:
    {
        "value": "Dharmendra Pandey",
        "relation_type": "S/O",
        "confidence": float,
        "source_tokens": [...]
    }
    """

    for i, token in enumerate(tokens):
        text = token["text"].strip()

        match = RELATION_PATTERN.match(text)
        if not match:
            continue

        relation = match.group(1).upper()
        name_part = match.group(2).strip()

        source_tokens = [token]
        full_name_parts = [name_part]

        # Look ahead for surname (next lines)
        j = i + 1
        while j < len(tokens):
            next_text = tokens[j]["text"].strip()

            if not next_text:
                break

            if is_address_line(next_text):
                break

            # Stop if numeric or punctuation-heavy
            if any(char.isdigit() for char in next_text):
                break

            # Likely surname or continuation
            full_name_parts.append(next_text.rstrip(","))
            source_tokens.append(tokens[j])

            j += 1

        full_name = " ".join(full_name_parts).strip()

        confidence = aggregate_confidence(source_tokens)

        return {
            "value": full_name,
            "relation_type": relation,
            "confidence": confidence,
            "source_tokens": source_tokens
        }

    return {
        "value": "",
        "relation_type": "",
        "confidence": 0.0,
        "source_tokens": []
    }
