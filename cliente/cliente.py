import requests

class ArcadeClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    # Métodos para puntuaciones
    def get_top_scores(self, game_name=None, limit=10):
        """Obtiene las mejores puntuaciones para un juego específico o todos los juegos"""
        endpoint = f"{self.base_url}/scores/"
        params = {}
        if game_name:
            params['game'] = game_name
        if limit:
            params['limit'] = limit
            
        response = self.session.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def save_score(self, player_name, game_name, score):
        """Guarda una nueva puntuación en el servidor"""
        endpoint = f"{self.base_url}/scores/"
        data = {
            "player_name": player_name,
            "game_name": game_name,
            "score": score
        }
        response = self.session.post(endpoint, json=data)
        return response.status_code == 201
    
    # Métodos para sesiones de juego
    def start_game_session(self, game_name, player_name="Anonymous"):
        """Inicia una nueva sesión de juego en el servidor"""
        endpoint = f"{self.base_url}/games/start"
        data = {
            "game_name": game_name,
            "player_name": player_name
        }
        response = self.session.post(endpoint, json=data)
        if response.status_code == 201:
            return response.json()
        return None
    
    def end_game_session(self, session_id):
        """Finaliza una sesión de juego en el servidor"""
        endpoint = f"{self.base_url}/games/end/{session_id}"
        response = self.session.put(endpoint)
        if response.status_code == 200:
            return response.json()
        return None