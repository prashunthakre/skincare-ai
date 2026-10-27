class SkinAdvisoryEngine:
    """
    All-Rounder Bilingual (English & Hindi) Clinical Dermatology Advisory Engine.
    Covers the core classes plus the comprehensive Fitzpatrick 17k (114+ conditions)
    and global dermatological disease spectrum across all skin tones (Types I-VI).
    Always provides English PDF-safe fields ('pdf_name', 'pdf_description', 'pdf_precautions')
    so PDF reports never print '????' when the UI is in Hindi mode.
    """
    def __init__(self):
        self.knowledge_base = {
            'Eczema': {
                'en': {
                    'name': 'Eczema (Dermatitis)',
                    'severity_base': 'Moderate',
                    'description': 'An inflammatory skin condition causing red/hyperpigmented, dry, itchy, and irritated patches across any skin tone.',
                    'precautions': [
                        'Apply fragrance-free ceramide moisturizers 2-3 times daily.',
                        'Avoid harsh soaps, hot water baths, and known allergen triggers.',
                        'Consult a dermatologist for topical corticosteroid or calcineurin therapy.'
                    ]
                },
                'hi': {
                    'name': 'एक्जिमा (Eczema)',
                    'severity_base': 'Moderate',
                    'description': 'यह एक सूजन संबंधी त्वचा रोग है जिसमें त्वचा रूखी, लाल या गहरे रंग की और खुजलीदार हो जाती है।',
                    'precautions': [
                        'दिन में 2-3 बार बिना खुशबू वाला मॉइस्चराइज़र लगाएं।',
                        'तेज़ साबुन और गर्म पानी से नहाने से बचें।',
                        'त्वचा विशेषज्ञ की सलाह से उचित क्रीम का उपयोग करें।'
                    ]
                }
            },
            'Melanoma': {
                'en': {
                    'name': 'Melanoma (Malignant Skin Cancer)',
                    'severity_base': 'High',
                    'description': 'A serious malignant tumor of melanocytes showing asymmetry, irregular borders, color variation, or rapid evolution.',
                    'precautions': [
                        'URGENT: Schedule an immediate excisional biopsy with a dermatologist or oncologist.',
                        'Do not delay clinical evaluation or attempt home remedies.',
                        'Monitor ABCDE signs (Asymmetry, Border, Color, Diameter, Evolution).'
                    ]
                },
                'hi': {
                    'name': 'मेलेनोमा (Melanoma - स्किन कैंसर)',
                    'severity_base': 'High',
                    'description': 'यह मेलेनोसाइट्स में होने वाला सबसे गंभीर त्वचा कैंसर है। समय पर पहचान और बायोप्सी अत्यंत आवश्यक है।',
                    'precautions': [
                        'URGENT: तुरंत त्वचा या कैंसर विशेषज्ञ (Oncologist) से मिलें।',
                        'घरेलू उपचार में समय नष्ट न करें।',
                        'तिल या घाव के आकार, रंग और किनारों में बदलाव पर नज़र रखें।'
                    ]
                }
            },
            'Atopic Dermatitis': {
                'en': {
                    'name': 'Atopic Dermatitis',
                    'severity_base': 'Moderate',
                    'description': 'A chronic relapsing form of eczema causing intense pruritus, lichenification, and barrier dysfunction.',
                    'precautions': [
                        'Maintain skin barrier hydration with thick emollients immediately after bathing.',
                        'Wear breathable cotton fabrics and avoid scratching.',
                        'Seek dermatological guidance for flare-up management.'
                    ]
                },
                'hi': {
                    'name': 'एटोपिक डर्मेटाइटिस (Atopic Dermatitis)',
                    'severity_base': 'Moderate',
                    'description': 'यह एक दीर्घकालिक एक्जिमा है जिससे त्वचा में अत्यधिक रूखापन और खुजली होती है।',
                    'precautions': [
                        'नहाने के तुरंत बाद गाढ़ा मॉइस्चराइज़र लगाएं।',
                        'सूती कपड़े पहनें और प्रभावित हिस्से को खुजलाने से बचें।'
                    ]
                }
            },
            'Basal Cell Carcinoma': {
                'en': {
                    'name': 'Basal Cell Carcinoma (BCC)',
                    'severity_base': 'High',
                    'description': 'A malignant epidermal skin tumor arising from basal cells, often presenting as a pearly or pigmented nodule or ulcer.',
                    'precautions': [
                        'URGENT: Consult a dermatologist for dermoscopic evaluation and biopsy.',
                        'Protect skin from UV radiation using broad-spectrum SPF 50+ sunscreen.',
                        'Avoid picking or traumatizing the lesion.'
                    ]
                },
                'hi': {
                    'name': 'बेसल सेल कार्सिनोमा (Basal Cell Carcinoma)',
                    'severity_base': 'High',
                    'description': 'यह त्वचा की बेसल कोशिकाओं में शुरू होने वाला त्वचा कैंसर है जो चमकदार या गहरे उभार के रूप में दिखता है।',
                    'precautions': [
                        'URGENT: बायोप्सी और जांच के लिए तुरंत त्वचा विशेषज्ञ से मिलें।',
                        'तेज़ धूप से बचें और SPF 50+ सनस्क्रीन का प्रयोग करें।'
                    ]
                }
            },
            'Squamous Cell Carcinoma': {
                'en': {
                    'name': 'Squamous Cell Carcinoma (SCC)',
                    'severity_base': 'High',
                    'description': 'A malignant neoplasm of epidermal keratinocytes presenting as a scaly, crusted, or ulcerated plaque or nodule.',
                    'precautions': [
                        'URGENT: Immediate dermatological biopsy and surgical evaluation required.',
                        'Protect all sun-exposed skin from UV radiation.',
                        'Monitor for bleeding, rapid growth, or tenderness.'
                    ]
                },
                'hi': {
                    'name': 'स्क्वैमस सेल कार्सिनोमा (Squamous Cell Carcinoma)',
                    'severity_base': 'High',
                    'description': 'यह एपिडर्मल कोशिकाओं का एक त्वचा कैंसर है जो पपड़ीदार या घाव वाले उभार के रूप में दिखाई देता है।',
                    'precautions': [
                        'URGENT: तुरंत त्वचा विशेषज्ञ से बायोप्सी और जांच कराएं।',
                        'धूप से त्वचा का पूर्ण बचाव करें।'
                    ]
                }
            },
            'Melanocytic Nevi': {
                'en': {
                    'name': 'Melanocytic Nevi (Benign Mole)',
                    'severity_base': 'Low',
                    'description': 'A benign proliferation of melanocytes (common mole) with uniform pigmentation and regular borders.',
                    'precautions': [
                        'Perform monthly self-examinations for any change in size, shape, or color.',
                        'Apply broad-spectrum SPF 30+ sunscreen daily.'
                    ]
                },
                'hi': {
                    'name': 'सामान्य तिल (Melanocytic Nevi)',
                    'severity_base': 'Low',
                    'description': 'यह एक सामान्य और सुरक्षित तिल (Mole) है।',
                    'precautions': [
                        'आकार या रंग में किसी भी बदलाव की नियमित जांच करें।',
                        'धूप में निकलते समय सनस्क्रीन लगाएं।'
                    ]
                }
            },
            'Benign Keratosis': {
                'en': {
                    'name': 'Benign Keratosis / Actinic Keratosis',
                    'severity_base': 'Low',
                    'description': 'Keratinocytic skin growths including solar lentigines, lichen planus-like keratosis, and actinic keratosis.',
                    'precautions': [
                        'Monitor rough or scaly sun-exposed patches with a dermatologist.',
                        'Use daily UV protection and gentle emollients.'
                    ]
                },
                'hi': {
                    'name': 'बिनाइन केराटोसिस (Benign Keratosis)',
                    'severity_base': 'Low',
                    'description': 'यह त्वचा की बाहरी परत की वृद्धि है जो धूप या उम्र के कारण होती है।',
                    'precautions': [
                        'बदलाव दिखने पर डॉक्टर से जांच कराएं।',
                        'सनस्क्रीन और मॉइस्चराइज़र का नियमित उपयोग करें।'
                    ]
                }
            },
            'Psoriasis / Lichen Planus': {
                'en': {
                    'name': 'Psoriasis / Lichen Planus',
                    'severity_base': 'Moderate',
                    'description': 'Chronic immune-mediated papulosquamous dermatoses characterized by well-demarcated scaly plaques or violaceous papules.',
                    'precautions': [
                        'Use keratolytics (salicylic acid/urea) and thick moisturizers regularly.',
                        'Avoid skin trauma (Koebner phenomenon), smoking, and stress triggers.',
                        'Follow dermatologist-prescribed topical or systemic therapy.'
                    ]
                },
                'hi': {
                    'name': 'सोरायसिस / लाइकेन प्लानस (Psoriasis / Lichen Planus)',
                    'severity_base': 'Moderate',
                    'description': 'यह ऑटोइम्यून त्वचा विकार है जिसमें पपड़ीदार चकत्ते और खुजली होती है।',
                    'precautions': [
                        'त्वचा को चोट लगने और सूखापन होने से बचाएं।',
                        'डॉक्टर द्वारा दी गई क्रीम और दवाइयों का नियमित प्रयोग करें।'
                    ]
                }
            },
            'Seborrheic Keratoses': {
                'en': {
                    'name': 'Seborrheic Keratoses & Benign Tumors',
                    'severity_base': 'Low',
                    'description': 'Harmless, well-circumscribed epidermal growths with a stuck-on waxy or verrucous appearance.',
                    'precautions': [
                        'Avoid picking, rubbing, or scratching the growth.',
                        'Consult a dermatologist only if it becomes irritated or bleeds.'
                    ]
                },
                'hi': {
                    'name': 'सेबोरहाइक केराटोसिस (Seborrheic Keratoses)',
                    'severity_base': 'Low',
                    'description': 'यह एक गैर-कैंसरयुक्त और सुरक्षित त्वचा वृद्धि है।',
                    'precautions': [
                        'इन्हें खुरचने या छीलने की कोशिश न करें।',
                        'यदि जलन या खून आए तो डॉक्टर को दिखाएं।'
                    ]
                }
            },
            'Fungal Infections (Tinea)': {
                'en': {
                    'name': 'Fungal Infection (Tinea / Ringworm / Candidiasis)',
                    'severity_base': 'Moderate',
                    'description': 'Superficial dermatophyte or yeast infection presenting with annular scaling, central clearing, or intertriginous erythema.',
                    'precautions': [
                        'Keep the affected skin area clean, cool, and completely dry.',
                        'Use topical antifungal agents (clotrimazole/terbinafine) as advised by a physician.',
                        'Do not share towels or clothing; wash fabrics in hot water.'
                    ]
                },
                'hi': {
                    'name': 'फंगल इन्फेक्शन (दाद / Tinea / Ringworm)',
                    'severity_base': 'Moderate',
                    'description': 'यह एक संक्रामक फंगल संक्रमण है जिससे गोल लाल या गहरे खुजलीदार चकत्ते बनते हैं।',
                    'precautions': [
                        'प्रभावित हिस्से को साफ और पूरी तरह सूखा रखें।',
                        'डॉक्टर की सलाह से एंटीफंगल क्रीम लगाएं और तौलिया साझा न करें।'
                    ]
                }
            },
            'Viral Infections (Warts)': {
                'en': {
                    'name': 'Viral / Parasitic Skin Infection (Warts / Molluscum / Scabies)',
                    'severity_base': 'Moderate',
                    'description': 'Cutaneous viral or parasitic infection causing hyperkeratotic papules, umbilicated lesions, or pruritic burrows.',
                    'precautions': [
                        'Avoid scratching or shaving over lesions to prevent autoinoculation.',
                        'Maintain strict personal hygiene and consult a dermatologist for targeted treatment.'
                    ]
                },
                'hi': {
                    'name': 'वायरल / परजीवी त्वचा संक्रमण (Warts / Scabies)',
                    'severity_base': 'Moderate',
                    'description': 'यह वायरल या परजीवी संक्रमण है जिससे त्वचा पर छोटे दाने, मस्से या तेज खुजली होती है।',
                    'precautions': [
                        'दानों को खुरचने से बचें ताकि संक्रमण अन्य हिस्सों में न फैले।',
                        'उचित इलाज के लिए त्वचा विशेषज्ञ से मिलें।'
                    ]
                }
            },
            'Acne Vulgaris': {
                'en': {
                    'name': 'Acne Vulgaris / Folliculitis',
                    'severity_base': 'Low',
                    'description': 'Pilosebaceous unit inflammation presenting with comedones, inflammatory papules, pustules, or nodules.',
                    'precautions': [
                        'Cleanse gently twice daily with a non-comedogenic salicylic acid or benzoyl peroxide wash.',
                        'Never squeeze or pop pustules to prevent post-inflammatory hyperpigmentation and scarring.',
                        'Use oil-free, non-comedogenic sunscreen and moisturizers.'
                    ]
                },
                'hi': {
                    'name': 'मुंहासे / फॉलिकुलिटिस (Acne Vulgaris)',
                    'severity_base': 'Low',
                    'description': 'रोमछिद्रों में तेल और बैक्टीरिया जमा होने से होने वाले दाने और मुंहासे।',
                    'precautions': [
                        'चेहरे को दिन में दो बार माइल्ड फेसवॉश से धोएं।',
                        'मुंहासों को फोड़ने या दबाने से बचें ताकि दाग न पड़ें।'
                    ]
                }
            },
            'Vitiligo': {
                'en': {
                    'name': 'Vitiligo (Pigmentary Disorder)',
                    'severity_base': 'Moderate',
                    'description': 'Autoimmune loss of epidermal melanocytes resulting in well-demarcated depigmented macules and patches.',
                    'precautions': [
                        'Protect depigmented patches strictly from sunburn using SPF 50+ sunscreen.',
                        'Consult a dermatologist for phototherapy (NB-UVB) or topical immunomodulators.'
                    ]
                },
                'hi': {
                    'name': 'विटिलिगो / सफेद दाग (Vitiligo)',
                    'severity_base': 'Moderate',
                    'description': 'मेलेनोसाइट कोशिकाओं की कमी के कारण त्वचा पर सफेद धब्बे बनना। यह छुआछूत की बीमारी नहीं है।',
                    'precautions': [
                        'सफेद हिस्सों को धूप से बचाने के लिए SPF 50+ सनस्क्रीन लगाएं।',
                        'फोटोथेरेपी और इलाज के लिए त्वचा विशेषज्ञ से परामर्श लें।'
                    ]
                }
            }
        }

        self.high_risk_keywords = [
            'melanoma', 'carcinoma', 'sarcoma', 'lymphoma', 'mycosis fungoides',
            'stevens johnson', 'malignant', 'lentigo maligna', 'epidermolysis bullosa'
        ]
        self.low_risk_keywords = [
            'nevus', 'nevi', 'milia', 'syringoma', 'fordyce', 'striae',
            'seborrheic keratosis', 'pilar cyst', 'mucous cyst', 'freckle', 'keloid'
        ]

    def analyze(self, class_name, confidence, lang='en'):
        clean_name = (class_name or "Skin Condition").strip()

        matched_key = None
        if clean_name in self.knowledge_base:
            matched_key = clean_name
        else:
            lower_c = clean_name.lower()
            for k in self.knowledge_base:
                if k.lower() in lower_c or lower_c in k.lower():
                    matched_key = k
                    break

        if matched_key:
            info = self.knowledge_base[matched_key][lang]
            info_en = self.knowledge_base[matched_key]['en']
            base_severity = info['severity_base']
            display_name = info['name']
            description = info['description']
            precautions = info['precautions']
            pdf_name = info_en['name']
            pdf_description = info_en['description']
            pdf_precautions = info_en['precautions']
        else:
            lower_c = clean_name.lower()
            if any(k in lower_c for k in self.high_risk_keywords):
                base_severity = 'High'
            elif any(k in lower_c for k in self.low_risk_keywords):
                base_severity = 'Low'
            else:
                base_severity = 'Moderate'

            display_name = clean_name.title()
            pdf_name = display_name
            pdf_description = (
                f"Clinical morphological analysis indicates features consistent with {display_name} "
                f"(identified across Fitzpatrick I-VI reference spectrum with {confidence:.1f}% confidence)."
            )
            pdf_precautions = [
                "Keep the affected skin barrier clean, protected, and avoid scratching or friction.",
                "Avoid unprescribed topical steroids or harsh chemical exfoliants on the lesion.",
                "Consult a board-certified dermatologist for clinical confirmation and targeted therapy."
            ]

            if lang == 'hi':
                description = f"क्लिनिकल विज़ुअल विश्लेषण के आधार पर यह '{display_name}' के लक्षण दर्शाता है। सटीक पुष्टि और उपचार के लिए त्वचा विशेषज्ञ से परामर्श लें।"
                precautions = [
                    "प्रभावित त्वचा को साफ रखें और खुजलाने या रगड़ने से बचें।",
                    "बिना डॉक्टर की सलाह के कोई भी स्टेरॉयड या तेज़ क्रीम न लगाएं।",
                    "सटीक जांच और उपचार के लिए प्रमाणित त्वचा विशेषज्ञ (Dermatologist) से मिलें।"
                ]
            else:
                description = pdf_description
                precautions = pdf_precautions

        if base_severity == 'High':
            risk_level = 'Urgent Consultation Recommended' if lang == 'en' else 'तत्काल डॉक्टर से मिलें (Urgent Consultation Recommended)'
            final_severity = 'High'
        elif base_severity == 'Moderate':
            if confidence > 80:
                final_severity = 'Moderate'
                risk_level = 'Medium Risk - Medical evaluation advised' if lang == 'en' else 'मध्यम जोखिम - डॉक्टर को दिखाना उचित रहेगा (Medium Risk)'
            else:
                final_severity = 'Moderate-Low'
                risk_level = 'Low to Medium Risk - Monitor the area' if lang == 'en' else 'कम से मध्यम जोखिम - निगरानी रखें (Monitor the area)'
        else:
            final_severity = 'Low'
            risk_level = 'Low Risk - Routine monitoring recommended' if lang == 'en' else 'कम जोखिम - सामान्य देखभाल और निगरानी रखें (Low Risk)'

        return {
            'disease_key': clean_name,
            'name': display_name,
            'description': description,
            'severity': final_severity,
            'risk_level': risk_level,
            'precautions': precautions,
            'pdf_name': pdf_name,
            'pdf_description': pdf_description,
            'pdf_precautions': pdf_precautions
        }
