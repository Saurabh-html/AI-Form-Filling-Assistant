import re

# -------------------------------
# Light name cleaner (NOT strict)
# -------------------------------

BLOCK_WORDS = {
    "INDIA", "GOVERNMENT", "AUTHORITY", "UIDAI",
    "INCOME", "TAX", "DEPARTMENT", "OF"
}


def clean_name(name: str) -> str:
    """
    Cleans OCR-extracted person names.
    Removes headers, authorities, junk.
    """

    if not name:
        return ""

    name = name.upper().strip()

    # Remove non-alphabetic noise
    name = re.sub(r"[^A-Z ]", "", name)
    name = re.sub(r"\s+", " ", name)

    # Block obvious non-name headers
    if any(word in name for word in BLOCK_WORDS):
        return ""

    words = name.split()

    # Indian names usually 2–4 words
    if not (2 <= len(words) <= 4):
        return ""

    return name


# -------------------------------
# Backward compatibility
# -------------------------------
def extract_applicant_name(text: str) -> str:
    """
    Legacy helper (kept so nothing else breaks)
    """
    return clean_name(text)
