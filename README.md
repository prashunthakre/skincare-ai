# 🩺 SkinCare AI - Intelligent Dermatological Diagnosis & Advisory Platform

![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**SkinCare AI** is a state-of-the-art web application powered by **Deep Learning (MobileNetV2)** and **Streamlit**. It provides instant skin lesion analysis, personalized skincare advice, automated PDF report generation, and real-time nearby doctor recommendations.

---

## ✨ Key Features

- 🔬 **AI Skin Lesion Classifier**: High-accuracy Transfer Learning model (MobileNetV2) trained to detect 9+ skin diseases & conditions:
  - Melanoma (Skin Cancer)
  - Basal Cell Carcinoma (BCC)
  - Eczema
  - Atopic Dermatitis
  - Psoriasis & Lichen Planus
  - Fungal Infections (Tinea, Ringworm, Candidiasis)
  - Warts & Viral Infections
  - Melanocytic Nevi (NV)
  - Benign Keratosis (BKL)

- 🤖 **Interactive AI Dermatology Chatbot**: Context-aware assistant to help users evaluate symptoms, skincare routines, and precautions.
- 📍 **Doctor & Clinic Matcher**: Integrates OpenStreetMap Nominatim API to find verified dermatologists and skin clinics near your location.
- 📄 **Automated Medical PDF Generator**: Download comprehensive diagnostic reports with confidence scores, risk severity, and care instructions.
- 🔐 **Secure User Authentication**: Complete registration and login system backed by SQLite and hashed passkeys.
- 💎 **Modern Responsive Design**: Custom CSS styling with modern typography, dynamic animations, and dark/light glassmorphism elements.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit, Custom CSS, Extra Streamlit Components
- **Backend / Machine Learning**: TensorFlow 2.15, Keras, Scikit-learn, NumPy, Pandas, Pillow
- **APIs & Services**: OpenStreetMap Nominatim API
- **PDF Engine**: FPDF
- **Database**: SQLite3

---

## 📁 Repository Structure

```text
├── backend/
│   ├── model.h5             # Trained MobileNetV2 Keras Model
│   ├── model.py             # Preprocessing & Inference pipeline
│   ├── class_indices.json   # Disease class labels mapping
│   ├── advisory.py          # Detailed clinical guidance & recommendations
│   ├── chatbot.py           # AI Chatbot logic
│   ├── doctor.py            # Nominatim OpenStreetMap Doctor search
│   ├── report.py            # PDF report generator engine
│   ├── auth_utils.py        # Authentication & SQLite utilities
│   └── users.db             # User storage
├── frontend/
│   ├── app.py               # Main Entrypoint & Authentication UI
│   ├── components.py        # Reusable UI components & assets loader
│   ├── assets/              # App images & background media
│   └── pages/
│       ├── 0_Home.py        # Dashboard & overview
│       ├── 1_Diagnosis.py   # AI Image Analyzer, Chatbot, & Doctor Match
│       ├── 2_About_Us.py    # Project architecture & team details
│       └── 3_Contact.py     # Feedback & support
├── requirements.txt         # Project dependencies
├── train_model.py           # Model training script
└── README.md                # Documentation
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/prashunthakre/skincare-ai.git
cd skincare-ai
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run frontend/app.py
```

Open your browser and navigate to `http://localhost:8501`.

---

## ☁️ Live Deployment

This project is optimized for deployment on **Streamlit Community Cloud**:

1. Fork or push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and create a new app.
4. Set parameters:
   - **Repository**: `your-username/skincare-ai`
   - **Branch**: `main`
   - **Main file path**: `frontend/app.py`
   - **Python Version**: `3.10` or `3.11`
5. Click **Deploy!**

---

## ⚠️ Disclaimer

*SkinCare AI is an educational and supportive AI diagnostic tool. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a certified dermatologist for clinical evaluation.*

---

## 👨‍💻 Author

**Prashun Thakre**  
*Full Stack Developer & AI/ML Engineer*  
- GitHub: [@prashunthakre](https://github.com/prashunthakre)
