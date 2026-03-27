# app/__init__.py
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Configure CORS
    CORS(
        app,
        origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
    )

    # Register blueprints
    from app.api.v1.ai import ai_bp

    app.register_blueprint(ai_bp, url_prefix="/api/v1/ai")

    return app
