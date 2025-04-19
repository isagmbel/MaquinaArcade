from flask import Blueprint, request, jsonify
from servidor.db.database import db
from servidor.modelos.modelo import Score

score_bp = Blueprint('scores', __name__)

@score_bp.route('/', methods=['GET'])
def get_all_scores():
    game_name = request.args.get('game', None)
    limit = request.args.get('limit', 10, type=int)
    
    query = Score.query
    
    if game_name:
        query = query.filter_by(game_name=game_name)
    
    scores = query.order_by(Score.score.desc()).limit(limit).all()
    return jsonify([score.to_dict() for score in scores])

@score_bp.route('/<game_name>', methods=['GET'])
def get_game_scores(game_name):
    limit = request.args.get('limit', 10, type=int)
    scores = Score.query.filter_by(game_name=game_name).order_by(Score.score.desc()).limit(limit).all()
    return jsonify([score.to_dict() for score in scores])

@score_bp.route('/', methods=['POST'])
def add_score():
    data = request.json
    
    if not data or 'player_name' not in data or 'game_name' not in data or 'score' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_score = Score(
        player_name=data['player_name'],
        game_name=data['game_name'],
        score=data['score']
    )
    
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify(new_score.to_dict()), 201

@score_bp.route('/<int:score_id>', methods=['DELETE'])
def delete_score(score_id):
    score = Score.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    return jsonify({'message': 'Score deleted successfully'}), 200