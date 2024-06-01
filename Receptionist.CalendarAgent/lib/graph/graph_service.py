import json
from lib.configuration import GRAPH_TENANT_ID, GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET, ASSISTANT_CALENDAR_UPN
from azure.identity import ClientSecretCredential
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.users.item.events.events_request_builder import EventsRequestBuilder
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
    async def search_calendar_events(self, search_term: str) -> str:
        request_configuration = RequestConfiguration(
            query_parameters=EventsRequestBuilder.EventsRequestBuilderGetQueryParameters(
                filter = f"Contains(subject, '{search_term}')"
            )
        )
        filtered_events = await self.graph_service_client.users.by_user_id(ASSISTANT_CALENDAR_UPN).calendar.events.get(
            request_configuration
        )
        return json.dumps( 
                [
                    {
                        'body': event.body.content,
                        'subject': event.subject,
                        'start_time': event.start.date_time
                    } for event in filtered_events.value
                ]
        )
    async def get_calendar_events(self):
        events = await self.graph_service_client.users.by_user_id(ASSISTANT_CALENDAR_UPN).calendar.events.get()
        return [f'{event.subject} on {event.start.date_time}' for event in events.value]