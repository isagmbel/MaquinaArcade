from servidor.modelos.modelo import Score
from servidor.db.database import db

class ScoreManager:
    @staticmethod
    def add_score(player_name, game_name, score_value):
        """Agrega una nueva puntuación"""
        score = Score(
            player_name=player_name,
            game_name=game_name,
            score=score_value
        )
        db.session.add(score)
        db.session.commit()
        return score

    @staticmethod
    def get_top_scores(game_name=None, limit=10):
        """Obtiene las mejores puntuaciones, filtradas por juego si se especifica"""
        query = Score.query
        if game_name:
            query = query.filter_by(game_name=game_name)
        return query.order_by(Score.score.desc()).limit(limit).all()

    @staticmethod
    def delete_score(score_id):
        """Elimina una puntuación por su ID"""
        score = Score.query.get(score_id)
        if score:
            db.session.delete(score)
            db.session.commit()
            return True
        return False