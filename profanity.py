import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Your WebPurify API key (replace with your actual key)
API_KEY = '27530d0b658daae198b2154a1c01918b'

# WebPurify endpoint for checking profanity in text
WEBPURIFY_API_URL = "https://api1.webpurify.com/services/rest/"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def detect_cuss_words(text):
    # Prepare the request parameters
    params = {
        'method': 'webpurify.live.check',
        'api_key': API_KEY,
        'text': text,
        'format': 'json'
    }

    # Send the request to the WebPurify API
    response = requests.get(WEBPURIFY_API_URL, params=params)

    # Parse the JSON response
    result = response.json()

    if result['rsp']['@attributes']['stat'] == 'ok':
        # Check if profanity was found
        contains_profanity = result['rsp']['found']
        return bool(int(contains_profanity))  # Convert string '1' or '0' to boolean
    else:
        # Handle any API errors
        print("Error:", result['rsp']['err']['msg'])
        return None

@app.route('/check_profanity', methods=['GET'])
def check_profanity():
    message = request.args.get('message')
    if not message:
        return jsonify({"error": "No message provided"}), 400

    result = detect_cuss_words(message)

    if result is None:
        return jsonify({"error": "An error occurred while checking for profanity"}), 500

    return jsonify({"contains_profanity": result})

# Remove this line
# if __name__ == '__main__':
#     app.run(debug=True)
