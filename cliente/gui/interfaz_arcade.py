import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys

# Asegúrate de que puedas importar los módulos necesarios
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from cliente.gui.pantalla_juegos import GameScreen
from cliente.gui.pantalla_puntuaciones import ScoreboardScreen
from cliente.cliente import ArcadeClient
from juegos.n_reinas import QueensGame
from juegos.recorrido_del_caballo import KnightTourGame
from juegos.torres_de_hanoi import HanoiGame

class ArcadeInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Arcade Games Machine")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Inicializar cliente HTTP
        self.client = ArcadeClient()
        
        # Variables para seguimiento
        self.current_player = tk.StringVar(value="Jugador")
        self.current_game = None
        self.game_session_id = None
        
        # Crear frames principales
        self.setup_frames()
        
        # Mostrar pantalla de inicio
        self.show_main_menu()
    
    def setup_frames(self):
        """Configura los frames principales de la aplicación"""
        # Frame principal que contiene todo
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para la cabecera con información del jugador
        self.header_frame = tk.Frame(self.main_frame, bg="#333")
        self.header_frame.pack(fill=tk.X)
        
        # Etiqueta para el nombre del jugador
        self.player_label = tk.Label(
            self.header_frame, 
            textvariable=self.current_player,
            font=("Arial", 12, "bold"),
            bg="#333", fg="white",
            padx=10, pady=5
        )
        self.player_label.pack(side=tk.LEFT)
        
        # Botón para cambiar el nombre del jugador
        self.change_name_btn = tk.Button(
            self.header_frame,
            text="Cambiar Nombre",
            command=self.change_player_name
        )
        self.change_name_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón para ver puntuaciones
        self.scores_btn = tk.Button(
            self.header_frame,
            text="Puntuaciones",
            command=self.show_scoreboard
        )
        self.scores_btn.pack(side=tk.RIGHT, padx=10)
        
        # Frame para el contenido principal (cambia según la pantalla)
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def clear_content(self):
        """Limpia el frame de contenido para mostrar una nueva pantalla"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Muestra el menú principal con los juegos disponibles"""
        self.clear_content()
        
        # Título principal
        title_label = tk.Label(
            self.content_frame,
            text="ARCADE GAMES",
            font=("Arial", 24, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Frame para la cuadrícula de juegos
        games_frame = tk.Frame(self.content_frame)
        games_frame.pack(pady=30)
        
        # Definir los juegos disponibles
        games = [
            {
                "name": "N-Reinas",
                "description": "Coloca N reinas en un tablero sin que se amenacen",
                "command": lambda: self.start_game("n_reinas")
            },
            {
                "name": "Recorrido del Caballo",
                "description": "Haz que el caballo recorra todo el tablero",
                "command": lambda: self.start_game("recorrido_del_caballo")
            },
            {
                "name": "Torres de Hanói",
                "description": "Mueve la torre completa a otro poste",
                "command": lambda: self.start_game("torres_de_hanoi")
            }
        ]
        
        # Crear botones para cada juego
        for i, game in enumerate(games):
            game_frame = tk.Frame(games_frame, bd=2, relief=tk.RAISED, padx=10, pady=10)
            game_frame.grid(row=i//2, column=i%2, padx=20, pady=20)
            
            name_label = tk.Label(
                game_frame,
                text=game["name"],
                font=("Arial", 14, "bold")
            )
            name_label.pack(pady=5)
            
            desc_label = tk.Label(
                game_frame,
                text=game["description"],
                wraplength=200
            )
            desc_label.pack(pady=5)
            
            play_btn = tk.Button(
                game_frame,
                text="JUGAR",
                font=("Arial", 12),
                command=game["command"],
                width=15
            )
            play_btn.pack(pady=10)
    
    def change_player_name(self):
        """Permite al usuario cambiar su nombre"""
        new_name = simpledialog.askstring(
            "Cambiar Nombre",
            "Introduce tu nombre:",
            initialvalue=self.current_player.get()
        )
        
        if new_name and new_name.strip():
            self.current_player.set(new_name.strip())
    
    def start_game(self, game_type):
        """Inicia un juego específico"""
        # Registrar el inicio del juego en el servidor
        response = self.client.start_game_session(
            game_name=game_type,
            player_name=self.current_player.get()
        )
        
        if response:
            self.game_session_id = response.get('id')
        
        # Crear instancia del juego según el tipo
        if game_type == "n_reinas":
            self.current_game = QueensGame()
            game_title = "N-Reinas"
        elif game_type == "recorrido_del_caballo":
            self.current_game = KnightTourGame()
            game_title = "Recorrido del Caballo"
        elif game_type == "torres_De_hanoi":
            self.current_game = HanoiGame()
            game_title = "Torres de Hanói"
        else:
            messagebox.showerror("Error", "Juego no reconocido")
            return
        
        # Mostrar la pantalla del juego
        self.clear_content()
        game_screen = GameScreen(
            self.content_frame,
            self.current_game,
            game_type,
            game_title,
            self.end_game
        )
        game_screen.pack(fill=tk.BOTH, expand=True)
    
    def end_game(self, game_type, score):
        """Finaliza el juego actual y guarda la puntuación"""
        # Finalizar la sesión en el servidor
        if self.game_session_id:
            self.client.end_game_session(self.game_session_id)
            self.game_session_id = None
        
        # Guardar puntuación
        self.client.save_score(
            player_name=self.current_player.get(),
            game_name=game_type,
            score=score
        )
        
        # Mostrar mensaje con la puntuación
        messagebox.showinfo(
            "Fin del Juego",
            f"¡Juego terminado!\nTu puntuación: {score}"
        )
        
        # Volver al menú principal
        self.show_main_menu()
    
    def show_scoreboard(self):
        """Muestra la pantalla de puntuaciones"""
        self.clear_content()
        scoreboard = ScoreboardScreen(
            self.content_frame,
            self.client,
            back_command=self.show_main_menu
        )
        scoreboard.pack(fill=tk.BOTH, expand=True)