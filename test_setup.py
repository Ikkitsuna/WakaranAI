"""
Script de test pour vérifier que tout est correctement installé
"""
import sys
import importlib


def test_python_version():
    """Vérifie la version de Python"""
    print("🐍 Test Python...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requis: 3.10+)")
        return False


def test_package(package_name, import_name=None):
    """Teste l'import d'un package"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"   ✅ {package_name}")
        return True
    except ImportError:
        print(f"   ❌ {package_name} (non installé)")
        return False


def test_tesseract():
    """Teste Tesseract"""
    print("\n🔍 Test Tesseract OCR...")
    
    try:
        import pytesseract
        from PIL import Image
        
        # Créer une image de test
        test_img = Image.new('RGB', (200, 50), color='white')
        
        # Tenter une reconnaissance (devrait retourner vide mais pas d'erreur)
        try:
            pytesseract.image_to_string(test_img)
            print("   ✅ Tesseract fonctionne")
            return True
        except pytesseract.TesseractNotFoundError:
            print("   ❌ Tesseract non trouvé")
            print("      Installez Tesseract depuis:")
            print("      https://github.com/UB-Mannheim/tesseract/wiki")
            print("      Ou modifiez ocr_handler.py pour spécifier le chemin")
            return False
    except ImportError as e:
        print(f"   ❌ Erreur d'import: {e}")
        return False


def test_ollama():
    """Teste la connexion à Ollama"""
    print("\n🤖 Test Ollama...")
    
    try:
        import requests
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                print("   ✅ Ollama est accessible")
                
                if models:
                    print(f"   📦 Modèles disponibles:")
                    for model in models:
                        print(f"      - {model['name']}")
                    
                    # Vérifier si gemma2:2b existe
                    if any('gemma2' in m['name'] for m in models):
                        print("   ✅ gemma2:2b trouvé")
                    else:
                        print("   ⚠️ gemma2:2b non trouvé")
                        print("      Exécutez: ollama pull gemma2:2b")
                else:
                    print("   ⚠️ Aucun modèle installé")
                    print("      Exécutez: ollama pull gemma2:2b")
                
                return True
            else:
                print(f"   ❌ Ollama a retourné le code {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Impossible de se connecter à Ollama")
            print("      Assurez-vous qu'Ollama est lancé:")
            print("      - Sur Windows, Ollama démarre automatiquement")
            print("      - Sinon, exécutez: ollama serve")
            return False
            
    except ImportError:
        print("   ❌ Package 'requests' non installé")
        return False


def test_keyboard_permissions():
    """Teste les permissions pour les hotkeys"""
    print("\n⌨️ Test permissions hotkey...")
    
    try:
        import keyboard
        print("   ✅ Package 'keyboard' installé")
        print("   ⚠️ Note: Sur Windows, lancez l'app en administrateur pour les hotkeys globales")
        return True
    except ImportError:
        print("   ❌ Package 'keyboard' non installé")
        return False


def main():
    """Exécute tous les tests"""
    print("=" * 60)
    print("🧪 GAME TRANSLATOR - Test d'installation")
    print("=" * 60)
    
    results = []
    
    # Test Python
    results.append(test_python_version())
    
    # Test des packages
    print("\n📦 Test des packages Python...")
    results.append(test_package("PIL (Pillow)", "PIL"))
    results.append(test_package("requests"))
    results.append(test_package("keyboard"))
    results.append(test_package("mss"))
    results.append(test_package("pytesseract"))
    
    # Test Tesseract
    results.append(test_tesseract())
    
    # Test Ollama
    results.append(test_ollama())
    
    # Test permissions
    results.append(test_keyboard_permissions())
    
    # Résumé
    print("\n" + "=" * 60)
    total = len(results)
    passed = sum(results)
    
    if passed == total:
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print("=" * 60)
        print("\n🚀 Vous pouvez lancer l'application:")
        print("   python main.py")
    else:
        print(f"⚠️ {total - passed}/{total} test(s) échoué(s)")
        print("=" * 60)
        print("\n📖 Consultez INSTALL_WINDOWS.md pour l'aide à l'installation")
    
    print("\n")


if __name__ == '__main__':
    main()
