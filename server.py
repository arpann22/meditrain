from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    system = data.get("system", "")
    messages = data.get("messages", [])

    if not system or not messages:
        return jsonify({"error": "Missing system or messages"}), 400

    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY not set in .env"}), 500

    # Call Groq API
    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "max_tokens": 300,
            "messages": [
                {"role": "system", "content": system},
                *messages
            ]
        }
    )

    if not response.ok:
        print("Groq error:", response.text)
        return jsonify({"error": "Groq API failed", "detail": response.text}), 500

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)