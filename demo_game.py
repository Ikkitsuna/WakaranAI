"""
Script de démonstration pour tester Game Translator sans jeu
Crée une fenêtre avec du texte en anglais pour tester l'OCR + traduction
"""
import tkinter as tk
from tkinter import font as tkfont


class DemoGameWindow:
    """Fenêtre de démo simulant un jeu avec du texte en anglais"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Demo Game - Test Game Translator")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Titre
        title = tk.Label(
            self.root,
            text="🎮 Demo Game Window",
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Press F9 to activate Game Translator, then draw a rectangle around any text below",
            font=('Arial', 12),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        instructions.pack(pady=10)
        
        # Zone 1: Dialog
        self._create_dialog_box(
            "Quest Giver",
            "Greetings, brave adventurer! The ancient dragon has awakened in the mountains. "
            "Will you help us defeat this terrible beast and save our village?"
        )
        
        # Zone 2: Item description
        self._create_item_box(
            "Legendary Sword of Fire",
            "A mystical blade forged in dragon fire. +50 Attack, +30 Fire Damage. "
            "Special: Burning Slash - Deals massive fire damage to all enemies."
        )
        
        # Zone 3: Tutorial
        self._create_tutorial_box(
            "Combat Tutorial",
            "Press SPACE to attack\nPress SHIFT to dodge\nPress Q to use special ability\n"
            "Press E to open inventory"
        )
        
        # Zone 4: Menu
        self._create_menu_box()
        
        # Footer
        footer = tk.Label(
            self.root,
            text="This is a DEMO window. Launch main.py and test the translator on these texts!",
            font=('Arial', 10, 'italic'),
            fg='#7f8c8d',
            bg='#2c3e50'
        )
        footer.pack(side=tk.BOTTOM, pady=20)
    
    def _create_dialog_box(self, speaker, text):
        """Crée une boîte de dialogue"""
        frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        frame.pack(pady=10, padx=20, fill=tk.X)
        
        speaker_label = tk.Label(
            frame,
            text=speaker,
            font=('Arial', 14, 'bold'),
            fg='#f39c12',
            bg='#34495e'
        )
        speaker_label.pack(anchor=tk.W, padx=10, pady=5)
        
        text_label = tk.Label(
            frame,
            text=text,
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#34495e',
            wraplength=700,
            justify=tk.LEFT
        )
        text_label.pack(anchor=tk.W, padx=10, pady=10)
    
    def _create_item_box(self, name, description):
        """Crée une boîte d'item"""
        frame = tk.Frame(self.root, bg='#8e44ad', relief=tk.RAISED, borderwidth=2)
        frame.pack(pady=10, padx=20, fill=tk.X)
        
        name_label = tk.Label(
            frame,
            text=f"⚔️ {name}",
            font=('Arial', 13, 'bold'),
            fg='#ffffff',
            bg='#8e44ad'
        )
        name_label.pack(anchor=tk.W, padx=10, pady=5)
        
        desc_label = tk.Label(
            frame,
            text=description,
            font=('Arial', 10),
            fg='#ecf0f1',
            bg='#8e44ad',
            wraplength=700,
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, padx=10, pady=10)
    
    def _create_tutorial_box(self, title, text):
        """Crée une boîte de tutoriel"""
        frame = tk.Frame(self.root, bg='#16a085', relief=tk.RAISED, borderwidth=2)
        frame.pack(pady=10, padx=20, fill=tk.X)
        
        title_label = tk.Label(
            frame,
            text=f"📖 {title}",
            font=('Arial', 13, 'bold'),
            fg='#ffffff',
            bg='#16a085'
        )
        title_label.pack(anchor=tk.W, padx=10, pady=5)
        
        text_label = tk.Label(
            frame,
            text=text,
            font=('Courier New', 10),
            fg='#ecf0f1',
            bg='#16a085',
            justify=tk.LEFT
        )
        text_label.pack(anchor=tk.W, padx=10, pady=10)
    
    def _create_menu_box(self):
        """Crée un menu"""
        frame = tk.Frame(self.root, bg='#c0392b', relief=tk.RAISED, borderwidth=2)
        frame.pack(pady=10, padx=20, fill=tk.X)
        
        title = tk.Label(
            frame,
            text="📋 Main Menu",
            font=('Arial', 13, 'bold'),
            fg='#ffffff',
            bg='#c0392b'
        )
        title.pack(pady=5)
        
        menu_items = [
            "Continue Game",
            "New Game",
            "Load Game",
            "Settings",
            "Exit"
        ]
        
        for item in menu_items:
            label = tk.Label(
                frame,
                text=f"> {item}",
                font=('Arial', 11),
                fg='#ecf0f1',
                bg='#c0392b',
                cursor='hand2'
            )
            label.pack(anchor=tk.W, padx=20, pady=2)
    
    def run(self):
        """Lance la fenêtre"""
        print("🎮 Demo Game Window lancée")
        print("=" * 60)
        print("Instructions:")
        print("1. Laissez cette fenêtre ouverte")
        print("2. Dans un autre terminal, lancez: python main.py")
        print("3. Appuyez sur F9")
        print("4. Dessinez un rectangle autour d'un texte de cette fenêtre")
        print("5. Attendez la traduction!")
        print("=" * 60)
        self.root.mainloop()


if __name__ == '__main__':
    demo = DemoGameWindow()
    demo.run()
