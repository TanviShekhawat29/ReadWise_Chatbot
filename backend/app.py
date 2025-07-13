from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

@app.route('/recommend', methods=['GET'])
def recommend_books():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    params = {
        'q': query,
        'maxResults': 5,
        'printType': 'books'
    }

    res = requests.get(GOOGLE_BOOKS_API, params=params)
    data = res.json()

    results = []
    if 'items' in data:
        for item in data['items']:
            info = item['volumeInfo']
            results.append({
                'title': info.get('title'),
                'authors': info.get('authors'),
                'description': info.get('description'),
                'thumbnail': info.get('imageLinks', {}).get('thumbnail'),
                'infoLink': info.get('infoLink')
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
