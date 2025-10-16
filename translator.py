"""
Module pour la traduction via Ollama
"""
import requests
import json
import time


class OllamaTranslator:
    """Gère les traductions via l'API Ollama"""
    
    def __init__(self, config):
        """
        Initialise le traducteur
        
        Args:
            config: Dict avec ollama_url, ollama_model, source_lang, target_lang
        """
        self.url = config.get('ollama_url', 'http://localhost:11434')
        self.model = config.get('ollama_model', 'gemma2:2b')
        self.source_lang = config.get('source_lang', 'en')
        self.target_lang = config.get('target_lang', 'fr')
        
        # Map des codes de langue vers noms complets
        self.lang_names = {
            'en': 'English',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'it': 'Italian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
    
    def test_connection(self):
        """
        Teste la connexion à Ollama
        
        Returns:
            bool: True si OK, False sinon
        """
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                print(f"✅ Connexion Ollama OK")
                print(f"📦 Modèles disponibles: {', '.join(model_names)}")
                
                # Vérifier si le modèle configuré existe
                if any(self.model in name for name in model_names):
                    print(f"✅ Modèle '{self.model}' trouvé")
                    return True
                else:
                    print(f"⚠️ Modèle '{self.model}' non trouvé, mais Ollama est accessible")
                    return True
            else:
                print(f"❌ Ollama a répondu avec le code {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Impossible de se connecter à Ollama sur {self.url}")
            print("   Vérifiez qu'Ollama est bien lancé (ollama serve)")
            return False
        except Exception as e:
            print(f"❌ Erreur lors du test de connexion: {e}")
            return False
    
    def translate(self, text):
        """
        Traduit un texte
        
        Args:
            text: Texte à traduire
            
        Returns:
            str: Texte traduit ou message d'erreur
        """
        if not text or not text.strip():
            return "⚠️ Aucun texte à traduire"
        
        target_lang_name = self.lang_names.get(self.target_lang, self.target_lang)
        
        # Prompt optimisé pour la traduction
        prompt = f"Translate this to {target_lang_name}, only output the translation without any explanation:\n\n{text}"
        
        print(f"🌐 Traduction en cours ({self.source_lang} → {self.target_lang})...")
        print(f"   Texte: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Plus déterministe pour la traduction
                        "top_p": 0.9
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                translation = result.get('response', '').strip()
                
                elapsed = time.time() - start_time
                print(f"⏱️ Traduction terminée en {elapsed:.2f}s")
                print(f"✅ Résultat: '{translation[:100]}{'...' if len(translation) > 100 else ''}'")
                
                if translation:
                    return translation
                else:
                    return "⚠️ Aucune traduction reçue"
            else:
                error_msg = f"Erreur Ollama (code {response.status_code})"
                print(f"❌ {error_msg}")
                try:
                    error_detail = response.json()
                    print(f"   Détail: {error_detail}")
                except:
                    pass
                return f"❌ {error_msg}"
                
        except requests.exceptions.Timeout:
            print("❌ Timeout: Ollama met trop de temps à répondre")
            return "⏱️ Timeout: traduction trop longue"
        except requests.exceptions.ConnectionError:
            print("❌ Impossible de se connecter à Ollama")
            return "❌ Erreur: Ollama non accessible"
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return f"❌ Erreur: {str(e)}"
    
    def translate_streaming(self, text, callback):
        """
        Traduit avec streaming (pour une UX plus réactive)
        
        Args:
            text: Texte à traduire
            callback: Fonction appelée avec chaque chunk de traduction
            
        Returns:
            str: Traduction complète
        """
        if not text or not text.strip():
            return "⚠️ Aucun texte à traduire"
        
        target_lang_name = self.lang_names.get(self.target_lang, self.target_lang)
        prompt = f"Translate this to {target_lang_name}, only output the translation:\n\n{text}"
        
        print(f"🌐 Traduction streaming en cours...")
        
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9
                    }
                },
                stream=True,
                timeout=30
            )
            
            full_translation = ""
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    text_chunk = chunk.get('response', '')
                    full_translation += text_chunk
                    
                    if callback:
                        callback(text_chunk)
            
            print(f"✅ Traduction streaming terminée")
            return full_translation.strip()
            
        except Exception as e:
            print(f"❌ Erreur streaming: {e}")
            return f"❌ Erreur: {str(e)}"
