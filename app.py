from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    intent = data.get("intent")
    entities = data.get("entities", {})

    if intent == "ask_genre_recommendation":
        genre = entities.get("genre", "fiction")
        
        # Call Google Books API
        books = fetch_books_from_google(genre)

        if books:
            response_text = f"Here are some {genre} books:\n- " + "\n- ".join(books)
        else:
            response_text = f"Sorry, I couldn't find any {genre} books at the moment."

        return jsonify({"output": response_text})
    
    return jsonify({"output": "I'm not sure how to help with that yet."})


def fetch_books_from_google(genre):
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults=5"
    try:
        response = requests.get(url)
        data = response.json()

        books = []
        for item in data.get("items", []):
            title = item["volumeInfo"].get("title", "Unknown Title")
            authors = item["volumeInfo"].get("authors", ["Unknown Author"])
            books.append(f"{title} by {', '.join(authors)}")
        return books

    except Exception as e:
        print(f"Error fetching books: {e}")
        return []
