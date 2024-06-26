"""
Configuration for the Python external orchestration service.

The project root must contain a .env file.
"""
import os
from dotenv import load_dotenv


load_dotenv()

GRAPH_TENANT_ID = os.environ["GRAPH_TENANT_ID"]
GRAPH_CLIENT_ID = os.environ["GRAPH_CLIENT_ID"]
GRAPH_CLIENT_SECRET = os.environ["GRAPH_CLIENT_SECRET"]
ASSISTANT_CALENDAR_UPN = os.environ["ASSISTANT_CALENDAR_UPN"]

AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
LOCAL_TZ = os.getenv("LOCAL_TZ", "US/Eastern")
