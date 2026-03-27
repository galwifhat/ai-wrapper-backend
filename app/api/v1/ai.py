# app/api/v1/ai.py
from flask import Blueprint, request, Response, stream_with_context
from app.services.openrouter.stream import stream_chat_completion

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/stream", methods=["POST"])
def stream():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return {"error": "No messages provided"}, 400

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
