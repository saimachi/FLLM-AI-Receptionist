import os
from dotenv import load_dotenv


load_dotenv()

GRAPH_TENANT_ID = os.environ['GRAPH_TENANT_ID']
GRAPH_CLIENT_ID = os.environ['GRAPH_CLIENT_ID']
GRAPH_CLIENT_SECRET = os.environ['GRAPH_CLIENT_SECRET']
ASSISTANT_CALENDAR_UPN = os.environ['ASSISTANT_CALENDAR_UPN']
