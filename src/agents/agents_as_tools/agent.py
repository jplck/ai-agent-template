import os
from typing import Any
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from azure.ai.projects.aio import AIProjectClient
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize clients at module level for devui discovery
project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

chat_client = AzureAIAgentClient(
    model_deployment_name="gpt-4.1",
    project_client=project_client
)

# Create agents at module level for devui discovery
hr_agent = chat_client.create_agent(
    name="HR Specialist",
    instructions="You are an HR specialist agent that handles employee onboarding and offboarding tasks.",
).as_tool(
    name="HRSpecialist",
    description="Handles employee onboarding and offboarding tasks.",
    arg_name="prompt",
    arg_description="The onboarding or offboarding request details.",
)

orchestrator_agent = chat_client.create_agent(
    name="Orchestrator",
    instructions="You are an orchestrator agent that routes tasks to specialized agents based on content.",
    tools=[hr_agent],
)

async def main():
    async for chunk in orchestrator_agent.run_stream("Onboard a new employee named Alice. Offboard an employee named Bob."):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
