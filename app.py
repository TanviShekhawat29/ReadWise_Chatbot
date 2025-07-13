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

    # Check for genre from Watson Assistant
    genre = None
    try:
        genre = data['context']['skills']['main skill']['user_defined'].get('genre')
    except Exception:
        pass

    if genre:
        books = get_books_by_genre(genre)
        response_text = f"Here are some popular {genre} books:\n" + books
    else:
        response_text = "Please tell me what genre you're interested in, like fantasy or mystery!"

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

def get_books_by_genre(genre):
    params = {
        "q": f"subject:{genre}",
        "maxResults": 5,
        "printType": "books",
        "langRestrict": "en"
    }
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        items = response.json().get("items", [])
        if not items:
            return "Sorry, I couldn't find any books in that genre."

        book_list = []
        for item in items:
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title", "Unknown Title")
            authors = ", ".join(volume_info.get("authors", ["Unknown Author"]))
            book_list.append(f"📘 {title} by {authors}")

        return "\n".join(book_list)
    except Exception as e:
        return "Oops! Something went wrong while fetching books."

if __name__ == "__main__":
    app.run(debug=True)
