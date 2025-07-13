from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def watson_webhook():
    try:
        data = request.get_json()
        print("✅ Received data from Watson:", data)

        # Process the input from Watson (this is just an example)
        user_input = data.get("input", {}).get("text", "")
        
        # Create a basic response — customize as needed
        reply = f"You said: {user_input}"

        response = {
            "output": {
                "generic": [
                    {
                        "response_type": "text",
                        "text": reply
                    }
                ]
            }
        }
        return jsonify(response)
    
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Something went wrong on the server"}), 500

@app.route('/', methods=['GET'])
def root():
    return "Watson Webhook is running 🚀"

if __name__ == '__main__':
    app.run(debug=True)
