# app/api/v1/ai.py
import os
from flask import Blueprint, request, Response, stream_with_context
from app.services.openrouter.stream import stream_chat_completion

ai_bp = Blueprint("ai", __name__)

SYSTEM_INSTRUCTIONS = {
    "role": "system",
    "content": os.getenv("AI_SYSTEM_INSTRUCTIONS", "You are a helpful AI assistant."),
}


@ai_bp.route("/stream", methods=["POST"])
def stream():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return {"error": "No messages provided"}, 400

    messages = [SYSTEM_INSTRUCTIONS] + messages

    def generate():
        for chunk in stream_chat_completion(messages):
            yield chunk

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",  # Change from text/plain
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
