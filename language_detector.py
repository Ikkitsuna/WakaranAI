"""
Module pour la détection automatique de langue dans les images
"""
import re
from collections import Counter


class LanguageDetector:
    """Détecte la langue d'un texte basé sur les caractères Unicode"""
    
    def __init__(self):
        # Plages Unicode pour différents scripts
        self.script_ranges = {
            'latin': [(0x0041, 0x007A), (0x00C0, 0x00FF)],  # A-Z, a-z, accents
            'cyrillic': [(0x0400, 0x04FF)],  # Cyrillique
            'arabic': [(0x0600, 0x06FF)],  # Arabe
            'hiragana': [(0x3040, 0x309F)],  # Hiragana japonais
            'katakana': [(0x30A0, 0x30FF)],  # Katakana japonais
            'cjk': [(0x4E00, 0x9FFF)],  # Caractères CJK (chinois/japonais/coréen)
            'hangul': [(0xAC00, 0xD7AF)],  # Hangul coréen
            'thai': [(0x0E00, 0x0E7F)],  # Thaï
        }
    
    def detect_scripts(self, text):
        """
        Détecte les scripts présents dans le texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            dict: {script: count} des caractères par script
        """
        script_counts = Counter()
        
        for char in text:
            code_point = ord(char)
            
            # Ignorer espaces et ponctuation
            if char.isspace() or char in '.,;:!?-—()[]{}「」『』':
                continue
            
            # Vérifier chaque script
            for script, ranges in self.script_ranges.items():
                for start, end in ranges:
                    if start <= code_point <= end:
                        script_counts[script] += 1
                        break
        
        return script_counts
    
    def detect_language(self, text):
        """
        Détecte la ou les langues probables du texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            list: Liste des langues détectées (codes pour OCR)
        """
        if not text or len(text.strip()) < 2:
            return ['en']  # Défaut
        
        scripts = self.detect_scripts(text)
        total_chars = sum(scripts.values())
        
        if total_chars == 0:
            return ['en']
        
        detected_languages = []
        
        # Calculer les pourcentages
        percentages = {script: (count / total_chars * 100) for script, count in scripts.items()}
        
        # Japonais (hiragana, katakana ou CJK)
        japanese_score = (
            percentages.get('hiragana', 0) + 
            percentages.get('katakana', 0) + 
            percentages.get('cjk', 0) * 0.5  # CJK partagé avec chinois
        )
        
        if japanese_score > 10:  # Au moins 10% de caractères japonais
            detected_languages.append('ja')
        
        # Chinois (beaucoup de CJK, peu de hiragana/katakana)
        if percentages.get('cjk', 0) > 20 and japanese_score < 10:
            # Difficile de distinguer simplifié/traditionnel sans analyse poussée
            # On utilise simplifié par défaut (plus commun dans les jeux)
            detected_languages.append('ch_sim')
        
        # Coréen
        if percentages.get('hangul', 0) > 10:
            detected_languages.append('ko')
        
        # Latin (anglais, français, etc.)
        if percentages.get('latin', 0) > 20:
            detected_languages.append('en')
        
        # Cyrillique (russe)
        if percentages.get('cyrillic', 0) > 20:
            detected_languages.append('ru')
        
        # Arabe
        if percentages.get('arabic', 0) > 20:
            detected_languages.append('ar')
        
        # Thaï
        if percentages.get('thai', 0) > 20:
            detected_languages.append('th')
        
        # Si rien détecté, défaut anglais
        if not detected_languages:
            detected_languages = ['en']
        
        return detected_languages
    
    def get_ocr_config(self, text):
        """
        Retourne la configuration OCR optimale pour le texte
        
        Args:
            text: Texte échantillon
            
        Returns:
            dict: Configuration avec langues recommandées
        """
        languages = self.detect_language(text)
        scripts = self.detect_scripts(text)
        
        # Recommandation de mode OCR
        total_chars = sum(scripts.values())
        asian_chars = (
            scripts.get('hiragana', 0) + 
            scripts.get('katakana', 0) + 
            scripts.get('cjk', 0) + 
            scripts.get('hangul', 0)
        )
        
        asian_percentage = (asian_chars / total_chars * 100) if total_chars > 0 else 0
        
        # Recommander EasyOCR si beaucoup de caractères asiatiques
        recommended_mode = 'easyocr' if asian_percentage > 30 else 'tesseract'
        
        return {
            'languages': languages,
            'recommended_mode': recommended_mode,
            'scripts_detected': dict(scripts),
            'confidence': 'high' if total_chars > 10 else 'low'
        }


def auto_detect_languages(image, sample_text=None):
    """
    Helper function pour détecter automatiquement les langues
    
    Args:
        image: PIL Image (non utilisé pour l'instant, future analyse visuelle)
        sample_text: Texte échantillon déjà extrait (optionnel)
        
    Returns:
        list: Langues détectées
    """
    detector = LanguageDetector()
    
    if sample_text:
        return detector.detect_language(sample_text)
    
    # Si pas de texte fourni, on ne peut pas détecter
    # Dans le futur, on pourrait faire une pré-analyse rapide de l'image
    return ['en']
