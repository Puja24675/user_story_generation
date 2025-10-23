import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

async def generate_story_async(requirement: str):

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=openai_api_key
    )

    # Strong system prompt for GPT-based reasoning
    system_message = system_message = """

        You are a Requirement-to-User-Story transformation agent.

        Your task is to analyze any given input text and determine whether it can be transformed into a valid Agile user story.

        Follow these rules strictly:

        1. If the input represents a clear, valid requirement that includes:
        - A user or actor (who needs it)
        - A clear goal or action (what they want to do)
        - A reason or benefit (why they need it)
        Then generate a **User Story** in this format:
        "As a [user/actor], I want to [goal/action], so that [benefit/outcome]."

        2. If the input is relevant to software or system requirements but lacks clarity, completeness, or context (for example, missing actor, purpose, or benefit), respond exactly with:
        unclear

        3. If the input is irrelevant to software, system, or business requirements (for example, everyday tasks, non-technical phrases, random sentences), respond exactly with:
        invalid requirement

        4. Never attempt to infer, assume, or hallucinate additional context beyond what is clearly given in the input.
        - Do NOT create artificial user stories for vague, technical, or irrelevant statements.
        - Do NOT fix unclear requirements — just label them as "unclear".


        Your goal is to strictly enforce these rules and produce one of the following outputs only:
        - "User Story: As a [actor], I want to [action], so that [benefit].\n"
                "Acceptance Criteria:\n"
                "- [criterion 1]\n"
                "- [criterion 2]\n"
                "- [criterion 3]"
        - The word unclear or invalid requirement(if input is not valid)
        """
    
    agent = AssistantAgent(
        "assistant",
        model_client=model_client,
        system_message=system_message
    )

    task = (
        f"Convert the following requirement into a valid Agile user story with acceptance criteria:\n\n"
        f"Requirement: {requirement}\n\n"
        f"Follow the required format strictly."
    )

    result = await agent.run(task=task)
    output = result.messages[-1].content.strip()
    # print(output)
    await model_client.close()

    if output in ('unclear','invalid requirement'):
        # Clarification case
        story = "Invalid"
        criteria=[]
    else:
        # Normal user story case
        lines = output.strip().split("\n")
        story = lines[0].replace("User Story:", "").strip()
        criteria = [line.strip("- ").strip() for line in lines[1:] if line.startswith("-")]

    return story, criteria


def generate_user_story(requirement: str):
    """
    Sync wrapper for Flask or other apps.
    Always returns a tuple: (story, criteria) if story is valid otherwise strictly 
    do not return criteria.
    """
    return asyncio.run(generate_story_async(requirement))