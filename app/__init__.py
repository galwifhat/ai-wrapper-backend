# app/__init__.py
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Configure CORS
    CORS(
        app,
        origins=[
            "http://localhost:5173",
            "http://127.0.0.1:3006",
            "https://api-wrapper.mlbyte.space",
            "http://152.53.48.110:3006",
            "https://ai-wrapper-frontend-fc667js9u-galwifhat.vercel.app/",
        ],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
    )

    # Register blueprints
    from app.api.v1.ai import ai_bp

    app.register_blueprint(ai_bp, url_prefix="/api/v1/ai")

    return app
