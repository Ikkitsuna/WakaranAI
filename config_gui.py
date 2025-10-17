"""
Interface graphique de configuration pour Game Translator
"""
import json
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
from pathlib import Path


class ConfigGUI:
    """Interface de configuration graphique"""

    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self.load_config()
        self.recording_key = None
        self.temp_hotkey = None

        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("🎮 Game Translator - Configuration")
        self.root.geometry("750x750")
        self.root.resizable(True, True)  # Permettre le redimensionnement
        self.root.configure(bg='#1e1e1e')

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1e1e1e', foreground='#ffffff', font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#61dafb')
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TCombobox', fieldbackground='#404040', background='#404040', foreground='#ffffff', selectbackground='#61dafb')
        style.map('TCombobox', fieldbackground=[('readonly', '#404040')])
        style.map('TCombobox', selectbackground=[('readonly', '#61dafb')])
        style.map('TCombobox', selectforeground=[('readonly', '#000000')])

        self.create_widgets()

    def load_config(self):
        """Charge la configuration existante"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'translation_mode': 'tesseract',
                'vision_model': 'gemma3:4b',
                'ollama_model': 'gemma2:2b',
                'ollama_url': 'http://localhost:11434',
                'source_lang': 'en',
                'target_lang': 'fr',
                'ocr_languages': ['ja', 'en'],
                'auto_detect_language': True,
                'hotkey': 'ctrl+shift+t',
                'toggle_mode_hotkey': 'ctrl+shift+m',
                'overlay_timeout': 60
            }

    def save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder la configuration:\n{e}")
            return False

    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Canvas pour permettre le scroll
        canvas = tk.Canvas(self.root, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)

        # Frame principal avec padding dans le canvas
        main_frame = tk.Frame(canvas, bg='#1e1e1e', padx=20, pady=20)

        # Créer une fenêtre dans le canvas
        canvas_frame = canvas.create_window((0, 0), window=main_frame, anchor="nw")

        # Configurer le scroll
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        main_frame.bind("<Configure>", configure_scroll)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack le canvas et la scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind la molette de la souris
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Titre
        title = ttk.Label(main_frame, text="⚙️ Configuration", style='Title.TLabel')
        title.pack(pady=(0, 20))

        # === SECTION HOTKEYS ===
        hotkey_frame = tk.LabelFrame(
            main_frame, text=" 🎯 Raccourcis Clavier ",
            bg='#2d2d2d', fg='#61dafb',
            font=('Segoe UI', 11, 'bold'),
            padx=15, pady=15
        )
        hotkey_frame.pack(fill=tk.X, pady=(0, 15))

        # Hotkey traduction
        tk.Label(
            hotkey_frame, text="Raccourci pour traduire:",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=0, column=0, sticky='w', pady=5)

        self.hotkey_entry = tk.Entry(
            hotkey_frame, font=('Segoe UI', 11), width=25,
            bg='#404040', fg='#ffffff', insertbackground='white',
            disabledbackground='#303030', disabledforeground='#aaaaaa',
            readonlybackground='#404040'
        )
        self.hotkey_entry.insert(0, self.config.get('hotkey', 'ctrl+shift+t'))
        self.hotkey_entry.grid(row=0, column=1, padx=10, pady=5)
        self.hotkey_entry.config(state='readonly')

        tk.Button(
            hotkey_frame, text="📝 Changer",
            command=lambda: self.record_hotkey('hotkey'),
            bg='#404040', fg='#ffffff', font=('Segoe UI', 9),
            cursor='hand2', relief=tk.FLAT, padx=10, pady=5
        ).grid(row=0, column=2, pady=5)

        # Hotkey toggle mode
        tk.Label(
            hotkey_frame, text="Raccourci pour changer de mode:",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=1, column=0, sticky='w', pady=5)

        self.toggle_entry = tk.Entry(
            hotkey_frame, font=('Segoe UI', 11), width=25,
            bg='#404040', fg='#ffffff', insertbackground='white',
            disabledbackground='#303030', disabledforeground='#aaaaaa',
            readonlybackground='#404040'
        )
        self.toggle_entry.insert(0, self.config.get('toggle_mode_hotkey', 'ctrl+shift+m'))
        self.toggle_entry.grid(row=1, column=1, padx=10, pady=5)
        self.toggle_entry.config(state='readonly')

        tk.Button(
            hotkey_frame, text="📝 Changer",
            command=lambda: self.record_hotkey('toggle_mode_hotkey'),
            bg='#404040', fg='#ffffff', font=('Segoe UI', 9),
            cursor='hand2', relief=tk.FLAT, padx=10, pady=5
        ).grid(row=1, column=2, pady=5)

        # Info
        info_label = tk.Label(
            hotkey_frame,
            text="💡 Conseil: Utilisez des combinaisons (Ctrl+Shift+...) pour éviter les conflits avec les jeux",
            bg='#2d2d2d', fg='#888888', font=('Segoe UI', 8),
            wraplength=600, justify=tk.LEFT
        )
        info_label.grid(row=2, column=0, columnspan=3, pady=(10, 0))

        # === SECTION TRADUCTION ===
        trans_frame = tk.LabelFrame(
            main_frame, text=" 🌍 Paramètres de Traduction ",
            bg='#2d2d2d', fg='#61dafb',
            font=('Segoe UI', 11, 'bold'),
            padx=15, pady=15
        )
        trans_frame.pack(fill=tk.X, pady=(0, 15))

        # Mode de traduction
        tk.Label(
            trans_frame, text="Mode de traduction par défaut:",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=0, column=0, sticky='w', pady=5)

        self.mode_combo = ttk.Combobox(
            trans_frame, values=['tesseract', 'easyocr', 'vision'],
            state='readonly', width=23, font=('Segoe UI', 10)
        )
        self.mode_combo.set(self.config.get('translation_mode', 'tesseract'))
        self.mode_combo.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Langue source
        tk.Label(
            trans_frame, text="Langue source:",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=1, column=0, sticky='w', pady=5)

        lang_values = ['en', 'fr', 'es', 'de', 'it', 'pt', 'ja', 'ko', 'zh']
        self.source_combo = ttk.Combobox(
            trans_frame, values=lang_values,
            state='readonly', width=23, font=('Segoe UI', 10)
        )
        self.source_combo.set(self.config.get('source_lang', 'en'))
        self.source_combo.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Langue cible
        tk.Label(
            trans_frame, text="Langue cible:",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=2, column=0, sticky='w', pady=5)

        self.target_combo = ttk.Combobox(
            trans_frame, values=lang_values,
            state='readonly', width=23, font=('Segoe UI', 10)
        )
        self.target_combo.set(self.config.get('target_lang', 'fr'))
        self.target_combo.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Auto-détection
        self.auto_detect_var = tk.BooleanVar(value=self.config.get('auto_detect_language', True))
        tk.Checkbutton(
            trans_frame, text="Détection automatique de la langue source",
            variable=self.auto_detect_var,
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10),
            selectcolor='#1e1e1e', activebackground='#2d2d2d',
            activeforeground='#ffffff'
        ).grid(row=3, column=0, columnspan=2, sticky='w', pady=5)

        # === SECTION AFFICHAGE ===
        display_frame = tk.LabelFrame(
            main_frame, text=" 📺 Affichage ",
            bg='#2d2d2d', fg='#61dafb',
            font=('Segoe UI', 11, 'bold'),
            padx=15, pady=15
        )
        display_frame.pack(fill=tk.X, pady=(0, 15))

        # Timeout overlay
        tk.Label(
            display_frame, text="Durée d'affichage de l'overlay (secondes):",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=0, column=0, sticky='w', pady=5)

        self.timeout_spin = tk.Spinbox(
            display_frame, from_=5, to=300, increment=5,
            width=10, font=('Segoe UI', 11),
            bg='#404040', fg='#ffffff', buttonbackground='#505050',
            insertbackground='white', readonlybackground='#404040'
        )
        self.timeout_spin.delete(0, tk.END)
        self.timeout_spin.insert(0, self.config.get('overlay_timeout', 60))
        self.timeout_spin.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # === SECTION MODÈLES ===
        models_frame = tk.LabelFrame(
            main_frame, text=" 🤖 Modèles Ollama ",
            bg='#2d2d2d', fg='#61dafb',
            font=('Segoe UI', 11, 'bold'),
            padx=15, pady=15
        )
        models_frame.pack(fill=tk.X, pady=(0, 15))

        # URL Ollama
        tk.Label(
            models_frame, text="URL Ollama:",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=0, column=0, sticky='w', pady=5)

        self.ollama_url_entry = tk.Entry(
            models_frame, font=('Segoe UI', 11), width=35,
            bg='#404040', fg='#ffffff', insertbackground='white'
        )
        self.ollama_url_entry.insert(0, self.config.get('ollama_url', 'http://localhost:11434'))
        self.ollama_url_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Modèle LLM
        tk.Label(
            models_frame, text="Modèle LLM (OCR modes):",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=1, column=0, sticky='w', pady=5)

        self.llm_entry = tk.Entry(
            models_frame, font=('Segoe UI', 11), width=35,
            bg='#404040', fg='#ffffff', insertbackground='white'
        )
        self.llm_entry.insert(0, self.config.get('ollama_model', 'gemma2:2b'))
        self.llm_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Modèle Vision
        tk.Label(
            models_frame, text="Modèle Vision:",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 10)
        ).grid(row=2, column=0, sticky='w', pady=5)

        self.vision_entry = tk.Entry(
            models_frame, font=('Segoe UI', 11), width=35,
            bg='#404040', fg='#ffffff', insertbackground='white'
        )
        self.vision_entry.insert(0, self.config.get('vision_model', 'gemma3:4b'))
        self.vision_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # === BOUTONS ===
        button_frame = tk.Frame(main_frame, bg='#1e1e1e')
        button_frame.pack(pady=(10, 0))

        tk.Button(
            button_frame, text="💾 Sauvegarder",
            command=self.save_and_close,
            bg='#61dafb', fg='#1e1e1e', font=('Segoe UI', 11, 'bold'),
            cursor='hand2', relief=tk.FLAT, padx=20, pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame, text="❌ Annuler",
            command=self.root.quit,
            bg='#404040', fg='#ffffff', font=('Segoe UI', 11),
            cursor='hand2', relief=tk.FLAT, padx=20, pady=10
        ).pack(side=tk.LEFT, padx=5)

    def record_hotkey(self, key_type):
        """Enregistre une nouvelle hotkey"""
        self.recording_key = key_type

        # Créer une fenêtre modale pour l'enregistrement
        record_window = tk.Toplevel(self.root)
        record_window.title("Enregistrement de la touche")
        record_window.geometry("450x200")
        record_window.configure(bg='#1e1e1e')
        record_window.transient(self.root)
        record_window.grab_set()

        # Centrer la fenêtre
        record_window.update_idletasks()
        x = (record_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (record_window.winfo_screenheight() // 2) - (200 // 2)
        record_window.geometry(f"450x200+{x}+{y}")

        frame = tk.Frame(record_window, bg='#1e1e1e', padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame, text="⌨️ Pressez la combinaison de touches souhaitée",
            bg='#1e1e1e', fg='#61dafb', font=('Segoe UI', 12, 'bold')
        ).pack(pady=(0, 10))

        tk.Label(
            frame, text="Exemples: Ctrl+Shift+T, Alt+F1, Ctrl+G",
            bg='#1e1e1e', fg='#888888', font=('Segoe UI', 9)
        ).pack(pady=(0, 20))

        self.current_keys_label = tk.Label(
            frame, text="En attente...",
            bg='#2d2d2d', fg='#ffffff', font=('Segoe UI', 14, 'bold'),
            padx=20, pady=15, relief=tk.SOLID, borderwidth=1
        )
        self.current_keys_label.pack(pady=(0, 20))

        tk.Button(
            frame, text="❌ Annuler",
            command=record_window.destroy,
            bg='#404040', fg='#ffffff', font=('Segoe UI', 10),
            cursor='hand2', relief=tk.FLAT, padx=15, pady=5
        ).pack()

        # Variables pour la détection
        self.pressed_keys = set()
        self.temp_hotkey = None

        def on_key_event(event):
            """Détecte les touches pressées"""
            if event.event_type == 'down':
                # Normaliser le nom de la touche
                key_name = event.name.lower()

                # Mapper les touches spéciales
                key_map = {
                    'control': 'ctrl',
                    'left ctrl': 'ctrl',
                    'right ctrl': 'ctrl',
                    'left shift': 'shift',
                    'right shift': 'shift',
                    'left alt': 'alt',
                    'right alt': 'alt',
                    'left windows': 'win',
                    'right windows': 'win'
                }

                key_name = key_map.get(key_name, key_name)
                self.pressed_keys.add(key_name)

                # Afficher les touches actuelles
                display = '+'.join(sorted(self.pressed_keys, key=lambda x: (
                    0 if x == 'ctrl' else 1 if x == 'shift' else 2 if x == 'alt' else 3
                )))
                self.current_keys_label.config(text=display or "En attente...")

            elif event.event_type == 'up':
                # Quand on relâche les touches, enregistrer la combinaison
                if len(self.pressed_keys) >= 1:  # Au moins une touche
                    # Créer la hotkey au format keyboard
                    hotkey = '+'.join(sorted(self.pressed_keys, key=lambda x: (
                        0 if x == 'ctrl' else 1 if x == 'shift' else 2 if x == 'alt' else 3
                    )))

                    self.temp_hotkey = hotkey
                    keyboard.unhook_all()
                    record_window.destroy()
                    self.apply_hotkey()

        # Hook toutes les touches
        keyboard.hook(on_key_event)

        # Attendre la fermeture de la fenêtre
        record_window.protocol("WM_DELETE_WINDOW", lambda: [keyboard.unhook_all(), record_window.destroy()])

    def apply_hotkey(self):
        """Applique la hotkey enregistrée"""
        if self.temp_hotkey and self.recording_key:
            if self.recording_key == 'hotkey':
                self.hotkey_entry.config(state='normal')
                self.hotkey_entry.delete(0, tk.END)
                self.hotkey_entry.insert(0, self.temp_hotkey)
                self.hotkey_entry.config(state='readonly')
            elif self.recording_key == 'toggle_mode_hotkey':
                self.toggle_entry.config(state='normal')
                self.toggle_entry.delete(0, tk.END)
                self.toggle_entry.insert(0, self.temp_hotkey)
                self.toggle_entry.config(state='readonly')

            self.temp_hotkey = None
            self.recording_key = None

    def save_and_close(self):
        """Sauvegarde la configuration et ferme la fenêtre"""
        # Récupérer toutes les valeurs
        self.config['hotkey'] = self.hotkey_entry.get()
        self.config['toggle_mode_hotkey'] = self.toggle_entry.get()
        self.config['translation_mode'] = self.mode_combo.get()
        self.config['source_lang'] = self.source_combo.get()
        self.config['target_lang'] = self.target_combo.get()
        self.config['auto_detect_language'] = self.auto_detect_var.get()
        self.config['overlay_timeout'] = int(self.timeout_spin.get())
        self.config['ollama_url'] = self.ollama_url_entry.get()
        self.config['ollama_model'] = self.llm_entry.get()
        self.config['vision_model'] = self.vision_entry.get()

        # Sauvegarder
        if self.save_config():
            messagebox.showinfo(
                "✅ Succès",
                "Configuration sauvegardée avec succès!\n\nRedémarrez Game Translator pour appliquer les changements."
            )
            self.root.quit()

    def run(self):
        """Lance l'interface"""
        self.root.mainloop()


def main():
    """Point d'entrée"""
    app = ConfigGUI()
    app.run()


if __name__ == '__main__':
    main()
