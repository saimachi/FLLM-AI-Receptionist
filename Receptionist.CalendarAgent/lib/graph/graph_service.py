from lib.configuration import GRAPH_TENANT_ID, GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET, ASSISTANT_CALENDAR_UPN
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from typing import Annotated
from fastapi import Depends


def graph_service_client():
    credentials = ClientSecretCredential(
        tenant_id=GRAPH_TENANT_ID,
        client_id=GRAPH_CLIENT_ID,
        client_secret=GRAPH_CLIENT_SECRET
    )
    scopes = ['https://graph.microsoft.com/.default']
    return GraphServiceClient(credentials=credentials, scopes=scopes)

def graph_service(graph_client: Annotated[GraphServiceClient, Depends(graph_service_client)]):
    return GraphService(graph_client)

class GraphService:
    """Performs operations using the Microsoft Graph API."""
    def __init__(self, graph_service_client: GraphServiceClient):
        self.graph_service_client = graph_service_client
    async def get_calendar_events(self):
        events = await self.graph_service_client.users.by_user_id(ASSISTANT_CALENDAR_UPN).calendar.events.get()
        return [f'{event.subject} on {event.start.date_time}' for event in events.value]

InjectedGraphService = Annotated[GraphService, Depends(graph_service)]