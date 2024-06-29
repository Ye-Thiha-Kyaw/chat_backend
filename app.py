from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Rasa server URL
Rasa_url = "http://localhost:5005/webhooks/rest/webhook"

# Endpoint to handle incoming messages
@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    user_message = data.get('message')
    sender_id = data.get('sender', 'default')

    if not user_message:
        logging.error("No message received in the request")
        return jsonify({"error": "No message received"}), 400

    try:
        # Send user message to Rasa server
        logging.debug(f"Sending message to Rasa: {user_message}")
        response = requests.post(Rasa_url, json={"sender": sender_id, "message": user_message})

        # Check if the request was successful
        if response.status_code != 200:
            logging.error(f"Error from Rasa server: {response.status_code} - {response.text}")
            return jsonify({"error": "Error from Rasa server"}), response.status_code

        # Extract text responses from Rasa server response
        bot_messages = response.json()
        logging.debug(f"Received response from Rasa: {bot_messages}")

        return jsonify(bot_messages)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Rasa server failed: {e}")
        return jsonify({"error": "Failed to reach Rasa server"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
