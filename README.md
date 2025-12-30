![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![OCR](https://img.shields.io/badge/OCR-PaddleOCR-green)

# 🧠 AI-Powered Government Form Auto-Filling System

An intelligent OCR-based system that extracts information from Indian identity documents (Aadhaar, PAN, Driving License, Education Certificates) and automatically fills government application forms with downloadable PDFs.

---

## 🚀 Features

✅ Google Docs–style OCR accuracy (PaddleOCR)  
✅ Multi-document upload support  
✅ Zone-based extraction for Indian documents  
✅ Unified data aggregation (no overwriting)  
✅ Auto-filled government forms  
✅ Downloadable professional PDFs  
✅ Ashoka Emblem & official formatting  
✅ Streamlit-based interactive UI  

---

## 🏗️ System Architecture

![System Architecture](assets/screenshots/methodology.png)

---

## 🪪 Supported Documents

| Document Type | Supported |
|---------------|-----------|
| Aadhaar Card | ✅ |
| PAN Card | ✅ |
| Driving License | ✅ |
| 10th / 12th Certificates | ✅ |

---

## 📋 Supported Forms

- Government Scholarship Application  
- Government Job Application (Basic)  
- Address Verification Form  

---

## 🖼️ Screenshots

### Upload & OCR Extraction
![OCR Output](assets/screenshots/ocr_output.png)

### Unified Extracted Data
![Unified Data](assets/screenshots/unified_data.png)

### Auto-Filled Form UI
![Auto Filled UI](assets/screenshots/form_ui.png)

### Generated PDF
![PDF Output](assets/screenshots/pdf_output.png)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** – UI
- **PaddleOCR** – OCR Engine
- **OpenCV** – Image processing
- **ReportLab** – PDF generation

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/AI-Form-Filling-Assistant.git
cd AI-Form-Filling-Assistant
2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Run Application

streamlit run frontend/app.py
📂 Project Structure

AI_FORM_FILLING_ASSISTANT/
│
├── backend/
│   ├── ocr/
│   ├── extraction/
│   ├── forms/
│   ├── utils/
│   └── schemas/
│
├── frontend/
│   └── app.py
│
├── assets/
│   ├── screenshots/
│   └── ashoka_emblem.png
│
├── samples/
├── requirements.txt
└── README.md
🎯 Use Case
This system helps:

Students filling scholarship forms

Job applicants

Government service applicants

Digital onboarding platforms

🔒 Disclaimer
This project is for educational and demonstration purposes only.
No sensitive data is stored or transmitted.

👨‍🎓 Author
Saurabh Suman
B.Tech Final Year Student
Computer Science and Design

📫 Feel free to connect for collaboration or improvements.

🌟 Future Enhancements
DigiLocker integration

Hindi + regional language OCR

Face matching verification

Web deployment

Form submission APIs