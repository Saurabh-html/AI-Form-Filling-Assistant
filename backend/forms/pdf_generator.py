from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import textwrap
import os


def generate_form_pdf(filled_form: dict):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    x_margin = 50
    y = height - 50

    # ---------------- Ashoka Emblem ----------------
    emblem_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "assets",
        "ashoka_emblem.png"
    )

    if os.path.exists(emblem_path):
        c.drawImage(
            emblem_path,
            width / 2 - 30,
            y - 60,
            width=60,
            height=60,
            preserveAspectRatio=True,
            mask="auto"
        )

    y -= 80

    # ---------------- Title ----------------
    c.setFont("Times-Bold", 16)
    c.drawCentredString(width / 2, y, filled_form["title"])

    y -= 25
    c.setFont("Times-Roman", 10)
    c.drawCentredString(
        width / 2,
        y,
        f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
    )

    y -= 15
    c.line(x_margin, y, width - x_margin, y)
    y -= 30

    # ---------------- Section Header ----------------
    c.setFont("Times-Bold", 12)
    c.drawString(x_margin, y, "Applicant Details")
    y -= 20

    # ---------------- Form Fields ----------------
    c.setFont("Times-Roman", 11)

    for field, value in filled_form["fields"].items():
        label = field.replace("_", " ").title()
        value = value if value else "-"

        c.drawString(x_margin, y, f"{label}:")

        # ✅ FIXED WRAPPING (SAFE FOR A4)
        wrapped_lines = textwrap.wrap(value, 60)
        text_x = x_margin + 170

        first = True
        for line in wrapped_lines:
            if first:
                c.drawString(text_x, y, line)
                first = False
            else:
                y -= 14
                c.drawString(text_x, y, line)

        y -= 20

        # Page break safety
        if y < 120:
            c.showPage()
            c.setFont("Times-Roman", 11)
            y = height - 50

    # ---------------- Footer ----------------
    footer_y = 45
    c.setFont("Times-Italic", 9)
    c.drawCentredString(
        width / 2,
        footer_y,
        "This is a computer-generated document. No signature is required."
    )

    c.save()
    buffer.seek(0)
    return buffer
