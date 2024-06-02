from datetime import datetime
from lib.configuration import GRAPH_TENANT_ID, GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET, ASSISTANT_CALENDAR_UPN
from azure.identity import ClientSecretCredential
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.users.item.events.events_request_builder import EventsRequestBuilder
from msgraph import GraphServiceClient
from typing import Annotated
from fastapi import Depends
from pytz import timezone, UTC


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
    async def does_calendar_event_exist(self, name: str, time: str) -> str:
        current_time = datetime.now(timezone("EST"))
        # If there's a parsing error, just use the current time
        converted_time = current_time
        try:
            converted_time = datetime.strptime(time, "%H:%M")
        except ValueError:
            print(f"[ERROR] Failed to parse input {time}")
        else:
            # Military time normalization
            # For example, if the user's appointment is at "2:00", but it's currently afternoon, then their appointment is at "14:00" 
            if converted_time.hour < 12 and current_time.hour >= 12:
                print(f'[INFO] Military time hour normalization from {converted_time.hour} to {converted_time.hour + 12}')
                converted_time = converted_time.replace(hour=(converted_time.hour + 12))
            converted_time = converted_time.replace(current_time.year, current_time.month, current_time.day)
        # Use UTC (timezone-agnostic) for comparison
        converted_time = converted_time.astimezone(timezone("UTC"))
        # Look for username in subject
        request_configuration = RequestConfiguration(
            query_parameters=EventsRequestBuilder.EventsRequestBuilderGetQueryParameters(
                filter = f"Contains(subject, '{name}')"
            )
        )
        filtered_events = await self.graph_service_client.users.by_user_id(ASSISTANT_CALENDAR_UPN).calendar.events.get(
            request_configuration
        )
        for event in filtered_events.value:
            # Strip millisecond field
            event_time = datetime.strptime(event.start.date_time[:-8], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=UTC)
            # 15 minute (900 s) grace period
            if abs((event_time - converted_time).total_seconds()) <= 900:
                return True
        return False