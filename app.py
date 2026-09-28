"""
app.py

Flask backend for the Digital Marketing FAQ Chatbot (AI/NLP Internship Task 2).

Exposes:
    GET  /                -> serves the chat UI (templates/index.html)
    POST /api/chat        -> accepts {"message": "..."} and returns
                              {"answer": "...", "category": "...", "similarity": 0.0}
    GET  /api/health       -> simple health-check endpoint

Run with:
    python app.py
"""

from flask import Flask, jsonify, render_template, request

from chatbot.matcher import FAQMatcher

app = Flask(__name__)

# The matcher loads the FAQ dataset and fits the TF-IDF vectorizer ONCE at
# startup, so every request just does a fast transform + similarity lookup
# instead of refitting the model every time.
matcher = FAQMatcher()


@app.route("/")
def index():
    """Serve the chatbot's frontend page."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok", "faqs_loaded": len(matcher.faqs)})


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chatbot endpoint.

    Expects JSON body: {"message": "<user question>"}
    Returns JSON body: {"answer": "...", "category": "...", "similarity": 0.0}
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Field 'message' is required and cannot be empty."}), 400

    if len(message) > 500:
        return jsonify({"error": "Message is too long. Please keep it under 500 characters."}), 400

    result = matcher.get_best_match(message)

    return jsonify(
        {
            "answer": result["answer"],
            "category": result["category"],
            "similarity": result["similarity"],
        }
    )


@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Not found."}), 404


@app.errorhandler(500)
def server_error(_e):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    # debug=True is convenient for local development; turn it off in production.
    app.run(debug=True, host="0.0.0.0", port=5000)
