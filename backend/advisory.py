class SkinAdvisoryEngine:
    def __init__(self):
        # Disease knowledge base mapped to new 10 classes
        self.knowledge_base = {
            'Eczema': {
                'en': {'name': 'Eczema', 'severity_base': 'Moderate', 'description': 'A condition that makes your skin red and itchy. It is common in children but can occur at any age.', 'precautions': ['Moisturize your skin regularly.', 'Identify and avoid triggers.', 'Take shorter showers or baths.']},
                'hi': {'name': 'एक्जिमा (Eczema)', 'severity_base': 'Moderate', 'description': 'यह एक ऐसी स्थिति है जिसमें त्वचा लाल हो जाती है और खुजली होती है।', 'precautions': ['त्वचा को नियमित रूप से मॉइस्चराइज़ करें।', 'ट्रिगर्स को पहचानें और उनसे बचें।', 'कम समय के लिए नहाएं।']}
            },
            'Melanoma': {
                'en': {'name': 'Melanoma', 'severity_base': 'High', 'description': 'The most serious type of skin cancer, developing in the melanocytes. High risk of spreading if untreated.', 'precautions': ['URGENT: Immediate consultation with an oncologist or dermatologist required.', 'Do not delay medical evaluation.', 'Track any changes in ABCD (Asymmetry, Border, Color, Diameter).']},
                'hi': {'name': 'मेलेनोमा (Melanoma)', 'severity_base': 'High', 'description': 'यह सबसे खतरनाक किस्म का स्किन कैंसर है।', 'precautions': ['URGENT: तुरंत कैंसर विशेषज्ञ से मिलें।', 'डॉक्टर के पास जाने में देरी न करें।']}
            },
            'Atopic Dermatitis': {
                'en': {'name': 'Atopic Dermatitis', 'severity_base': 'Moderate', 'description': 'A common type of eczema that typically starts in childhood, causing dry, itchy skin.', 'precautions': ['Use mild soaps and moisturize often.', 'Avoid scratching the affected areas.']},
                'hi': {'name': 'एटोपिक डर्मेटाइटिस', 'severity_base': 'Moderate', 'description': 'यह एक प्रकार का एक्जिमा है जो बचपन में शुरू होता है और त्वचा को सूखा और खुजलीदार बनाता है।', 'precautions': ['हल्के साबुन का प्रयोग करें और बार-बार मॉइस्चराइज़ करें।', 'प्रभावित क्षेत्रों को खुजलाने से बचें।']}
            },
            'Basal Cell Carcinoma': {
                'en': {'name': 'Basal Cell Carcinoma', 'severity_base': 'High', 'description': 'A type of skin cancer that begins in the basal cells. It usually appears as a slightly transparent bump on the skin.', 'precautions': ['URGENT: Schedule a biopsy/consultation with a dermatologist.', 'Protect the area from further UV exposure.']},
                'hi': {'name': 'बेसल सेल कार्सिनोमा', 'severity_base': 'High', 'description': 'यह एक प्रकार का त्वचा कैंसर है जो बेसल कोशिकाओं में शुरू होता है।', 'precautions': ['URGENT: तुरंत डॉक्टर से मिलें।', 'धूप से बचाव करें।']}
            },
            'Melanocytic Nevi': {
                'en': {'name': 'Melanocytic Nevi (Normal Mole)', 'severity_base': 'Low', 'description': 'A common mole. Usually harmless, but should be monitored for malignant transformation.', 'precautions': ['Regularly check for changes in size, shape, or color.', 'Use sunscreen when exposed to the sun.']},
                'hi': {'name': 'सामान्य तिल (Melanocytic Nevi)', 'severity_base': 'Low', 'description': 'यह एक सामान्य तिल है, जो आमतौर पर सुरक्षित होता है।', 'precautions': ['आकार, रंग में बदलाव की जाँच करें।', 'धूप में निकलने से पहले सनस्क्रीन का प्रयोग करें।']}
            },
            'Benign Keratosis': {
                'en': {'name': 'Benign Keratosis', 'severity_base': 'Low', 'description': 'A non-cancerous skin growth that can appear scaly, waxy, or slightly elevated. Common with age.', 'precautions': ['Generally harmless, but monitor for changes.', 'Keep the skin moisturized.']},
                'hi': {'name': 'बिनाइन केराटोसिस', 'severity_base': 'Low', 'description': 'यह एक गैर-कैंसरयुक्त त्वचा की वृद्धि है जो उम्र के साथ आम है।', 'precautions': ['आमतौर पर सुरक्षित, लेकिन बदलाव पर ध्यान दें।', 'त्वचा को मॉइस्चराइज रखें।']}
            },
            'Psoriasis / Lichen Planus': {
                'en': {'name': 'Psoriasis / Lichen Planus', 'severity_base': 'Moderate', 'description': 'Skin disorders characterized by scaly or itchy patches. Often caused by an overactive immune system.', 'precautions': ['Avoid skin trauma and stress.', 'Apply prescribed topical treatments.']},
                'hi': {'name': 'सोरायसिस / लाइकेन प्लानस', 'severity_base': 'Moderate', 'description': 'पपड़ीदार या खुजली वाले पैच की विशेषता वाले त्वचा विकार।', 'precautions': ['तनाव और त्वचा की चोट से बचें।', 'डॉक्टर द्वारा दी गई क्रीम का उपयोग करें।']}
            },
            'Seborrheic Keratoses': {
                'en': {'name': 'Seborrheic Keratoses', 'severity_base': 'Low', 'description': 'One of the most common noncancerous skin growths in older adults.', 'precautions': ['No treatment necessary unless irritated.', 'Do not try to scratch them off.']},
                'hi': {'name': 'सेबोरहाइक केराटोसिस', 'severity_base': 'Low', 'description': 'वृद्ध वयस्कों में सबसे आम गैर-कैंसरयुक्त त्वचा वृद्धि में से एक है।', 'precautions': ['जब तक खुजली न हो, इलाज की कोई आवश्यकता नहीं है।', 'इन्हें खुरचने की कोशिश न करें।']}
            },
            'Fungal Infections (Tinea)': {
                'en': {'name': 'Fungal Infection (Tinea / Ringworm)', 'severity_base': 'Moderate', 'description': 'Common fungal skin infections that cause a red, itchy, circular rash.', 'precautions': ['Keep the area clean and dry.', 'Use over-the-counter or prescribed antifungal creams.']},
                'hi': {'name': 'फंगल इन्फेक्शन (दाद / Tinea)', 'severity_base': 'Moderate', 'description': 'सामान्य फंगल संक्रमण जो लाल, खुजलीदार, गोलाकार चकत्ते पैदा करता है।', 'precautions': ['प्रभावित क्षेत्र को साफ और सूखा रखें।', 'एंटीफंगल क्रीम का उपयोग करें।']}
            },
            'Viral Infections (Warts)': {
                'en': {'name': 'Viral Infection (Warts / Molluscum)', 'severity_base': 'Low', 'description': 'Common viral skin infections causing small, raised bumps.', 'precautions': ['Avoid scratching or picking at the bumps.', 'Consult a doctor for removal options.']},
                'hi': {'name': 'वायरल इन्फेक्शन (मस्से)', 'severity_base': 'Low', 'description': 'सामान्य वायरल संक्रमण जिससे छोटे, उभरे हुए दाने हो जाते हैं।', 'precautions': ['दानों को खुरचने से बचें।', 'इलाज के लिए डॉक्टर से मिलें।']}
            },
            'Unknown': {
                'en': {'name': 'Unknown / Unrecognized', 'severity_base': 'Unknown', 'description': 'The model could not confidently identify the condition.', 'precautions': ['Consult a dermatologist for a professional diagnosis.']},
                'hi': {'name': 'अज्ञात / पहचान नहीं हो पाई', 'severity_base': 'Unknown', 'description': 'माफ़ करें, एआई मॉडल इस बीमारी की पहचान नहीं कर पा रहा है।', 'precautions': ['डॉक्टर से संपर्क करें।']}
            }
        }

    def analyze(self, class_name, confidence, lang='en'):
        """
        Returns a dictionary containing severity, description, and precautions
        in the specified language ('en' or 'hi').
        """
        if class_name not in self.knowledge_base:
            class_name = 'Unknown'
            
        info = self.knowledge_base[class_name][lang]
        base_severity = info['severity_base']
        
        # Risk Engine Logic & Formatting translated dynamically
        if base_severity == 'High':
            risk_level = 'Urgent Consultation Recommended' if lang == 'en' else 'तत्काल डॉक्टर से मिलें (Urgent Consultation Recommended)'
            final_severity = 'High'
        elif base_severity == 'Moderate':
            if confidence > 80:
                final_severity = 'Moderate'
                risk_level = 'Medium Risk - Medical evaluation advised' if lang == 'en' else 'मध्यम जोखिम - डॉक्टर को दिखाना ठीक रहेगा (Medium Risk - Medical evaluation advised)'
            else:
                final_severity = 'Moderate-Low'
                risk_level = 'Low to Medium Risk - Monitor the area' if lang == 'en' else 'कम जोखिम - इस पर निगरानी रखें (Low Risk - Monitor the area)'
        elif base_severity == 'Unknown':
             final_severity = 'Unknown'
             risk_level = 'Unknown Risk - Consult Doctor' if lang == 'en' else 'अज्ञात - डॉक्टर से परामर्श लें (Unknown Risk - Consult Doctor)'
        else:
            final_severity = 'Low'
            risk_level = 'Low Risk - Routine monitoring recommended' if lang == 'en' else 'कम जोखिम - घबराने की बात नहीं, बस ध्यान रखें (Low Risk - Routine monitoring)'

        return {
            'disease_key': class_name,
            'name': info['name'],
            'description': info['description'],
            'severity': final_severity,
            'risk_level': risk_level,
            'precautions': info['precautions']
        }
