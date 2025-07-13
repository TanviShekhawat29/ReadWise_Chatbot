from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Optional: allows cross-origin requests if you're testing from other sources

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    query = data.get('query') or data.get('input')  # handle different Watson formats
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    return jsonify({"response": f"Received: {query}"})
