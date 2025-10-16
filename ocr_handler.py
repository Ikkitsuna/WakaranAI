"""
Module pour l'extraction de texte via OCR
"""
import time
import os
import platform
from PIL import Image


class OCRHandler:
    """Gère l'extraction de texte depuis des images"""
    
    def __init__(self, engine='tesseract'):
        """
        Initialise le handler OCR
        
        Args:
            engine: 'tesseract' ou 'easyocr'
        """
        self.engine = engine
        self.reader = None
        
        if engine == 'easyocr':
            try:
                import easyocr
                print("🔧 Initialisation d'EasyOCR...")
                self.reader = easyocr.Reader(['en', 'fr'], gpu=False)
                print("✅ EasyOCR prêt")
            except ImportError:
                print("⚠️ EasyOCR non installé, fallback sur Tesseract")
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
        Extrait le texte d'une image
        
        Args:
            image: PIL.Image
            
        Returns:
            str: Texte détecté (vide si rien trouvé)
        """
        if not image:
            return ""
        
        start_time = time.time()
        
        try:
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
        
        # Configuration pour améliorer la détection
        custom_config = r'--oem 3 --psm 6'
        
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    
    def _extract_with_easyocr(self, image):
        """Extraction avec EasyOCR"""
        if not self.reader:
            return ""
        
        # EasyOCR attend un numpy array ou un chemin de fichier
        import numpy as np
        img_array = np.array(image)
        
        results = self.reader.readtext(img_array)
        
        # Combiner tous les textes détectés
        texts = [result[1] for result in results]
        return ' '.join(texts)


def preprocess_image_for_ocr(image):
    """
    Prétraitement de l'image pour améliorer l'OCR
    
    Args:
        image: PIL.Image
        
    Returns:
        PIL.Image: Image prétraitée
    """
    try:
        import cv2
        import numpy as np
        
        # Convertir en numpy array
        img_array = np.array(image)
        
        # Convertir en niveaux de gris
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Augmenter le contraste
        gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        
        # Débruitage
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Binarisation adaptative
        binary = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Reconvertir en PIL Image
        processed_image = Image.fromarray(binary)
        
        return processed_image
        
    except ImportError:
        # Si OpenCV n'est pas disponible, retourner l'image originale
        print("⚠️ OpenCV non disponible, pas de prétraitement")
        return image
    except Exception as e:
        print(f"⚠️ Erreur prétraitement: {e}")
        return image
