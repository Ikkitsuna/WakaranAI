"""
Script de test pour l'auto-détection de langue
"""
from language_detector import LanguageDetector

# Créer détecteur
detector = LanguageDetector()

# Tests avec différentes langues
test_texts = {
    "Anglais": "Hello world! This is a test of the automatic language detection system.",
    "Français": "Bonjour le monde! Ceci est un test du système de détection automatique.",
    "Japonais (Hiragana)": "こんにちは世界！これは自動言語検出システムのテストです。",
    "Japonais (Katakana)": "テストメッセージ。カタカナで書かれています。",
    "Japonais (Kanji)": "日本語のテキストです。漢字が含まれています。",
    "Coréen": "안녕하세요! 한국어 텍스트입니다.",
    "Chinois simplifié": "你好世界！这是简体中文测试。",
    "Arabe": "مرحبا بالعالم! هذا اختبار للغة العربية.",
    "Russe": "Привет мир! Это тест русского языка.",
    "Mixte (Anglais + Japonais)": "Hello こんにちは World 世界！",
}

print("=" * 80)
print("TEST AUTO-DÉTECTION DE LANGUE")
print("=" * 80)

for nom, texte in test_texts.items():
    print(f"\n📝 {nom}:")
    print(f"   Texte: {texte[:50]}{'...' if len(texte) > 50 else ''}")
    
    # Détecter scripts
    scripts = detector.detect_scripts(texte)
    print(f"   Scripts: {scripts}")
    
    # Détecter langues
    langues = detector.detect_language(texte)
    print(f"   Langues détectées: {langues}")
    
    # Config OCR recommandée
    config = detector.get_ocr_config(texte)
    print(f"   Mode recommandé: {config['recommended_mode']}")
    print(f"   Langues OCR: {config['languages']}")
    print(f"   Confiance: {config['confidence']}")

print("\n" + "=" * 80)
print("✅ Tests terminés!")
print("=" * 80)
