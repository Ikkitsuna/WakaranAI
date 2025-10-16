"""
Game Translator - MVP
Outil de traduction en temps réel pour jeux vidéo
"""
import json
import sys
import threading
import time
from pathlib import Path

import keyboard

from screenshot import capture_with_selection
from ocr_handler import OCRHandler
from translator import OllamaTranslator
from vision_translator import VisionTranslator
from overlay import show_overlay_threaded, show_error_overlay


class GameTranslator:
    """Application principale"""
    
    def __init__(self, config_path='config.json'):
        """
        Initialise l'application
        
        Args:
            config_path: Chemin vers le fichier de configuration
        """
        print("🎮 Game Translator - Initialisation...")
        print("=" * 50)
        
        # Charger la configuration
        self.config = self.load_config(config_path)
        
        # Initialiser les composants
        self.translation_mode = self.config.get('translation_mode', 'ocr')
        
        # Initialiser le traducteur vision (lazy loading possible)
        self.vision_translator = None
        if self.translation_mode == 'vision':
            self.vision_translator = VisionTranslator(
                model_name=self.config.get('vision_model', 'gemma3:4b'),
                ollama_url=self.config.get('ollama_url', 'http://localhost:11434')
            )
        
        # Toujours initialiser OCR et translator classique (pour fallback)
        self.ocr = OCRHandler(engine=self.config.get('ocr_engine', 'tesseract'))
        self.translator = OllamaTranslator(self.config)
        
        self.is_processing = False
        self.hotkey = self.config.get('hotkey', 'F9')
        self.toggle_hotkey = self.config.get('toggle_mode_hotkey', 'F10')
        
        print("=" * 50)
    
    def load_config(self, config_path):
        """
        Charge la configuration depuis le fichier JSON
        
        Args:
            config_path: Chemin vers le fichier de configuration
            
        Returns:
            dict: Configuration
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Configuration chargée depuis '{config_path}'")
            
            # Afficher le mode de traduction
            translation_mode = config.get('translation_mode', 'ocr')
            print(f"   Mode: {translation_mode.upper()}")
            
            if translation_mode == 'vision':
                print(f"   Modèle Vision: {config.get('vision_model')}")
            else:
                print(f"   Modèle: {config.get('ollama_model')}")
                print(f"   OCR: {config.get('ocr_engine')}")
            
            print(f"   Traduction: {config.get('source_lang')} → {config.get('target_lang')}")
            print(f"   Hotkey: {config.get('hotkey')}")
            return config
        except FileNotFoundError:
            print(f"⚠️ Fichier de configuration non trouvé: '{config_path}'")
            print("   Utilisation de la configuration par défaut")
            return {
                'translation_mode': 'ocr',
                'vision_model': 'gemma3:4b',
                'ollama_model': 'gemma2:2b',
                'ollama_url': 'http://localhost:11434',
                'source_lang': 'en',
                'target_lang': 'fr',
                'hotkey': 'F9',
                'ocr_engine': 'tesseract'
            }
        except json.JSONDecodeError as e:
            print(f"❌ Erreur de parsing JSON: {e}")
            sys.exit(1)
    
    def test_setup(self):
        """
        Teste que tout est correctement configuré
        
        Returns:
            bool: True si OK, False sinon
        """
        print("\n🔍 Vérification de la configuration...")
        print("-" * 50)
        
        # Tester selon le mode
        if self.translation_mode == 'vision':
            print("📸 Mode VISION activé")
            if not self.vision_translator.test_connection():
                print("\n⚠️ Modèle vision non disponible, fallback sur mode OCR")
                self.translation_mode = 'ocr'
                return self.translator.test_connection()
        else:
            print("📝 Mode OCR activé")
            if not self.translator.test_connection():
                print("\n❌ Ollama n'est pas accessible!")
                print("   Assurez-vous qu'Ollama est lancé: ollama serve")
                return False
        
        print("-" * 50)
        return True
    
    def process_translation(self):
        """
        Workflow complet: capture → OCR → traduction → affichage
        """
        if self.is_processing:
            print("⚠️ Traitement déjà en cours, veuillez patienter...")
            return
        
        self.is_processing = True
        
        try:
            print("\n" + "=" * 50)
            print("🚀 NOUVEAU PROCESSUS DE TRADUCTION")
            print("=" * 50)
            
            # Étape 1: Capture de la zone sélectionnée
            image, bbox = capture_with_selection()
            
            if image is None:
                print("⚠️ Aucune capture effectuée")
                self.is_processing = False
                return
            
            # Variables pour le texte original et traduit
            text = None
            translated = None
            
            # ====== MODE VISION ======
            if self.translation_mode == 'vision':
                print("\n🤖 Mode VISION: Extraction et traduction directe...")
                
                try:
                    # Traduction directe via le modèle vision
                    target_lang_full = {
                        'fr': 'French',
                        'en': 'English',
                        'es': 'Spanish',
                        'de': 'German',
                        'it': 'Italian',
                        'pt': 'Portuguese',
                        'ja': 'Japanese',
                        'ko': 'Korean',
                        'zh': 'Chinese'
                    }.get(self.config.get('target_lang', 'fr'), 'French')
                    
                    translated = self.vision_translator.translate_image(
                        image, 
                        target_lang=target_lang_full
                    )
                    
                    # Vérifier si la traduction a échoué
                    if translated.startswith('[ERREUR:') or not translated.strip():
                        print("⚠️ Échec du mode vision, fallback sur OCR...")
                        self.translation_mode = 'ocr'  # Temporary fallback
                    else:
                        text = "[Texte extrait par vision]"  # Placeholder
                        print(f"✅ Vision OK: {len(translated)} caractères")
                
                except Exception as e:
                    print(f"⚠️ Erreur vision: {e}, fallback sur OCR...")
                    self.translation_mode = 'ocr'  # Temporary fallback
            
            # ====== MODE OCR (ou fallback) ======
            if self.translation_mode == 'ocr' or translated is None:
                print("\n🔍 Mode OCR: Extraction puis traduction...")
                
                # Étape 2: OCR
                text = self.ocr.extract_text(image)
                
                if not text or len(text.strip()) < 2:
                    print("❌ Aucun texte détecté dans la zone sélectionnée")
                    show_error_overlay("Aucun texte détecté dans la zone")
                    self.is_processing = False
                    return
                
                # Étape 3: Traduction
                print("\n🌐 Traduction du texte...")
                translated = self.translator.translate(text)
            
            # Restaurer le mode original si fallback temporaire
            if self.config.get('translation_mode') == 'vision':
                self.translation_mode = 'vision'
            
            # Étape 5: Affichage de l'overlay
            print("\n📺 Affichage de l'overlay...")
            
            # Calculer la position de l'overlay (à côté de la zone sélectionnée)
            overlay_x = bbox[2] + 10  # À droite de la zone
            overlay_y = bbox[1]
            
            # S'assurer que l'overlay reste dans l'écran
            # (simplification, on peut améliorer avec pywin32 pour obtenir la résolution exacte)
            if overlay_x > 1920 - 420:  # Supposons 1920 de largeur
                overlay_x = bbox[0] - 410  # À gauche si pas de place à droite
            
            # Récupérer le timeout depuis la config
            overlay_timeout = self.config.get('overlay_timeout', 60)
            
            # Lancer l'overlay dans un thread séparé
            overlay_thread = threading.Thread(
                target=show_overlay_threaded,
                args=(overlay_x, overlay_y, text, translated, 400, 250, overlay_timeout),
                daemon=True
            )
            overlay_thread.start()
            
            print("\n" + "=" * 50)
            print("✅ PROCESSUS TERMINÉ AVEC SUCCÈS")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n❌ ERREUR CRITIQUE: {e}")
            import traceback
            traceback.print_exc()
            show_error_overlay(f"Erreur: {str(e)}")
        
        finally:
            self.is_processing = False
    
    def on_hotkey_pressed(self):
        """Callback appelé quand la hotkey est pressée"""
        print(f"\n⌨️ Hotkey '{self.hotkey}' détectée!")
        
        # Lancer le traitement dans un thread pour ne pas bloquer la détection des touches
        thread = threading.Thread(target=self.process_translation, daemon=True)
        thread.start()
    
    def toggle_translation_mode(self):
        """Bascule entre mode vision et mode OCR"""
        if self.is_processing:
            print("⚠️ Traitement en cours, impossible de changer de mode")
            return
        
        # Toggle le mode
        if self.translation_mode == 'vision':
            self.translation_mode = 'ocr'
            print("\n" + "🔄" * 25)
            print("⚡ PASSAGE EN MODE OCR (RAPIDE)")
            print("   ✅ Meilleur pour gaming (faible latence)")
            print("   ✅ Utilise Tesseract + LLM")
            print("🔄" * 25)
        else:
            self.translation_mode = 'vision'
            
            # Initialiser le vision_translator si pas déjà fait
            if self.vision_translator is None:
                print("\n📦 Chargement du modèle vision...")
                self.vision_translator = VisionTranslator(
                    model_name=self.config.get('vision_model', 'gemma3:4b'),
                    ollama_url=self.config.get('ollama_url', 'http://localhost:11434')
                )
            
            print("\n" + "🔄" * 25)
            print("🤖 PASSAGE EN MODE VISION (PRÉCIS)")
            print("   ⚠️ Plus lent, meilleur hors gaming")
            print("   ✅ Extraction + traduction directe")
            print("🔄" * 25)
    
    def on_toggle_pressed(self):
        """Callback pour la hotkey de toggle"""
        print(f"\n⌨️ Toggle hotkey '{self.toggle_hotkey}' détectée!")
        thread = threading.Thread(target=self.toggle_translation_mode, daemon=True)
        thread.start()
    
    def run(self):
        """Lance l'application"""
        # Tester la configuration
        if not self.test_setup():
            print("\n❌ Configuration incorrecte, impossible de démarrer")
            sys.exit(1)
        
        print("\n" + "=" * 50)
        print("✅ GAME TRANSLATOR PRÊT!")
        print("=" * 50)
        print(f"📌 {self.hotkey}: Commencer une traduction")
        print(f"� {self.toggle_hotkey}: Changer de mode (vision ⇄ ocr)")
        print(f"📌 Ctrl+C: Quitter")
        print(f"   Mode actuel: {self.translation_mode.upper()}")
        print("=" * 50)
        
        # Enregistrer les hotkeys
        keyboard.add_hotkey(self.hotkey, self.on_hotkey_pressed)
        keyboard.add_hotkey(self.toggle_hotkey, self.on_toggle_pressed)
        
        try:
            # Boucle principale (bloquante)
            keyboard.wait()
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt de Game Translator...")
            print("=" * 50)
            sys.exit(0)


def main():
    """Point d'entrée principal"""
    try:
        app = GameTranslator()
        app.run()
    except Exception as e:
        print(f"\n❌ ERREUR FATALE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
