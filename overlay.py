"""
Module pour l'affichage de l'overlay de traduction
"""
import tkinter as tk
from tkinter import scrolledtext
import threading


class TranslationOverlay:
    """Fenêtre overlay pour afficher les traductions"""
    
    def __init__(self, x, y, width=400, height=200):
        """
        Initialise l'overlay
        
        Args:
            x, y: Position de l'overlay
            width, height: Dimensions de l'overlay
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.root = None
        self.text_widget = None
        self.close_timer = None
    
    def show(self, original_text, translated_text, auto_close=True, timeout=30):
        """
        Affiche l'overlay avec le texte traduit
        
        Args:
            original_text: Texte original
            translated_text: Texte traduit
            auto_close: Si True, ferme automatiquement après timeout secondes
            timeout: Délai avant fermeture automatique (secondes)
        """
        self.root = tk.Tk()
        self.root.title("Game Translator")
        
        # Configuration de la fenêtre
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-alpha', 0.95)  # Légèrement transparent
        self.root.configure(bg='#1e1e1e')
        
        # Empêcher le redimensionnement
        self.root.resizable(False, False)
        
        # Frame principal avec padding
        main_frame = tk.Frame(self.root, bg='#1e1e1e', padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = tk.Label(
            main_frame,
            text="🎮 Game Translator",
            font=('Segoe UI', 12, 'bold'),
            fg='#61dafb',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(0, 5))
        
        # Séparateur
        separator = tk.Frame(main_frame, height=2, bg='#61dafb')
        separator.pack(fill=tk.X, pady=5)
        
        # Texte original (optionnel, commenté par défaut pour gagner de l'espace)
        if len(original_text) < 100:  # Afficher seulement si court
            original_label = tk.Label(
                main_frame,
                text=f"Original: {original_text}",
                font=('Segoe UI', 9),
                fg='#888888',
                bg='#1e1e1e',
                wraplength=self.width - 40,
                justify=tk.LEFT
            )
            original_label.pack(pady=(0, 5))
        
        # Zone de texte traduit avec scrollbar
        text_frame = tk.Frame(main_frame, bg='#1e1e1e')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = scrolledtext.ScrolledText(
            text_frame,
            font=('Segoe UI', 11),
            fg='#ffffff',
            bg='#2d2d2d',
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            insertbackground='white',
            selectbackground='#61dafb',
            selectforeground='#1e1e1e'
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.insert('1.0', translated_text)
        self.text_widget.configure(state='disabled')  # Read-only
        
        # Bouton de fermeture
        close_button = tk.Button(
            main_frame,
            text="✕ Fermer (ou cliquez n'importe où)",
            command=self.close,
            font=('Segoe UI', 9),
            fg='#ffffff',
            bg='#404040',
            activebackground='#505050',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            padx=10,
            pady=5
        )
        close_button.pack(pady=(5, 0))
        
        # Fermer sur clic n'importe où
        self.root.bind('<Button-1>', lambda e: self.close())
        self.text_widget.bind('<Button-1>', lambda e: self.close())
        
        # Fermer sur Échap
        self.root.bind('<Escape>', lambda e: self.close())
        
        # Copier dans le presse-papiers sur Ctrl+C
        self.root.bind('<Control-c>', lambda e: self._copy_to_clipboard(translated_text))
        
        # Timer de fermeture automatique
        if auto_close:
            self.close_timer = self.root.after(timeout * 1000, self.close)
            
            # Afficher le compte à rebours
            countdown_label = tk.Label(
                main_frame,
                text=f"Fermeture auto dans {timeout}s",
                font=('Segoe UI', 8),
                fg='#888888',
                bg='#1e1e1e'
            )
            countdown_label.pack(pady=(5, 0))
            
            self._update_countdown(countdown_label, timeout)
        
        # Centrer la fenêtre si les coordonnées sont à 0
        if self.x == 0 and self.y == 0:
            self.root.update_idletasks()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - self.width) // 2
            y = (screen_height - self.height) // 2
            self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        print("✅ Overlay affiché")
        self.root.mainloop()
    
    def _update_countdown(self, label, remaining):
        """Met à jour le compte à rebours"""
        if remaining > 0 and self.root:
            label.config(text=f"Fermeture auto dans {remaining}s")
            self.root.after(1000, lambda: self._update_countdown(label, remaining - 1))
    
    def _copy_to_clipboard(self, text):
        """Copie le texte dans le presse-papiers"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        print("📋 Texte copié dans le presse-papiers")
    
    def close(self):
        """Ferme l'overlay"""
        if self.root:
            if self.close_timer:
                self.root.after_cancel(self.close_timer)
            self.root.quit()
            self.root.destroy()
            self.root = None
            print("✅ Overlay fermé")
    
    def update_text(self, text):
        """
        Met à jour le texte affiché (utile pour le streaming)
        
        Args:
            text: Nouveau texte à afficher
        """
        if self.text_widget and self.root:
            self.text_widget.configure(state='normal')
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert('1.0', text)
            self.text_widget.configure(state='disabled')
            self.root.update()


def show_overlay_threaded(x, y, original_text, translated_text, width=400, height=200):
    """
    Affiche l'overlay dans un thread séparé
    
    Args:
        x, y: Position de l'overlay
        original_text: Texte original
        translated_text: Texte traduit
        width, height: Dimensions de l'overlay
    """
    overlay = TranslationOverlay(x, y, width, height)
    overlay.show(original_text, translated_text)


def show_error_overlay(error_message):
    """
    Affiche un overlay d'erreur
    
    Args:
        error_message: Message d'erreur à afficher
    """
    overlay = TranslationOverlay(0, 0, 400, 150)
    overlay.show(
        "Erreur",
        f"❌ {error_message}",
        auto_close=True,
        timeout=5
    )
