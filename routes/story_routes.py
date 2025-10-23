from flask import Blueprint, request, jsonify
from services.story_generator import generate_user_story
from utils.validator import validate_input

story_bp = Blueprint('story_bp', __name__)

@story_bp.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.get_json()

    # Validate input
    is_valid, error = validate_input(data)
    if not is_valid:
        return jsonify({'error': error}), 400

    requirement = data['requirement']
    story, criteria = generate_user_story(requirement)

    return jsonify({
        'user_story': story,
        'acceptance_criteria': criteria
    }), 200