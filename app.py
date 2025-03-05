# app.py

from flask import Flask, request, jsonify
import asyncio
from modules.group_chat import MovieBookingGroupChat

# Initialize Flask app
app = Flask(__name__)

# Initialize Router Agent
router = MovieBookingGroupChat()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Agentic AI Movie Booking System is running"}), 200

@app.route("/api/query", methods=["POST"])
def query_agents():
    """API Endpoint to process user queries through AI agents."""
    data = request.json
    user_query = data.get("query")
    user_id = data.get("user_id")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Process user request asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(router.process_query(user_query, user_id))

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
