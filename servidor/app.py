from flask import Flask
from servidor.rutas.rutas_juego import game_bp
from servidor.rutas.rutas_puntuacion import score_bp
from servidor.db.database import init_db

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Cargar configuración
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar la base de datos
    init_db(app)
    
    # Registrar blueprints
    app.register_blueprint(game_bp, url_prefix='/api/games')
    app.register_blueprint(score_bp, url_prefix='/api/scores')
    
    @app.route('/')
    def index():
        return {"message": "Arcade Games API", "status": "online"}
    
    return app
