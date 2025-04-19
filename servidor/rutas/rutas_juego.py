from flask import Blueprint, request, jsonify
from servidor.db.database import db
from servidor.modelos.modelo import GameSession

game_bp = Blueprint('games', __name__)

@game_bp.route('/start', methods=['POST'])
def start_game():
    data = request.json
    
    if not data or 'game_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Crear una nueva sesión de juego
    new_session = GameSession(
        game_name=data['game_name'],
        player_name=data.get('player_name', 'Anonymous')
    )
    
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify(new_session.to_dict()), 201

@game_bp.route('/end/<int:session_id>', methods=['PUT'])
def end_game(session_id):
    session = GameSession.query.get_or_404(session_id)
    
    from datetime import datetime
    session.end_time = datetime.utcnow()
    session.is_active = False
    
    db.session.commit()
    
    return jsonify(session.to_dict())

@game_bp.route('/active', methods=['GET'])
def get_active_games():
    active_sessions = GameSession.query.filter_by(is_active=True).all()
    return jsonify([session.to_dict() for session in active_sessions])