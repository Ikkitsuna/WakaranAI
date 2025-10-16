"""
Module pour la traduction via modèle vision multimodal
Utilise un modèle vision (comme gemma3:4b) pour extraire et traduire le texte directement depuis l'image
"""
import base64
import io
import requests
from PIL import Image


class VisionTranslator:
    """Traducteur utilisant un modèle vision multimodal via Ollama"""
    
    def __init__(self, model_name="gemma3:4b", ollama_url="http://localhost:11434"):
        """
        Initialise le traducteur vision
        
        Args:
            model_name: Nom du modèle vision Ollama (doit supporter les images)
            ollama_url: URL de l'API Ollama
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.session = requests.Session()
        
    def _image_to_base64(self, pil_image):
        """
        Convertit une image PIL en base64
        
        Args:
            pil_image: Image PIL
            
        Returns:
            str: Image encodée en base64
        """
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    def test_connection(self):
        """
        Teste la connexion à Ollama et vérifie que le modèle est disponible
        
        Returns:
            bool: True si la connexion est OK et le modèle existe
        """
        try:
            # Tester la connexion
            response = self.session.get(f"{self.ollama_url}/api/tags", timeout=5)
            
            if response.status_code != 200:
                print(f"❌ Ollama non accessible (status: {response.status_code})")
                return False
            
            # Vérifier que le modèle existe
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            if not models:
                print("⚠️ Aucun modèle Ollama trouvé")
                return False
            
            # Vérifier si le modèle vision est disponible
            model_found = any(self.model_name in model for model in models)
            
            if not model_found:
                print(f"⚠️ Modèle vision '{self.model_name}' non trouvé")
                print(f"📦 Modèles disponibles: {', '.join(models)}")
                return False
            
            print(f"✅ Modèle vision '{self.model_name}' trouvé")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion à Ollama: {e}")
            return False
    
    def translate_image(self, pil_image, target_lang="French", source_lang="English"):
        """
        Extrait et traduit le texte directement depuis l'image via le modèle vision
        
        Args:
            pil_image: Image PIL à traiter
            target_lang: Langue cible (ex: "French", "Spanish", etc.)
            source_lang: Langue source (optionnel, pour le prompt)
            
        Returns:
            str: Texte traduit ou message d'erreur
        """
        try:
            print(f"🔄 Conversion de l'image en base64...")
            image_base64 = self._image_to_base64(pil_image)
            
            # Construire le prompt
            prompt = (
                f"Extract all visible text from this image and translate it to {target_lang}. "
                f"Only output the {target_lang} translation, no explanations, no original text."
            )
            
            print(f"🤖 Envoi au modèle vision '{self.model_name}'...")
            print(f"📝 Target: {target_lang}")
            
            # Appel à l'API Ollama avec l'image
            response = self.session.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "images": [image_base64],
                    "stream": False
                },
                timeout=60  # Les modèles vision peuvent être plus lents
            )
            
            if response.status_code != 200:
                error_msg = f"Erreur API Ollama (status {response.status_code})"
                print(f"❌ {error_msg}")
                return f"[ERREUR: {error_msg}]"
            
            data = response.json()
            translation = data.get('response', '').strip()
            
            if not translation:
                print("⚠️ Aucune traduction reçue du modèle")
                return "[Aucun texte détecté ou traduit]"
            
            print(f"✅ Traduction vision reçue ({len(translation)} caractères)")
            return translation
            
        except requests.exceptions.Timeout:
            error_msg = "Timeout - Le modèle vision met trop de temps à répondre"
            print(f"❌ {error_msg}")
            return f"[ERREUR: {error_msg}]"
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erreur réseau: {e}"
            print(f"❌ {error_msg}")
            return f"[ERREUR: {error_msg}]"
            
        except Exception as e:
            error_msg = f"Erreur inattendue: {e}"
            print(f"❌ {error_msg}")
            return f"[ERREUR: {error_msg}]"
    
    def get_model_info(self):
        """
        Récupère les informations sur le modèle vision
        
        Returns:
            dict: Informations sur le modèle ou None si erreur
        """
        try:
            response = self.session.get(f"{self.ollama_url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                for model in models:
                    if self.model_name in model['name']:
                        return {
                            'name': model['name'],
                            'size': model.get('size', 'unknown'),
                            'modified': model.get('modified_at', 'unknown')
                        }
            
            return None
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des infos du modèle: {e}")
            return None


# Fonction helper pour un usage simple
def translate_screenshot_with_vision(pil_image, model="gemma3:4b", target_lang="French"):
    """
    Helper function pour traduire une capture d'écran avec le modèle vision
    
    Args:
        pil_image: Image PIL
        model: Nom du modèle vision
        target_lang: Langue cible
        
    Returns:
        str: Traduction
    """
    translator = VisionTranslator(model_name=model)
    return translator.translate_image(pil_image, target_lang=target_lang)
