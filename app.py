from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

@app.route("/", methods=["GET"])
def home():
    return "✅ ReadWise Chatbot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Try to extract genre, mood, and age from Watson Assistant context
    genre = mood = age = None
    try:
        user_defined = data['context']['skills']['main skill']['user_defined']
        genre = user_defined.get('genre')
        mood = user_defined.get('mood')
        age = user_defined.get('age')
    except Exception:
        pass

    if genre or mood or age:
        books = get_books_recommendation(genre, mood, age)
        response_text = f"Here are some books based on your preferences:\n{books}"
    else:
        response_text = (
            "Please tell me your preferences! You can mention a genre (e.g., mystery), "
            "a mood (e.g., uplifting), or an age group (e.g., teens)."
        )

    return jsonify({
        "output": {
            "generic": [
                {
                    "response_type": "text",
                    "text": response_text
                }
            ]
        }
    })

def get_books_recommendation(genre=None, mood=None, age=None):
    # Build the search query using any available filters
    query_parts = []
    if genre:
        query_parts.append(f"subject:{genre}")
    if mood:
        query_parts.append(mood)
    if age:
        query_parts.append(age)

    query = " ".join(query_parts) or "books"

    params = {
        "q": query,
        "maxResults": 5,
        "printType": "books",
        "langRestrict": "en"
    }

    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        items = response.json().get("items", [])
        if not items:
            return "😕 Sorry, I couldn't find any matching books."

        book_list = []
        for item in items:
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title", "Unknown Title")
            authors = ", ".join(volume_info.get("authors", ["Unknown Author"]))
            book_list.append(f"📘 {title} by {authors}")

        return "\n".join(book_list)
    except Exception:
        return "❌ Oops! Something went wrong while fetching books."

if __name__ == "__main__":
    app.run(debug=True)
