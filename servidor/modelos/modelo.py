from datetime import datetime
from servidor.db.database import db

class Score(db.Model):
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(50), nullable=False)
    game_name = db.Column(db.String(50), nullable=False)  # 'queens', 'knight', 'hanoi'
    score = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'player_name': self.player_name,
            'game_name': self.game_name,
            'score': self.score,
            'date_created': self.date_created.isoformat()
        }

class GameSession(db.Model):
    __tablename__ = 'game_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False)
    player_name = db.Column(db.String(50), nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'game_name': self.game_name,
            'player_name': self.player_name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_active': self.is_active
        }