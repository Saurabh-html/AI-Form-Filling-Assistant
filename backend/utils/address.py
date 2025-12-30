import re

def clean_address(addr):
    if not addr:
        return ""
    STOP_PATTERNS = [
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "VID", "@", "WWW", "HTTP"
    ]
    for p in STOP_PATTERNS:
        idx = addr.upper().find(p)
        if idx != -1:
            addr = addr[:idx]
    return addr.strip()
