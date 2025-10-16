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
from ocr_handler import OCRHandler, preprocess_image_for_ocr
from translator import OllamaTranslator
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
        self.ocr = OCRHandler(engine=self.config.get('ocr_engine', 'tesseract'))
        self.translator = OllamaTranslator(self.config)
        
        self.is_processing = False
        self.hotkey = self.config.get('hotkey', 'F9')
        
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
            print(f"   Modèle: {config.get('ollama_model')}")
            print(f"   Traduction: {config.get('source_lang')} → {config.get('target_lang')}")
            print(f"   Hotkey: {config.get('hotkey')}")
            print(f"   OCR: {config.get('ocr_engine')}")
            return config
        except FileNotFoundError:
            print(f"⚠️ Fichier de configuration non trouvé: '{config_path}'")
            print("   Utilisation de la configuration par défaut")
            return {
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
        
        # Tester Ollama
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
            
            # Étape 2: Prétraitement de l'image (optionnel)
            # image = preprocess_image_for_ocr(image)
            
            # Étape 3: OCR
            print("\n🔍 Extraction du texte...")
            text = self.ocr.extract_text(image)
            
            if not text or len(text.strip()) < 2:
                print("❌ Aucun texte détecté dans la zone sélectionnée")
                show_error_overlay("Aucun texte détecté dans la zone")
                self.is_processing = False
                return
            
            # Étape 4: Traduction
            print("\n🌐 Traduction du texte...")
            translated = self.translator.translate(text)
            
            # Étape 5: Affichage de l'overlay
            print("\n📺 Affichage de l'overlay...")
            
            # Calculer la position de l'overlay (à côté de la zone sélectionnée)
            overlay_x = bbox[2] + 10  # À droite de la zone
            overlay_y = bbox[1]
            
            # S'assurer que l'overlay reste dans l'écran
            # (simplification, on peut améliorer avec pywin32 pour obtenir la résolution exacte)
            if overlay_x > 1920 - 420:  # Supposons 1920 de largeur
                overlay_x = bbox[0] - 410  # À gauche si pas de place à droite
            
            # Lancer l'overlay dans un thread séparé
            overlay_thread = threading.Thread(
                target=show_overlay_threaded,
                args=(overlay_x, overlay_y, text, translated, 400, 250),
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
    
    def run(self):
        """Lance l'application"""
        # Tester la configuration
        if not self.test_setup():
            print("\n❌ Configuration incorrecte, impossible de démarrer")
            sys.exit(1)
        
        print("\n" + "=" * 50)
        print("✅ GAME TRANSLATOR PRÊT!")
        print("=" * 50)
        print(f"📌 Appuyez sur {self.hotkey} pour commencer une traduction")
        print("📌 Appuyez sur Ctrl+C pour quitter")
        print("=" * 50)
        
        # Enregistrer la hotkey
        keyboard.add_hotkey(self.hotkey, self.on_hotkey_pressed)
        
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
