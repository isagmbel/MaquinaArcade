from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    # Crear todas las tablas si no existen
    with app.app_context():
        db.create_all()