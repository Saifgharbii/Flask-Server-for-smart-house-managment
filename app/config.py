import os
from typing import Dict, Type

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