import os
import json
from PIL import Image
from google import genai


class MultimodalVisionEngine:
    """
    Global All-Rounder Multimodal Dermatology AI Engine powered by Google Gemini Vision.
    Includes:
    1. Non-Skin Image Guard (detects if user uploads a non-skin object like laptop/car/wall).
    2. Complete Fitzpatrick 17k (114+ diseases) & global dermatology diagnosis across Skin Types I-VI.
    3. Dual-language support with English PDF-safe fields so PDF reports never print '????' in Hindi mode.
    """
    def __init__(self, api_key=None):
        self.api_key = (api_key or os.environ.get("GEMINI_API_KEY", "")).strip()
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    def is_available(self):
        return self.client is not None and len(self.api_key) > 5

    def analyze_lesion(self, image: Image.Image, patient_data: dict, lang: str = 'en'):
        if not self.is_available():
            return None, "Gemini API key is not configured or invalid."

        rgb_img = image.convert("RGB")

        lang_instruction = (
            "Provide `condition_name` (Hindi name with English medical name in parentheses), `clinical_summary`, and `precautions` in Hindi (Devanagari script). Also ALWAYS provide `condition_name_en`, `clinical_summary_en`, and `precautions_en` in English for PDF generation."
            if lang == 'hi'
            else "Provide all text fields in clear clinical English."
        )

        prompt = f"""You are a world-renowned, board-certified global dermatologist and skin pathology expert with expertise across all Fitzpatrick Skin Types (Type I Very Fair to Type VI Deeply Pigmented/Dark Skin) and all geographic regions (South Asian/Indian, African, East Asian, Middle Eastern, European, Latin American).

Analyze this uploaded image carefully.

Patient Clinical Context:
- Age: {patient_data.get('age', 'Unknown')}
- Gender: {patient_data.get('gender', 'Unknown')}
- Lesion Duration: {patient_data.get('duration', 'Unknown')}
- Reported Symptoms: {patient_data.get('symptoms', 'None')}
- Medical History / Notes: {patient_data.get('pre_existing', 'None')}

CRITICAL STEP 1 (Non-Skin / Invalid Image Guard):
- First check if the image actually shows human skin, face, hair/scalp, nails, or mucosa.
- If the image is a random object (e.g., laptop, car, room, flower, animal, document, cartoon, blank screen) with NO human skin/body part visible, set `"is_valid_skin": false` and set `condition_name` to `"Invalid Image (No Human Skin Detected)"` (or Hindi equivalent if Hindi requested), `confidence` to `0.0`, `severity` to `"Low"`, and instruct the user to upload a clear close-up photo of the skin area.
- If human skin is visible and looks completely healthy/normal with no lesion, rash, pimple, or abnormality, set `"is_valid_skin": true`, `condition_name` to `"Healthy / Normal Skin"`, `severity` to `"Low"`.

CRITICAL STEP 2 (All-Rounder Global Dermatology Diagnosis):
- Do NOT restrict yourself to only 10 classes. Identify the EXACT dermatological condition from the complete global dermatology & Fitzpatrick 17k (114+ conditions) spectrum (e.g., Acne Vulgaris, Furuncle/Boil, Folliculitis, Eczema, Atopic Dermatitis, Allergic Contact Dermatitis, Seborrheic Dermatitis, Perioral Dermatitis, Psoriasis, Lichen Planus, Pityriasis Rosea, Urticaria/Hives, Rosacea, Tinea/Ringworm, Candidiasis, Paronychia, Impetigo, Cellulitis, Viral Warts, Molluscum Contagiosum, Herpes Simplex/Zoster, Scabies, Vitiligo, Melasma, Post-Inflammatory Hyperpigmentation, Acanthosis Nigricans, Alopecia Areata, Lupus Erythematosus, Melanocytic Nevus, Seborrheic Keratosis, Dermatofibroma, Keloid, Epidermoid Cyst, Actinic Keratosis, Basal Cell Carcinoma, Squamous Cell Carcinoma, Malignant Melanoma, etc.).
- Account for how erythema, inflammation, and pigment changes appear on the patient's specific skin tone (Fitzpatrick I to VI).

Language Requirement:
{lang_instruction}

Respond ONLY with a valid JSON object strictly matching this schema (no markdown fences, no extra text):
{{
  "is_valid_skin": true,
  "condition_name": "Exact Name of Identified Skin Disease/Condition (in requested language)",
  "condition_name_en": "Exact Name of Identified Skin Disease/Condition in English",
  "fitzpatrick_type": "Estimated Fitzpatrick Skin Type (e.g. Type IV Medium/Indian Skin)",
  "confidence": 92.0,
  "severity": "Low" | "Moderate" | "High",
  "risk_level": "Benign / Low Risk" | "Moderate Risk - Dermatologist Visit Advised" | "High Risk - Urgent Evaluation Required",
  "clinical_summary": "2-3 sentences detailing visual morphology, estimated Fitzpatrick skin tone, and clinical reasoning (in requested language).",
  "clinical_summary_en": "2-3 sentences detailing visual morphology, estimated Fitzpatrick skin tone, and clinical reasoning in English.",
  "precautions": ["Actionable precaution 1", "Actionable precaution 2", "Actionable precaution 3"],
  "precautions_en": ["Actionable precaution 1 in English", "Actionable precaution 2 in English", "Actionable precaution 3 in English"],
  "differentials": [
    {{"class": "Primary Condition Name in English", "confidence": 92.0}},
    {{"class": "Second Differential Condition in English", "confidence": 5.5}},
    {{"class": "Third Differential Condition in English", "confidence": 2.5}}
  ]
}}"""

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[rgb_img, prompt]
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            data = json.loads(raw_text)

            cond_en = data.get("condition_name_en") or data.get("condition_name", "Skin Condition")
            cond_disp = data.get("condition_name", cond_en)
            conf_val = float(data.get("confidence", 85.0))

            results = data.get("differentials", [
                {"class": cond_en, "confidence": conf_val}
            ])

            fitz_str = data.get("fitzpatrick_type", "")
            summary_disp = data.get("clinical_summary", "")
            summary_en = data.get("clinical_summary_en") or summary_disp
            if fitz_str and fitz_str not in summary_disp:
                summary_disp = f"[{fitz_str}] {summary_disp}"
            if fitz_str and fitz_str not in summary_en:
                summary_en = f"[{fitz_str}] {summary_en}"

            prec_disp = data.get("precautions", [
                "Keep the area clean and dry.",
                "Avoid picking or scratching.",
                "Consult a board-certified dermatologist."
            ])
            prec_en = data.get("precautions_en") or prec_disp

            info = {
                "name": cond_disp,
                "disease_key": cond_en,
                "severity": data.get("severity", "Low"),
                "risk_level": data.get("risk_level", "Benign"),
                "description": summary_disp,
                "precautions": prec_disp,
                "pdf_name": cond_en,
                "pdf_description": summary_en,
                "pdf_precautions": prec_en,
                "is_valid_skin": bool(data.get("is_valid_skin", True))
            }

            return {
                "results": results,
                "info": info,
                "top_pred_class": cond_disp,
                "top_confidence": conf_val,
                "engine_used": "Multimodal Vision AI + Fitzpatrick 17k All-Rounder"
            }, None
        except Exception as e:
            return None, str(e)
