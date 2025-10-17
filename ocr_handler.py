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
                
                # EasyOCR a des contraintes de compatibilité de langues
                # Japonais uniquement compatible avec anglais
                fixed_languages = self._fix_easyocr_language_compatibility(languages)
                if fixed_languages != languages:
                    print(f"   ℹ️ Langues ajustées pour compatibilité EasyOCR: {', '.join(fixed_languages)}")
                
                self.reader = easyocr.Reader(fixed_languages, gpu=True)
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
    
    def _fix_easyocr_language_compatibility(self, languages):
        """
        Corrige les incompatibilités de langues pour EasyOCR
        
        EasyOCR a des contraintes :
        - Japonais (ja) uniquement compatible avec anglais (en)
        - Coréen (ko) uniquement compatible avec anglais (en)
        - Chinois compatible avec d'autres langues
        
        Args:
            languages: Liste des langues demandées
            
        Returns:
            list: Liste corrigée des langues
        """
        # Langues asiatiques qui nécessitent l'anglais
        asian_langs_need_en = {'ja', 'ko'}
        
        fixed = list(languages)
        
        # Si on a du japonais ou coréen
        if any(lang in asian_langs_need_en for lang in languages):
            # S'assurer que 'en' est présent
            if 'en' not in fixed:
                fixed.append('en')
            
            # Retirer les langues latines autres que l'anglais (fr, es, de, etc.)
            latin_langs = {'fr', 'es', 'de', 'it', 'pt', 'ru', 'ar', 'th'}
            fixed = [lang for lang in fixed if lang not in latin_langs]
        
        return fixed
    
    def extract_text(self, image):
        """
        Extrait le texte d'une image avec auto-détection optionnelle des langues
        
        Args:
            image: PIL.Image
            
        Returns:
            tuple: (text, detected_lang) où detected_lang est le code de langue principale détectée
        """
        if not image:
            return "", None
        
        start_time = time.time()
        detected_lang = None
        
        try:
            # Si auto-détection activée avec Tesseract, faire une passe rapide
            if self.auto_detect and self.engine == 'tesseract':
                # Extraction rapide pour détecter la langue
                import pytesseract
                quick_text = pytesseract.image_to_string(image, config='--psm 6')
                
                if quick_text and len(quick_text.strip()) > 3:
                    # Détecter les langues
                    detected_langs = self.language_detector.detect_language(quick_text)
                    detected_lang = detected_langs[0] if detected_langs else None
                    
                    # Si différent de la config, ré-extraire avec langues détectées
                    if detected_langs and set(detected_langs) != set(self.languages):
                        print(f"🔍 Auto-détection: {', '.join(detected_langs)} (config: {', '.join(self.languages)})")
                        self.last_detected_languages = detected_langs
                        
                        # Sauvegarder config originale et extraire avec langues détectées
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
                            print(f"   📝 Langue principale: {detected_lang}")
                        else:
                            print("⚠️ Aucun texte détecté")
                        
                        return text, detected_lang
                        
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
                            print(f"   📝 Langue principale: {detected_lang}")
                        else:
                            print("⚠️ Aucun texte détecté")
                        
                        return text, detected_lang
            
            # Extraction normale
            if self.engine == 'easyocr':
                text = self._extract_with_easyocr(image)
            else:
                text = self._extract_with_tesseract(image)
            
            # Si auto-détection et pas encore fait, détecter maintenant
            if self.auto_detect and detected_lang is None and text and len(text.strip()) > 3:
                detected_langs = self.language_detector.detect_language(text)
                detected_lang = detected_langs[0] if detected_langs else None
            
            elapsed = time.time() - start_time
            print(f"⏱️ OCR terminé en {elapsed:.2f}s")
            
            # Nettoyer le texte
            text = text.strip()
            
            if text:
                print(f"✅ Texte détecté ({len(text)} caractères):")
                print(f"   '{text[:100]}{'...' if len(text) > 100 else ''}'")
                if detected_lang:
                    print(f"   📝 Langue détectée: {detected_lang}")
            else:
                print("⚠️ Aucun texte détecté")
            
            return text, detected_lang
            
        except Exception as e:
            print(f"❌ Erreur OCR: {e}")
            return "", None
    
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
