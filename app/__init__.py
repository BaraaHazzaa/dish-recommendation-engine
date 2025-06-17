# app/__init__.py

from flask import Flask
from flask_cors import CORS
from .routes import main as main_blueprint
from config.config import Config
from .services import initialize_models
import logging

def create_app():
    """Factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, supports_credentials=True)
    
    # Configure Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Flask application initialized.")
    
    # Register Blueprints
    app.register_blueprint(main_blueprint)
    
    # Initialize Models
    initialize_models()
    
    return app
