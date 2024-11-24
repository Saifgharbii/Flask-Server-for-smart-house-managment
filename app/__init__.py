from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Config

socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app