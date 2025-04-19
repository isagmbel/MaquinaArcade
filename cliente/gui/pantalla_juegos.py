import tkinter as tk
from tkinter import ttk

class GameScreen(tk.Frame):
    def __init__(self, parent, game_instance, game_type, game_title, end_game_callback):
        super().__init__(parent)
        self.parent = parent
        self.game = game_instance
        self.game_type = game_type
        self.game_title = game_title
        self.end_game_callback = end_game_callback
        
        # Variables de control
        self.score = 0
        
        # Configurar la interfaz del juego
        self.setup_ui()
        
        # Inicializar el juego
        self.start_game()
    
    def setup_ui(self):
        """Configura la interfaz básica del juego"""
        # Frame superior con título y puntuación
        self.header_frame = tk.Frame(self)
        self.header_frame.pack(fill=tk.X, pady=10)
        
        # Título del juego
        self.title_label = tk.Label(
            self.header_frame,
            text=self.game_title,
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=20)
        
        # Puntuación actual
        self.score_frame = tk.Frame(self.header_frame)
        self.score_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(
            self.score_frame,
            text="Puntuación:",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)
        
        self.score_label = tk.Label(
            self.score_frame,
            text="0",
            font=("Arial", 12, "bold")
        )
        self.score_label.pack(side=tk.LEFT, padx=5)
        
        # Frame para los controles específicos del juego
        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(fill=tk.X, pady=5)
        
        # Frame para el área de juego (este se personalizará en las subclases)
        self.game_area = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.game_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Botón para terminar el juego
        self.end_button = tk.Button(
            self,
            text="Terminar Juego",
            command=self.end_game
        )
        self.end_button.pack(pady=10)
    
    def update_score(self, new_score):
        """Actualiza la puntuación mostrada"""
        self.score = new_score
        self.score_label.config(text=str(new_score))
    
    def start_game(self):
        """Inicializa el juego - a ser implementado por las subclases"""
        pass
    
    def end_game(self):
        """Finaliza el juego actual y vuelve al menú principal"""
        self.end_game_callback(self.game_type, self.score)