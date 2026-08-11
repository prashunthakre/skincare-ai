from report import create_pdf_report

results = [{"class": "Eczema", "confidence": 95.5}]
info = {
    'name': 'Eczema (एक्जिमा)',
    'severity': 'Moderate',
    'risk_level': 'Medium Risk',
    'precautions': ['Moisturize', 'Avoid triggers']
}
p_data = {
    "name": "Prashun",
    "age": "25",
    "gender": "Male",
    "duration": "Few days",
    "symptoms": "Itching",
    "pre_existing": "None",
    "date": "2026-04-26"
}

try:
    print("Calling create_pdf_report")
    create_pdf_report("dummy.jpg", "dummy.jpg", results, info, [], "Mumbai", p_data)
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
