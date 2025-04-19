from servidor.modelos.modelo import GameSession
from servidor.db.database import db
from datetime import datetime

class GameManager:
    @staticmethod
    def start_game_session(game_name, player_name='Anonymous'):
        """Inicia una nueva sesión de juego"""
        session = GameSession(
            game_name=game_name,
            player_name=player_name,
            is_active=True
        )
        db.session.add(session)
        db.session.commit()
        return session

    @staticmethod
    def end_game_session(session_id):
        """Finaliza una sesión de juego existente"""
        session = GameSession.query.get(session_id)
        if session and session.is_active:
            session.is_active = False
            session.end_time = datetime.utcnow()
            db.session.commit()
            return session
        return None

    @staticmethod
    def get_active_sessions():
        """Obtiene todas las sesiones activas"""
        return GameSession.query.filter_by(is_active=True).all()