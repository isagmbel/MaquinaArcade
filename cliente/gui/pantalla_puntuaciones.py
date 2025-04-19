import tkinter as tk
from tkinter import ttk

class ScoreboardScreen(tk.Frame):
    def __init__(self, parent, client, back_command):
        super().__init__(parent)
        self.parent = parent
        self.client = client
        self.back_command = back_command
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Cargar puntuaciones iniciales (todas)
        self.load_scores()
    
    def setup_ui(self):
        """Configura la interfaz de la pantalla de puntuaciones"""
        # Título
        title_label = tk.Label(
            self,
            text="TABLA DE PUNTUACIONES",
            font=("Arial", 18, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Selector de juego
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            filter_frame,
            text="Filtrar por juego:",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=10)
        
        self.game_filter = ttk.Combobox(
            filter_frame,
            values=["Todos", "N-Reinas", "Recorrido del Caballo", "Torres de Hanói"],
            state="readonly",
            width=20
        )
        self.game_filter.current(0)
        self.game_filter.pack(side=tk.LEFT, padx=5)
        self.game_filter.bind("<<ComboboxSelected>>", self.filter_changed)
        
        # Tabla de puntuaciones
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Crear Treeview para mostrar las puntuaciones
        columns = ("rank", "player", "game", "score", "date")
        self.scores_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Definir encabezados
        self.scores_table.heading("rank", text="#")
        self.scores_table.heading("player", text="Jugador")
        self.scores_table.heading("game", text="Juego")
        self.scores_table.heading("score", text="Puntuación")
        self.scores_table.heading("date", text="Fecha")
        
        # Definir anchos de columnas
        self.scores_table.column("rank", width=50)
        self.scores_table.column("player", width=150)
        self.scores_table.column("game", width=150)
        self.scores_table.column("score", width=100)
        self.scores_table.column("date", width=150)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.scores_table.yview)
        self.scores_table.configure(yscrollcommand=scrollbar.set)
        
        # Colocar elementos en la tabla
        self.scores_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón para volver
        back_button = tk.Button(
            self,
            text="Volver al Menú",
            command=self.back_command,
            width=15
        )
        back_button.pack(pady=10)
    
    def filter_changed(self, event):
        """Se ejecuta cuando el usuario cambia el filtro de juego"""
        self.load_scores()
    
    def load_scores(self):
        """Carga las puntuaciones desde el servidor con el filtro actual"""
        # Limpiar tabla actual
        for item in self.scores_table.get_children():
            self.scores_table.delete(item)
        
        # Determinar el juego a filtrar
        game_map = {
            "Todos": None,
            "N-Reinas": "queens",
            "Recorrido del Caballo": "knight",
            "Torres de Hanói": "hanoi"
        }
        
        selected_game = game_map.get(self.game_filter.get())
        
        # Obtener puntuaciones del servidor
        scores = self.client.get_top_scores(game_name=selected_game, limit=20)
        
        # Insertar en la tabla
        for i, score in enumerate(scores, 1):
            # Convertir nombre del juego a formato legible
            game_name_map = {
                "queens": "N-Reinas",
                "knight": "Recorrido del Caballo",
                "hanoi": "Torres de Hanói"
            }
            
            game_name = game_name_map.get(score["game_name"], score["game_name"])
            
            # Formatear fecha (solo mostrar fecha, no hora)
            date = score["date_created"].split("T")[0]
            
            self.scores_table.insert("", tk.END, values=(
                i,  # Ranking
                score["player_name"],
                game_name,
                score["score"],
                date
            ))