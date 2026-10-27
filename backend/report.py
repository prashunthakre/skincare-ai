from fpdf import FPDF
import os
from datetime import datetime
from PIL import Image, ImageOps


def _prepare_square_pdf_image(src_path, out_path, size=(500, 500)):
    """
    Converts any portrait/landscape image into a clean square-cropped image
    so that FPDF renders it inside an exact 50x50 mm box without vertical overflow.
    """
    try:
        img = Image.open(src_path).convert("RGB")
        sq_img = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        sq_img.save(out_path, "JPEG", quality=92)
        return out_path
    except Exception:
        return src_path


def _clean_latin1(text, fallback="N/A"):
    """Ensures text is clean Latin-1 for FPDF without '????' artifacts."""
    if not text:
        return fallback
    raw = str(text).strip()
    # Keep printable ASCII/Latin-1 characters cleanly
    cleaned = raw.encode("latin-1", "ignore").decode("latin-1").strip()
    return cleaned if len(cleaned) >= 2 else fallback


def create_pdf_report(image_path, heatmap_path, results, info, doctors_list, location, p_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- HEADER SECTION ---
    pdf.set_fill_color(1, 87, 155)  # Deep Blue
    pdf.rect(0, 0, 210, 20, 'F')

    pdf.set_y(6)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(0, 10, txt="SkinCare AI Pro - Dermatological Assessment Report", ln=True, align='C')

    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # --- 1. PATIENT DETAILS SECTION ---
    pdf.set_font("Arial", size=12.5, style='B')
    pdf.set_text_color(1, 87, 155)
    pdf.cell(0, 7, txt="1. Patient Profile", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(38, 6.5, txt="Patient Name:", border=0)
    pdf.set_font("Arial", size=10)
    safe_pname = _clean_latin1(p_data.get('name', 'Patient'), fallback="Patient")
    pdf.cell(82, 6.5, txt=safe_pname, border=0)

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(30, 6.5, txt="Report Date:", border=0)
    pdf.set_font("Arial", size=10)
    pdf.cell(40, 6.5, txt=_clean_latin1(p_data.get('date', datetime.now().strftime("%Y-%m-%d"))), border=0)
    pdf.ln(6.5)

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(38, 6.5, txt="Age & Gender:", border=0)
    pdf.set_font("Arial", size=10)
    raw_gender = str(p_data.get('gender', 'N/A'))
    gender_map = {"पुरुष": "Male", "महिला": "Female", "अन्य": "Other"}
    safe_gender = _clean_latin1(gender_map.get(raw_gender, raw_gender), fallback="N/A")
    pdf.cell(82, 6.5, txt=f"{p_data.get('age', 'N/A')} Years | {safe_gender}", border=0)

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(30, 6.5, txt="Location:", border=0)
    pdf.set_font("Arial", size=10)
    pdf.cell(40, 6.5, txt=_clean_latin1(location, fallback="India")[:22], border=0)
    pdf.ln(9)

    # --- 2. MEDICAL CONTEXT SECTION ---
    pdf.set_font("Arial", size=12.5, style='B')
    pdf.set_text_color(1, 87, 155)
    pdf.cell(0, 7, txt="2. Medical Context & Symptoms", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    y_start = pdf.get_y()
    pdf.set_fill_color(240, 245, 250)
    pdf.rect(10, y_start, 190, 22, 'F')

    pdf.set_y(y_start + 2)
    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(48, 6, txt=" Duration of Symptoms:", border=0)
    pdf.set_font("Arial", size=10)
    pdf.cell(140, 6, txt=_clean_latin1(p_data.get('duration', 'Few days'), fallback="Few days"), border=0)
    pdf.ln(6)

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(48, 6, txt=" Primary Symptoms:", border=0)
    pdf.set_font("Arial", size=10)
    pdf.cell(140, 6, txt=_clean_latin1(p_data.get('symptoms', 'None reported'), fallback="Reported in clinic")[:85], border=0)
    pdf.ln(6)

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(48, 6, txt=" Pre-existing Conditions:", border=0)
    pdf.set_font("Arial", size=10)
    pdf.cell(140, 6, txt=_clean_latin1(p_data.get('pre_existing', 'None'), fallback="None")[:85], border=0)
    pdf.ln(10)

    # --- 3. AI DIAGNOSTIC ANALYSIS SECTION ---
    pdf.set_font("Arial", size=12.5, style='B')
    pdf.set_text_color(1, 87, 155)
    pdf.cell(0, 7, txt="3. AI Diagnostic Analysis", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    y = pdf.get_y()
    os.makedirs("temp", exist_ok=True)

    # Strict 48x48mm square images so portrait mobile photos never overflow vertically
    if image_path and os.path.exists(image_path):
        sq_upl = _prepare_square_pdf_image(image_path, "temp/pdf_sq_upl.jpg")
        pdf.image(sq_upl, x=15, y=y + 2, w=48, h=48)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(15, y + 2, 48, 48)
        pdf.set_font("Arial", size=8.5, style='I')
        pdf.text(27, y + 54.5, "Original Upload")

    if heatmap_path and os.path.exists(heatmap_path):
        sq_heat = _prepare_square_pdf_image(heatmap_path, "temp/pdf_sq_heat.jpg")
        pdf.image(sq_heat, x=73, y=y + 2, w=48, h=48)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(73, y + 2, 48, 48)
        pdf.set_font("Arial", size=8.5, style='I')
        pdf.text(81, y + 54.5, "AI Focus (Grad-CAM)")

    # Results Box (exact height = 48mm matching the two square images)
    if info.get('severity') in ['High', 'Moderate']:
        pdf.set_fill_color(255, 243, 224)
    else:
        pdf.set_fill_color(232, 245, 233)
    pdf.rect(130, y + 2, 70, 48, 'F')

    ax = 133
    ay = y + 8.5

    # Prefer English PDF-safe fields so Hindi mode never prints '????'
    raw_det_name = info.get('pdf_name') or info.get('disease_key') or info.get('name', 'Skin Condition')
    safe_name = _clean_latin1(raw_det_name, fallback="Skin Condition")
    safe_severity = _clean_latin1(info.get('severity', 'Moderate'), fallback="Moderate")

    pdf.set_font("Arial", size=9.5, style='B')
    pdf.text(ax, ay, "Primary Detection:")
    pdf.set_font("Arial", size=10, style='B')
    pdf.set_text_color(183, 28, 28)

    if len(safe_name) > 26:
        pdf.text(ax, ay + 5, safe_name[:26])
        pdf.text(ax, ay + 9.5, safe_name[26:52])
        ay_offset = 4.5
    else:
        pdf.text(ax, ay + 5, safe_name)
        ay_offset = 0

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9.5, style='B')
    pdf.text(ax, ay + 13.5 + ay_offset, "Confidence Score:")
    pdf.set_font("Arial", size=10)
    top_conf = results[0]['confidence'] if results else 85.0
    pdf.text(ax, ay + 18.5 + ay_offset, f"{top_conf:.1f}%")

    pdf.set_font("Arial", size=9.5, style='B')
    pdf.text(ax, ay + 26.5 + ay_offset, "Severity Level:")
    pdf.set_font("Arial", size=10)
    pdf.text(ax, ay + 31.5 + ay_offset, safe_severity)

    # Move cursor cleanly below the 48mm images and their captions
    pdf.set_y(y + 60)

    # --- CLINICAL SUMMARY ---
    raw_desc = info.get('pdf_description') or info.get('description', '')
    desc_text = _clean_latin1(raw_desc, fallback="")
    if desc_text:
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.set_x(10)
        pdf.cell(0, 6, txt="Clinical Assessment Summary:", ln=True)
        pdf.set_font("Arial", size=9.5)
        pdf.set_x(10)
        pdf.multi_cell(0, 4.8, txt=desc_text)
        pdf.ln(2.5)

    # --- RECOMMENDED PRECAUTIONS ---
    pdf.set_font("Arial", size=10.5, style='B')
    pdf.set_x(10)
    pdf.cell(0, 6, txt="Recommended Precautions:", ln=True)
    pdf.set_font("Arial", size=9.5)

    prec_list = info.get('pdf_precautions') or info.get('precautions', [])
    for prec in prec_list:
        safe_prec = _clean_latin1(prec, fallback="")
        if safe_prec:
            pdf.set_x(10)
            pdf.multi_cell(0, 4.8, txt=f"- {safe_prec}")

    # --- NEARBY RECOMMENDED DERMATOLOGISTS (Up to 2) ---
    if doctors_list and len(doctors_list) > 0 and pdf.get_y() < 228:
        pdf.ln(2.5)
        pdf.set_font("Arial", size=10.5, style='B')
        pdf.set_text_color(1, 87, 155)
        pdf.set_x(10)
        pdf.cell(0, 6, txt="4. Recommended Nearby Dermatologists / Clinics:", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=9)
        for doc in doctors_list[:2]:
            d_name = _clean_latin1(doc.get('name', 'Dermatology Clinic'))
            d_addr = _clean_latin1(doc.get('address', location))[:75]
            d_dist = _clean_latin1(doc.get('distance', ''))
            dist_tag = f" ({d_dist})" if d_dist else ""
            pdf.set_x(10)
            pdf.multi_cell(0, 4.5, txt=f"* {d_name}{dist_tag} - {d_addr}")

    # --- DISCLAIMER & SIGNATURE FOOTER ---
    if pdf.get_y() > 245:
        pdf.add_page()

    pdf.set_y(-38)
    pdf.set_x(10)
    pdf.set_font("Arial", size=8, style='I')
    pdf.set_text_color(100, 100, 100)
    disclaimer = (
        "DISCLAIMER: This report is generated by an Artificial Intelligence system intended for preliminary screening only. "
        "It does NOT constitute a definitive medical diagnosis. Please consult a qualified dermatologist or healthcare provider "
        "before making any medical decisions."
    )
    pdf.multi_cell(0, 4.2, txt=disclaimer)

    pdf.set_y(-20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10, style='B')
    pdf.text(15, pdf.get_y(), "Signature / Stamp:")
    pdf.line(50, pdf.get_y(), 120, pdf.get_y())

    pdf.text(140, pdf.get_y(), "Report Generated:")
    pdf.set_font("Arial", size=9.5, style='')
    pdf.text(175, pdf.get_y(), datetime.now().strftime("%Y-%m-%d"))

    out_path = "medical_report.pdf"
    pdf.output(out_path)
    return out_path
