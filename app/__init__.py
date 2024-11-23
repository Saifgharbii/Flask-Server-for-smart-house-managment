from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .db_init import init_firebase

def create_app(config_name: str = 'development') -> Flask:
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load config based on environment
    app.config.from_object(config_by_name[config_name])
    
    # Initialize CORS
    CORS(app)
    
    # Initialize Firebase
    init_firebase(app)
    
    # Register blueprints here
    from .controllers.user_controller import user_bp
    from .controllers.device_controller import device_bp
    from .controllers.room_controller import room_bp
    from .controllers.house_controller import house_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(device_bp, url_prefix='/api/devices')
    app.register_blueprint(room_bp, url_prefix='/api/rooms')
    app.register_blueprint(house_bp, url_prefix='/api/houses')
    
    return app
