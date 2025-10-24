import asyncio
import os
import json
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

# ---------------------- Reviewer Agent ----------------------

async def review_requirement_async(requirement: str) -> dict:
    """
    Uses GPT-4o via AutoGen to score a requirement from 0–10 and return a reason.
    Only scores >8 are considered valid for story generation.
    """
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=openai_api_key
    )

    system_message = """
You are a reviewer agent. Your job is to evaluate user requirements and score them from 0 to 10 based on clarity, completeness, and usefulness for generating user stories.

Scoring Criteria:
- Clear actor (e.g., 'As a user...')
- Clear action or goal
- Clear benefit or purpose
- Sufficient detail (not vague)
- Includes filters, roles, constraints, or time-based logic

Your behavior depends on the score:

1. If the score is between **1 and 5**:
   - Respond with a JSON object containing the score and a short reason explaining why the requirement is weak or unclear.
   - Do **not** attempt to fix or rewrite the input.

2. If the score is between **6 and 8**:
   - Respond with a JSON object containing:
     - `"score"`: the original score
     - `"reason"`: why the input is borderline
     - `"improved_requirement"`: a revised version of the input that improves clarity, structure, and completeness
     - `"revised_score"`: the new score after improvement
     - `"revised_reason"`: why the improved version is better

3. If the score is between **9 and 10**:
   - Respond with a JSON object containing the score and a short reason.
   - Do **not** modify the input.

Always respond in valid JSON format. Example formats:

For score 3:
```json
{
  "score": 3,
  "reason": "Missing actor and benefit; vague action"
}

"""

    agent = AssistantAgent(
        name="ReviewerAgent",
        model_client=model_client,
        system_message=system_message
    )

    task = f"Evaluate the following requirement and return a score and reason:\n\n{requirement}"
    result = await agent.run(task=task)
    # print(result)
    await model_client.close()

    try:
        response = result.messages[-1].content.strip()        
        print("Raw response:", repr(response))  # Debug print

        # Remove Markdown code block if present
        if response.startswith("```json"):
            response = response.replace("```json", "").strip()
        if response.endswith("```"):
            response = response[:-3].strip()

        if not response or not response.startswith("{"):
            raise ValueError("Empty or non-JSON response")

        return json.loads(response)
    except Exception as e:
        return {"score": 0, "reason": f"Failed to parse reviewer response: {str(e)}"}


def review_requirement(requirement: str):
    """
    Sync wrapper for reviewer agent.
    Returns a dict: { 'score': int, 'reason': str }
    """
    return asyncio.run(review_requirement_async(requirement))