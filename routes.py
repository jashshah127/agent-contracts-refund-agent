# app/routes.py

from flask import Blueprint, request, jsonify
from app.logic import process_refill

# Create the blueprint
refill_blueprint = Blueprint('refill', __name__)

# Route to handle the refill request
@refill_blueprint.route('/process_refill', methods=['POST'])
def process_refill_route():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Process refill logic
        result, status = process_refill(data)

        # Return the response with result and status code
        return jsonify(result), status
    except Exception as e:
        # If any error occurs, return error response
        return jsonify({"error": str(e)}), 500
