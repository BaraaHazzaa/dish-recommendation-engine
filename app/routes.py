# app/routes.py

from flask import Blueprint, jsonify, request
from .services import generate_and_store_recommendations, get_user_recommendations,save_user_preferences

main = Blueprint('main', __name__)

@main.route('/api/generate_recommendations/<int:user_id>', methods=['POST'])
def generate_recommendations(user_id):
    success = generate_and_store_recommendations(user_id)
    if success:
        return jsonify({"message": "Recommendations generated successfully."}), 200
    else:
        return jsonify({"error": "Failed to generate recommendations. Ensure you have sufficient interaction data."}), 400

@main.route('/api/recommendations/<int:user_id>', methods=['GET'])
def recommendations(user_id):
    # Check if recommendations exist for the user
    recommendations = get_user_recommendations(user_id)

    # If no recommendations found, generate them
    if recommendations.empty:
        success = generate_and_store_recommendations(user_id)
        if success:
            # Retrieve the recommendations after generating them
            recommendations = get_user_recommendations(user_id)
        else:
            return jsonify({"error": "Failed to generate recommendations."}), 400

    # Convert DataFrame to list of dictionaries and add 'AvailabilityStatus'
    rec_list = recommendations.to_dict(orient='records')
    for dish in rec_list:
        dish['AvailabilityStatus'] = 'In Stock' if dish['TotalQuantity'] > 0 else 'Out of Stock'

    return jsonify(rec_list), 200


@main.route('/api/preferences/<int:user_id>', methods=['POST'])
def update_preferences(user_id):
    # Extract preferences from the request body
    preferences = request.json
    
    # Save preferences and generate recommendations
    save_user_preferences(user_id, preferences)
    
    return jsonify({"message": "Preferences saved and recommendations generated."}), 200