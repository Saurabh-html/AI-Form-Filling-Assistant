import cv2
import numpy as np
from paddleocr import PaddleOCR
import threading

# -------------------------------
# Thread-safe OCR singleton
# -------------------------------
_ocr_lock = threading.Lock()
_ocr_instance = None


def get_ocr():
    global _ocr_instance
    if _ocr_instance is None:
        _ocr_instance = PaddleOCR(
            lang="en",
            use_angle_cls=True
        )
    return _ocr_instance


def extract_text_google_docs_style(image):
    """
    Returns:
    {
        "text": str,
        "tokens": [
            {
                "text": "...",
                "confidence": float,
                "box": [[x,y], ...]
            }
        ]
    }
    """

    # Convert PIL → OpenCV safely
    img = np.array(image)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    ocr = get_ocr()

    with _ocr_lock:
        result = ocr.ocr(img)

    if not result:
        return {"text": "", "tokens": []}

    full_text = []
    tokens = []

    # PaddleOCR (dict-style output)
    block = result[0]
    texts = block.get("rec_texts", [])
    scores = block.get("rec_scores", [])
    boxes = block.get("rec_polys", [])

    for text, score, box in zip(texts, scores, boxes):
        if text.strip():
            full_text.append(text)
            tokens.append({
                "text": text,
                "confidence": float(score),
                "box": box.tolist()
            })

    return {
        "text": "\n".join(full_text),
        "tokens": tokens
    }
