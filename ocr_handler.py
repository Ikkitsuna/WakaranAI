"""
Module pour l'extraction de texte via OCR
"""
import time
import os
import platform
from PIL import Image
from language_detector import LanguageDetector


class OCRHandler:
    """Gère l'extraction de texte depuis des images"""
    
    def __init__(self, engine='tesseract', languages=['en'], auto_detect=True):
        """
        Initialise le handler OCR
        
        Args:
            engine: 'tesseract' ou 'easyocr'
            languages: Liste des langues pour EasyOCR (ex: ['en', 'ja', 'zh_sim'])
            auto_detect: Si True, détecte automatiquement les langues dans le texte
        """
        self.engine = engine
        self.reader = None
        self.languages = languages
        self.auto_detect = auto_detect
        self.language_detector = LanguageDetector() if auto_detect else None
        self.last_detected_languages = None
        
        if engine == 'easyocr':
            try:
                import easyocr
                print(f"📦 Initialisation EasyOCR avec langues: {', '.join(languages)}")
                print("   ⏳ Cela peut prendre quelques secondes...")
                self.reader = easyocr.Reader(languages, gpu=True)
                print("✅ EasyOCR initialisé")
            except ImportError:
                print("⚠️ EasyOCR n'est pas installé (nécessite Python 3.11 ou 3.12)")
                print("   Fallback sur Tesseract")
                self.engine = 'tesseract'
            except Exception as e:
                print(f"⚠️ Erreur lors de l'initialisation EasyOCR: {e}")
                print("   Fallback sur Tesseract")
                self.engine = 'tesseract'
        
        if self.engine == 'tesseract':
            try:
                import pytesseract
                
                # Auto-détecter le chemin de Tesseract sur Windows
                if platform.system() == 'Windows':
                    possible_paths = [
                        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                        r'C:\Tesseract-OCR\tesseract.exe',
                    ]
                    
                    for path in possible_paths:
                        if os.path.exists(path):
                            pytesseract.pytesseract.tesseract_cmd = path
                            print(f"✅ Tesseract trouvé: {path}")
                            break
                
                print("✅ Tesseract sélectionné")
            except ImportError:
                print("❌ Tesseract non installé!")
                raise
    
    def extract_text(self, image):
        """
        Extrait le texte d'une image avec auto-détection optionnelle des langues
        
        Args:
            image: PIL.Image
            
        Returns:
            str: Texte détecté (vide si rien trouvé)
        """
        if not image:
            return ""
        
        start_time = time.time()
        
        try:
            # Si auto-détection activée avec Tesseract, faire une passe rapide
            if self.auto_detect and self.engine == 'tesseract':
                # Extraction rapide pour détecter la langue
                import pytesseract
                quick_text = pytesseract.image_to_string(image, config='--psm 6')
                
                if quick_text and len(quick_text.strip()) > 3:
                    # Détecter les langues
                    detected_langs = self.language_detector.detect_language(quick_text)
                    
                    # Si différent de la config, ré-extraire avec langues détectées
                    if set(detected_langs) != set(self.languages):
                        print(f"🔍 Auto-détection: {', '.join(detected_langs)} (config: {', '.join(self.languages)})")
                        self.last_detected_languages = detected_langs
                        
                        # Sauvegarder config originale
                        original_langs = self.languages
                        self.languages = detected_langs
                        text = self._extract_with_tesseract(image)
                        self.languages = original_langs
                        
                        elapsed = time.time() - start_time
                        print(f"⏱️ OCR terminé en {elapsed:.2f}s")
                        text = text.strip()
                        
                        if text:
                            print(f"✅ Texte détecté ({len(text)} caractères):")
                            print(f"   '{text[:100]}{'...' if len(text) > 100 else ''}'")
                            print(f"   📝 Langues auto-détectées: {', '.join(detected_langs)}")
                        else:
                            print("⚠️ Aucun texte détecté")
                        
                        return text
            
            # Extraction normale
            if self.engine == 'easyocr':
                text = self._extract_with_easyocr(image)
            else:
                text = self._extract_with_tesseract(image)
            
            elapsed = time.time() - start_time
            print(f"⏱️ OCR terminé en {elapsed:.2f}s")
            
            # Nettoyer le texte
            text = text.strip()
            
            if text:
                print(f"✅ Texte détecté ({len(text)} caractères):")
                print(f"   '{text[:100]}{'...' if len(text) > 100 else ''}'")
            else:
                print("⚠️ Aucun texte détecté")
            
            return text
            
        except Exception as e:
            print(f"❌ Erreur OCR: {e}")
            return ""
    
    def _extract_with_tesseract(self, image):
        """Extraction avec Tesseract"""
        import pytesseract
        
        # Mapper les codes de langue pour Tesseract
        lang_map = {
            'en': 'eng',
            'fr': 'fra',
            'ja': 'jpn',
            'ko': 'kor',
            'zh_sim': 'chi_sim',
            'zh_tra': 'chi_tra',
            'es': 'spa',
            'de': 'deu',
            'it': 'ita',
            'pt': 'por',
            'ru': 'rus',
            'ar': 'ara',
        }
        
        # Construire la liste des langues pour Tesseract
        tesseract_langs = [lang_map.get(lang, 'eng') for lang in self.languages]
        lang_string = '+'.join(tesseract_langs)
        
        # Configuration pour améliorer la détection
        custom_config = f'--oem 3 --psm 6 -l {lang_string}'
        
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    
    def _extract_with_easyocr(self, image):
        """Extraction avec EasyOCR"""
        if self.reader is None:
            print("⚠️ EasyOCR reader non initialisé")
            return ""
        
        import numpy as np
        
        # Convertir PIL Image en numpy array pour EasyOCR
        img_array = np.array(image)
        
        # EasyOCR retourne une liste de (bbox, texte, confiance)
        results = self.reader.readtext(img_array)
        
        # Extraire juste le texte
        texts = [result[1] for result in results]
        
        # Joindre tous les textes détectés
        return '\n'.join(texts)
