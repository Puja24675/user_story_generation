# User Story Generator

A small Flask service that converts plain-text requirements into Agile-style user stories with acceptance criteria using an LLM-based agent.

## Features

- Accepts a requirement string in JSON and returns a formatted user story and acceptance criteria.
- Validates input to ensure requests contain a useful requirement.
- Uses an async LLM client internally (wrapped for synchronous use by Flask).

## Project structure

- `app.py` - Flask application entrypoint.
- `routes/story_routes.py` - Flask blueprint exposing the `/generate_story` endpoint.
- `services/story_generator.py` - Core logic that calls the LLM client and parses the response.
- `utils/validator.py` - Input validation for incoming requests.

## Requirements

- Python 3.9+
- An OpenAI-compatible API key set as `OPENAI_API_KEY` in the environment when using the LLM integration.

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you don't plan to use the LLM (for local testing), you can still run the Flask app but requests will fail unless `OPENAI_API_KEY` is provided and the `autogen` client is available.

## Running the app

Start the Flask server:

```bash
python app.py
```

The server will listen on http://127.0.0.1:5000 by default.

## API

POST /generate_story

Request body (application/json):

```json
{
	"requirement": "As a user, I want to reset my password so that I can regain access if I forget it."
}
```

Response (200):

```json
{
	"user_story": "As a user, I want to reset my password, so that I can regain access if I forget it.",
	"acceptance_criteria": [
		"Criterion 1",
		"Criterion 2"
	]
}
```

If input validation fails, the API returns a 400 with an `error` message.

## Development notes

- The `services/story_generator.py` uses `autogen_agentchat` and `autogen_ext` packages with an OpenAI-style client. Ensure `OPENAI_API_KEY` is set.
- The `generate_user_story` function wraps an async flow so it can be called synchronously from Flask.
- The system prompt in the service enforces strict output formats: either a formatted user story + acceptance criteria, or the exact words `unclear` / `invalid requirement`.

## Testing

You can test the endpoint using `curl` or Postman.

Example with curl:

```bash
curl -X POST http://127.0.0.1:5000/generate_story \
	-H "Content-Type: application/json" \
	-d '{"requirement": "Allow users to reset forgotten passwords"}'
```

## Next steps / Improvements

- Add unit tests for `utils/validator.py` and `services/story_generator.py` (mock the LLM client).
- Add Dockerfile and a simple docker-compose for local development.
- Add rate limiting and authentication if exposing this service publicly.

---

If you'd like, I can also add a `requirements.txt`, tests, or a Dockerfile — tell me which and I'll add them.

