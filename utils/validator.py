import re


def validate_input(data):
    """Validate the incoming JSON body for a 'requirement'.

    Returns (is_valid: bool, reason: str).
    reason is a short human-friendly explanation when invalid.
    """
    if not data:
        return False, "Missing JSON body"
    if 'requirement' not in data:
        return False, 'Missing "requirement" field'

    req = data['requirement']
    if req is None:
        return False, "Requirement is null"

    req = str(req).strip()
    if not req:
        return False, "Requirement cannot be empty"

    # Reject inputs that are too short to be actionable (e.g., single-word 'Login')
    if len(req) < 10:
        return False, "Requirement is too short or vague"

    # Reject if no alphanumeric characters (only punctuation)
    if not re.search(r"[A-Za-z0-9]", req):
        return False, "Requirement does not contain alphanumeric characters"

    return True, ""

 