from fpdf import FPDF
import os
from datetime import datetime

def create_pdf_report(image_path, heatmap_path, results, info, doctors_list, location, p_data):
    pdf = FPDF()
    pdf.add_page()
    
    # --- HEADER SECTION ---
    # Add a logo placeholder or a premium header line
    pdf.set_fill_color(1, 87, 155) # Deep Blue
    pdf.rect(0, 0, 210, 20, 'F')
    
    pdf.set_y(6)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(0, 10, txt="SkinCare AI Pro - Dermatological Assessment Report", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0) # Reset to black
    pdf.ln(15)
    
    # --- PATIENT DETAILS SECTION ---
    pdf.set_font("Arial", size=14, style='B')
    pdf.set_text_color(1, 87, 155)
    pdf.cell(0, 10, txt="1. Patient Profile", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11, style='B')
    pdf.cell(40, 8, txt="Patient Name:", border=0)
    pdf.set_font("Arial", size=11)
    pdf.cell(80, 8, txt=p_data.get('name', 'N/A'), border=0)
    
    pdf.set_font("Arial", size=11, style='B')
    pdf.cell(30, 8, txt="Report Date:", border=0)
    pdf.set_font("Arial", size=11)
    pdf.cell(40, 8, txt=p_data.get('date', 'N/A'), border=0)
    pdf.ln(8)
    
    pdf.set_font("Arial", size=11, style='B')
    pdf.cell(40, 8, txt="Age & Gender:", border=0)
    pdf.set_font("Arial", size=11)
    pdf.cell(80, 8, txt=f"{p_data.get('age', 'N/A')} Years | {p_data.get('gender', 'N/A')}", border=0)
    pdf.ln(12)
    
    # --- MEDICAL CONTEXT SECTION ---
    pdf.set_font("Arial", size=14, style='B')
    pdf.set_text_color(1, 87, 155)
    pdf.cell(0, 10, txt="2. Medical Context & Symptoms", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Draw a subtle background box for context
    y_start = pdf.get_y()
    pdf.set_fill_color(240, 245, 250) # Light blueish gray
    pdf.rect(10, y_start, 190, 30, 'F')
    
    pdf.set_y(y_start + 3)
    pdf.set_font("Arial", size=11, style='B')
    pdf.cell(50, 8, txt=" Duration of Symptoms:", border=0)
    pdf.set_font("Arial", size=11)
    pdf.cell(140, 8, txt=p_data.get('duration', 'N/A'), border=0)
    pdf.ln(8)
    
    pdf.set_font("Arial", size=11, style='B')
    pdf.cell(50, 8, txt=" Primary Symptoms:", border=0)
    pdf.set_font("Arial", size=11)
    safe_symp = p_data.get('symptoms', 'None').encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(140, 8, txt=safe_symp, border=0)
    pdf.ln(8)
    
    pdf.set_font("Arial", size=11, style='B')
    pdf.cell(50, 8, txt=" Pre-existing Conditions:", border=0)
    pdf.set_font("Arial", size=11)
    safe_pre = p_data.get('pre_existing', 'None').encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(140, 8, txt=safe_pre, border=0)
    pdf.ln(15)
    
    # --- AI ANALYSIS SECTION ---
    pdf.set_font("Arial", size=14, style='B')
    pdf.set_text_color(1, 87, 155)
    pdf.cell(0, 10, txt="3. AI Diagnostic Analysis", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    y = pdf.get_y()
    # Insert Images
    if os.path.exists(image_path):
        pdf.image(image_path, x=15, y=y+2, w=50)
        pdf.set_font("Arial", size=9, style='I')
        pdf.text(25, y+57, "Original Upload")
        
    if heatmap_path and os.path.exists(heatmap_path):
        pdf.image(heatmap_path, x=75, y=y+2, w=50)
        pdf.set_font("Arial", size=9, style='I')
        pdf.text(82, y+57, "AI Focus (Grad-CAM)")
    
    # Results Box
    pdf.set_fill_color(255, 243, 224) if info['severity'] in ['High', 'Moderate'] else pdf.set_fill_color(232, 245, 233)
    pdf.rect(135, y+2, 65, 50, 'F')
    
    ax = 138
    ay = y + 10
    
    safe_name = info['name'].encode('latin-1', 'replace').decode('latin-1')
    safe_severity = info['severity'].encode('latin-1', 'replace').decode('latin-1')
    safe_risk = info['risk_level'].encode('latin-1', 'replace').decode('latin-1')
    
    pdf.set_font("Arial", size=10, style='B')
    pdf.text(ax, ay, "Primary Detection:")
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(183, 28, 28) # Dark Red
    
    # Handle long names wrapping
    if len(safe_name) > 25:
        pdf.text(ax, ay + 6, safe_name[:25])
        pdf.text(ax, ay + 11, safe_name[25:50])
        ay += 5
    else:
        pdf.text(ax, ay + 6, safe_name)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10, style='B')
    pdf.text(ax, ay + 16, "Confidence Score:")
    pdf.set_font("Arial", size=11)
    pdf.text(ax, ay + 22, f"{results[0]['confidence']:.1f}%")
    
    pdf.set_font("Arial", size=10, style='B')
    pdf.text(ax, ay + 32, "Severity Level:")
    pdf.set_font("Arial", size=11)
    pdf.text(ax, ay + 38, safe_severity)
    
    pdf.set_y(y + 65)
    
    # --- PRECAUTIONS ---
    pdf.set_font("Arial", size=12, style='B')
    pdf.set_x(10)
    pdf.cell(0, 8, txt="Recommended Precautions:", ln=True)
    pdf.set_font("Arial", size=10)
    
    for prec in info.get('precautions', []):
        safe_prec = prec.encode('latin-1', 'replace').decode('latin-1')
        pdf.set_x(10)
        pdf.multi_cell(0, 6, txt=f"- {safe_prec}")
    
    pdf.ln(10)
    
    # --- DISCLAIMER & SIGNATURE ---
    pdf.set_y(-50)
    pdf.set_x(10)
    pdf.set_font("Arial", size=9, style='I')
    pdf.set_text_color(100, 100, 100)
    disclaimer = "DISCLAIMER: This report is generated by an Artificial Intelligence system intended for preliminary screening only. It does NOT constitute a definitive medical diagnosis. Please consult a qualified dermatologist or healthcare provider before making any medical decisions."
    pdf.multi_cell(0, 5, txt=disclaimer)
    
    pdf.set_y(-30)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=11, style='B')
    pdf.text(15, pdf.get_y(), "Signature / Stamp:")
    pdf.line(50, pdf.get_y(), 120, pdf.get_y())
    
    pdf.text(140, pdf.get_y(), "Report Generated:")
    pdf.set_font("Arial", size=10, style='')
    pdf.text(175, pdf.get_y(), datetime.now().strftime("%Y-%m-%d"))
    
    out_path = "medical_report.pdf"
    pdf.output(out_path)
    return out_path
