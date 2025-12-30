def aggregate_confidence(tokens):
    """
    tokens: list of OCR tokens contributing to a field
    Each token = {"text": "...", "confidence": float}

    Returns float confidence
    """
    if not tokens:
        return 0.0

    scores = [t["confidence"] for t in tokens if "confidence" in t]
    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 2)
