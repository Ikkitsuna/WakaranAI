# 🎮 WakaranAI

[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![Ollama](https://img.shields.io/badge/Ollama-Required-orange.svg)](https://ollama.ai/)
[![Stars](https://img.shields.io/github/stars/Ikkitsuna/WakaranAI?style=social)](https://github.com/Ikkitsuna/WakaranAI)

> **From わからない (I don't understand) to わかった (I understand)!**

**[🇫🇷 Version Française](README_FR.md)** | **[🇯🇵 日本語版](README_JA.md)** *(coming soon)*

Real-time universal translator for video games using OCR/Vision and local AI (Ollama).

Instantly translate untranslated game texts by capturing any screen area.

---

## ✨ Features

- **Three translation modes**: Tesseract (fast), EasyOCR (accurate), or Vision (context-aware)
- **Automatic language detection**: Detects source language automatically (Japanese, Korean, Chinese, etc.)
- **Customizable hotkeys**: Prevent conflicts with games using modifier combinations
- **Global hotkey** to capture and translate on the fly
- **Mode switching hotkey** to cycle between translation modes in real-time
- **Visual area selection** for precise text capture
- **100% local translation** via Ollama (privacy-friendly)
- **Elegant transparent overlay** with auto-close (configurable timeout)
- **Configuration GUI** for easy setup

---

## 🚀 Translation Modes

### 1. Tesseract Mode (Fast ⚡)
- **Pipeline**: Screenshot → Tesseract OCR → LLM translation
- **Speed**: ⚡ Very fast (2-5 seconds)
- **Accuracy**: ✅ Good for clear text
- **GPU Usage**: Minimal (great for gaming)
- **Best for**: Active gameplay, simple text, European languages

### 2. EasyOCR Mode (Accurate 🎯)
- **Pipeline**: Screenshot → EasyOCR → LLM translation
- **Speed**: ⚡⚡ Fast (5-10 seconds)
- **Accuracy**: ✅✅ Excellent for Asian languages
- **GPU Usage**: Medium (with CUDA) or CPU
- **Best for**: Japanese, Korean, Chinese, 80+ languages
- **Note**: Requires Python 3.11 or 3.12

### 3. Vision Mode (Context-Aware 🔍)
- **Pipeline**: Screenshot → Vision Model → Direct translation
- **Speed**: 🐌 Slow (10-30 seconds)
- **Accuracy**: ✅✅✅ Excellent, understands visual context
- **GPU Usage**: High (may cause lag during gameplay)
- **Best for**: Screenshots, stylized text, paused games

### Switch Between Modes

**In-game**: Press `Ctrl+Shift+M` to cycle through modes!

```
Tesseract → Ctrl+Shift+M → EasyOCR → Ctrl+Shift+M → Vision → Ctrl+Shift+M → Tesseract...
```

---

## 🚀 Quick Installation

### Option 1: Automatic Installation (Recommended)

1. Download the project (ZIP or `git clone`)
2. Double-click **`INSTALL.bat`**
3. Wait for installation to complete
4. Done! 🎉

### Option 2: Manual Installation

#### Prerequisites

1. **Python 3.11 or 3.12** ([Download here](https://www.python.org/downloads/))
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation!
2. **Ollama** ([Download here](https://ollama.ai/))
3. **Tesseract OCR** ([Download here](https://github.com/UB-Mannheim/tesseract/wiki))
   - Add to PATH: `C:\Program Files\Tesseract-OCR`
4. **Git** (optional, for updates) ([Download here](https://git-scm.com/))

#### Manual Setup Steps

```bash
# 1. Create virtual environment
python -m venv venv311

# 2. Activate environment (Windows)
venv311\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

#### Install Ollama and Models

1. Install Ollama: [https://ollama.ai](https://ollama.ai)
2. Download models:
   ```bash
   # For OCR modes (fast, recommended)
   ollama pull gemma2:2b

   # For Vision mode (accurate, optional)
   ollama pull gemma3:4b
   ```
3. Start Ollama server:
   ```bash
   ollama serve
   ```

**Note about EasyOCR**: EasyOCR is **optional** but recommended for:
- 🇯🇵 Japanese games (kanji, hiragana, katakana)
- 🇨🇳 Chinese games (simplified and traditional)
- 🇰🇷 Korean games (hangul)
- 🎨 Exotic/stylized fonts

To enable EasyOCR: Uncomment lines in `requirements.txt` and re-run `INSTALL.bat`

---

## ⚙️ Configuration

### Graphical Interface (Recommended)

Double-click **`CONFIGURE.bat`** to open the configuration interface and customize:
- 🎯 **Keyboard shortcuts** (customizable hotkeys)
- 🌍 **Source and target languages**
- ⚙️ **Default translation mode**
- ⏱️ **Overlay display duration**
- 🤖 **Ollama models**

### Manual Configuration (config.json)

You can also directly edit `config.json`:

```json
{
  "translation_mode": "tesseract",
  "vision_model": "gemma3:4b",
  "ollama_model": "gemma2:2b",
  "ollama_url": "http://localhost:11434",
  "source_lang": "en",
  "target_lang": "fr",
  "ocr_languages": ["ja", "en"],
  "auto_detect_language": true,
  "hotkey": "ctrl+shift+t",
  "toggle_mode_hotkey": "ctrl+shift+m",
  "overlay_timeout": 60
}
```

### Configuration Options

- **overlay_timeout**: Overlay display duration in seconds
  - Default: `60` (1 minute)
  - Fast readers: `30` seconds
  - Slow readers: `90` or `120` seconds

- **Supported language codes**: `en`, `fr`, `es`, `de`, `it`, `pt`, `ja`, `ko`, `zh`

---

## 🎯 Usage

### Quick Launch

Double-click **`RUN.bat`** to start WakaranAI.

### Manual Launch

```bash
# Start Ollama (in separate terminal)
ollama serve

# Launch WakaranAI
venv311\Scripts\python main.py
```

### Default Shortcuts

- **`Ctrl+Shift+T`**: Translate screen area
- **`Ctrl+Shift+M`**: Switch mode (Tesseract ↔ EasyOCR ↔ Vision)
- **`Escape`**: Cancel selection
- **`Ctrl+C`**: Quit application (in console)

> 💡 **Tip**: Use combinations with modifiers (Ctrl, Shift, Alt) to avoid conflicts with games!

### Workflow

1. Launch your game
2. Press **`Ctrl+Shift+T`** to capture
3. Draw a rectangle around the text to translate
4. Wait for translation (2-5s in Tesseract, 5-10s in EasyOCR, 10-30s in Vision)
5. Read the translation in the overlay (stays 60 seconds by default)
6. If too slow, press **`Ctrl+Shift+M`** to switch to fast Tesseract mode!

---

## 🔄 Updates

### With Git (recommended)

Double-click **`UPDATE.bat`** to automatically update code and dependencies.

### Without Git

1. Download latest version from GitHub
2. Replace files (except `config.json`)
3. Run `UPDATE.bat` to update dependencies

---

## 🐛 Troubleshooting

### Overlay not showing
- Check if your shortcut is used by the game
- Try a combination with `Ctrl+Shift+...`
- Launch `CONFIGURE.bat` to change shortcuts

### Mouse still captured by game
- Switch game to **windowed mode** (windowed or borderless)
- Use `Escape` to cancel selection
- This is a limitation with fullscreen DirectX/OpenGL games

### "Unable to connect to Ollama"
- Check Ollama is running: `ollama serve`
- Test URL: open `http://localhost:11434` in browser
- Check port 11434 isn't blocked by firewall

### "Tesseract not found" or "TesseractNotFoundError"
- Check Tesseract is installed: `tesseract --version`
- On Windows, add to PATH or re-run `INSTALL.bat`

### "No text detected"
- Selected area may be too small or blurry
- Try EasyOCR mode: `Ctrl+Shift+M` to switch modes
- Text contrast may be too low

### "Module not found" error
- Re-run `INSTALL.bat`
- Or manually: `venv311\Scripts\pip install -r requirements.txt`

### Slow performance
- Use **Tesseract mode** for gaming
- Check CPU/GPU (Vision mode is very intensive)
- Reduce selected area size

---

## 📁 Main Files

```
WakaranAI/
├── INSTALL.bat            # 🔧 Automatic installation
├── RUN.bat                # ▶️ Quick launcher
├── CONFIGURE.bat          # ⚙️ Configuration interface
├── UPDATE.bat             # 🔄 Automatic update
├── main.py                # Main entry point
├── config_gui.py          # Configuration interface
├── config.json            # Configuration (created on first run)
└── venv311/               # Virtual environment (created by INSTALL.bat)
```

---

## 📝 Roadmap

- [ ] Linux/Mac support
- [ ] Automatic text zone detection
- [ ] Translation history
- [ ] Multi-monitor support
- [ ] Full GUI (without console)
- [ ] Customizable overlay themes
- [ ] More LLM model support

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open an issue to report a bug
- Suggest a feature
- Submit a pull request

---

## 📄 License

MIT License - This project is under MIT license. Feel free to adapt it to your needs!

---

## 🙏 Credits

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [Ollama](https://ollama.ai/)
- [Gemma](https://ai.google.dev/gemma) (Google)

---

**Developed with ❤️ for the gaming community**

If you like this project, don't forget to give it a ⭐ on GitHub!
