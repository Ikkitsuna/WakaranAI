"""
Module pour capturer une zone de l'écran sélectionnée par l'utilisateur
"""
import tkinter as tk
from PIL import Image, ImageGrab
import mss


class ScreenshotSelector:
    """Permet à l'utilisateur de sélectionner une zone de l'écran"""
    
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.root = None
        self.canvas = None
        
    def on_mouse_down(self, event):
        """Début de la sélection"""
        self.start_x = event.x
        self.start_y = event.y
        
        # Supprimer l'ancien rectangle s'il existe
        if self.rect:
            self.canvas.delete(self.rect)
    
    def on_mouse_move(self, event):
        """Mise à jour du rectangle pendant le drag"""
        if self.start_x is not None and self.start_y is not None:
            # Supprimer l'ancien rectangle
            if self.rect:
                self.canvas.delete(self.rect)
            
            # Dessiner le nouveau rectangle
            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='red', width=3
            )
    
    def on_mouse_up(self, event):
        """Fin de la sélection"""
        self.end_x = event.x
        self.end_y = event.y
        self.root.quit()
    
    def select_area(self):
        """
        Affiche une fenêtre en plein écran pour sélectionner une zone
        Retourne les coordonnées (x1, y1, x2, y2) ou None si annulé
        """
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # Semi-transparent
        self.root.attributes('-topmost', True)
        
        # Forcer l'affichage du curseur même si le jeu le capture
        self.root.config(cursor='crosshair')
        self.root.focus_force()
        self.root.grab_set()  # Capture tous les événements souris
        
        # Canvas pour dessiner le rectangle
        self.canvas = tk.Canvas(
            self.root,
            cursor='crosshair',  # Curseur en croix bien visible
            bg='gray',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Forcer le focus sur le canvas pour capturer la souris
        self.canvas.focus_set()
        
        # Instructions
        label = tk.Label(
            self.canvas,
            text="Dessinez un rectangle sur la zone à traduire\nAppuyez sur Échap pour annuler",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='black'
        )
        label.place(relx=0.5, rely=0.05, anchor='center')
        
        # Bind des événements souris
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        self.root.mainloop()
        
        # Nettoyer
        self.root.destroy()
        
        # Vérifier si une zone a été sélectionnée
        if (self.start_x is not None and self.start_y is not None and 
            self.end_x is not None and self.end_y is not None):
            # Normaliser les coordonnées (au cas où l'utilisateur dessine de droite à gauche)
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)
            
            # Vérifier que la zone n'est pas trop petite
            if (x2 - x1) > 10 and (y2 - y1) > 10:
                return (x1, y1, x2, y2)
        
        return None


def capture_screen_area(bbox):
    """
    Capture une zone spécifique de l'écran
    
    Args:
        bbox: Tuple (x1, y1, x2, y2) des coordonnées de la zone
        
    Returns:
        PIL.Image ou None si erreur
    """
    try:
        # Utiliser mss pour une capture plus performante
        with mss.mss() as sct:
            monitor = {
                "top": bbox[1],
                "left": bbox[0],
                "width": bbox[2] - bbox[0],
                "height": bbox[3] - bbox[1]
            }
            
            # Capturer la zone
            screenshot = sct.grab(monitor)
            
            # Convertir en PIL Image
            img = Image.frombytes(
                'RGB',
                (screenshot.width, screenshot.height),
                screenshot.rgb
            )
            
            return img
    except Exception as e:
        print(f"❌ Erreur lors de la capture d'écran: {e}")
        return None


def capture_with_selection():
    """
    Workflow complet: sélection + capture
    
    Returns:
        tuple (PIL.Image, bbox) ou (None, None) si erreur/annulation
    """
    print("📸 Mode sélection activé...")
    
    selector = ScreenshotSelector()
    bbox = selector.select_area()
    
    if bbox is None:
        print("⚠️ Sélection annulée")
        return None, None
    
    print(f"✅ Zone sélectionnée: {bbox}")
    
    img = capture_screen_area(bbox)
    
    if img:
        print(f"✅ Image capturée: {img.size[0]}x{img.size[1]} pixels")
        return img, bbox
    
    return None, None
