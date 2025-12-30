import cv2
import numpy as np


def confidence_color(conf):
    if conf >= 0.85:
        return (0, 200, 0)      # Green
    elif conf >= 0.6:
        return (0, 200, 255)    # Yellow
    return (0, 0, 255)          # Red


def draw_ocr_boxes(pil_image, tokens):
    """
    Draw OCR bounding boxes with confidence coloring
    """

    img = np.array(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for token in tokens:
        box = token.get("box")
        conf = token.get("confidence", 0)

        if not box or len(box) != 4:
            continue

        pts = np.array(box, dtype=np.int32)
        color = confidence_color(conf)

        cv2.polylines(img, [pts], isClosed=True, color=color, thickness=2)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
