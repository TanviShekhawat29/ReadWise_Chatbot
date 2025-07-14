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

    # Log incoming request for debugging
    print("🔥 Incoming request data:")
    print(data)

    # Extract user-defined context values from Watson
    genre = mood = age_group = None
    try:
        user_defined = data['context']['skills']['main skill']['user_defined']
        genre = user_defined.get('genre')
        mood = user_defined.get('mood')
        age_group = user_defined.get('age_group')  # ✅ fixed key
    except Exception as e:
        print("⚠️ Error extracting slot values:", e)

    # Get book recommendations if any input is present
    if genre or mood or age_group:
        books = get_books_recommendation(genre, mood, age_group)
        response_text = f"Here are some books based on your preferences:\n{books}"
    else:
        response_text = (
            "Please tell me your preferences! You can mention a genre (e.g., mystery), "
            "a mood (e.g., uplifting), or an age group (e.g., teens)."
        )

    # Return Watson-compatible JSON
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

def get_books_recommendation(genre=None, mood=None, age_group=None):
    # Build query string using available filters
    query_parts = []
    if genre:
        query_parts.append(f"subject:{genre}")
    if mood:
        query_parts.append(mood)
    if age_group:
        query_parts.append(age_group)

    query = " ".join(query_parts) or "books"
    print(f"🔍 Google Books Query: {query}")

    params = {
        "q": query,
        "maxResults": 5,
        "printType": "books",
        "langRestrict": "en"
    }

    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()
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
    except Exception as e:
        print("❌ Error fetching from Google Books API:", e)
        return "❌ Oops! Something went wrong while fetching books."

if __name__ == "__main__":
    app.run(debug=True)
