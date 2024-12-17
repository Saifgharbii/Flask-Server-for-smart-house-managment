from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from app.controller.arduino_controler import *
from app.controller.GHI_AI_model import ghi_fun
import os
import threading
from typing import Dict, Type
from datetime import datetime
import json



arduino_thread = None
thread_lock = threading.Lock()
socketio = SocketIO()


def background_thread():
    """Background thread that reads data from Arduino."""
    while True:
        data= ArduinoController.read_from_arduino()
        if isinstance(data, str):
            data_dict = json.loads(data)
        else:
            data_dict = data.copy()
        data_dict['timestamp'] = datetime.now().isoformat()
        socketio.emit('arduino_data', {'data': data_dict})
        

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my-secret-key')
    DEBUG = False
    TESTING = False
    FIREBASE_CREDENTIALS_PATH = os.getenv(
        'FIREBASE_CREDENTIALS_PATH',
        './firebase-credentials.json'
    )

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    FIREBASE_CREDENTIALS_PATH = './tests/firebase-credentials-test.json'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, ensure to set a strong secret key
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Ensure the Firebase credentials path is set in environment
    FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')

config_by_name: Dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from .api.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # SocketIO event handlers
    @socketio.on('connect')
    def handle_connect():
        global arduino_thread
        with thread_lock:
            if arduino_thread is None:
                arduino_thread = threading.Thread(target=background_thread)
                arduino_thread.daemon = True
                arduino_thread.start()
        print('Client connected')
        
    @socketio.on("command")
    def send_command(data):
        print(type(data))
        ArduinoController.send_to_arduino(data)
    @socketio.on("forcast")
    def send_forcast():
        return ghi_fun.main()
        
        
        
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
    
    return app