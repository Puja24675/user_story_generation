from flask import Blueprint, request, jsonify
from services.story_generator import generate_user_story
from services.reviewer import review_requirement
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

    review = review_requirement(requirement)
    print(f"Review Score: {review['score']}, Reason: {review['reason']}")

    if review["score"] >= 8:
        story, criteria = generate_user_story(requirement)
        return {
            "score": review["score"],
            "story": story,
            "criteria": criteria
        },200
    elif review["score"] < 8 and "improved_requirement" in review:
        improved_req = review["improved_requirement"]
        story, criteria = generate_user_story(improved_req)
        return {
            "score": review["revised_score"],
            "improved_requirement": improved_req,
            "story": story,
            "criteria": criteria,
            "note": "Improved your given requirement for story generation."
        },200
    else:
        return {
            "score": review["score"],
            "reason": review["reason"],
        },200