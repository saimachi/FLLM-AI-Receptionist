import json
from datetime import datetime
from lib.configuration import GRAPH_TENANT_ID, GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET, ASSISTANT_CALENDAR_UPN, LOCAL_TZ
from azure.identity import ClientSecretCredential
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.users.item.calendar.calendar_view.calendar_view_request_builder import CalendarViewRequestBuilder
from msgraph import GraphServiceClient
from typing import Annotated
from fastapi import Depends
from pytz import UTC, timezone


def graph_service_client():
    """
    Provision an authenticated GraphServiceClient for use with dependency injection.
    """
    credentials = ClientSecretCredential(
        tenant_id=GRAPH_TENANT_ID,
        client_id=GRAPH_CLIENT_ID,
        client_secret=GRAPH_CLIENT_SECRET
    )
    scopes = ["https://graph.microsoft.com/.default"]
    return GraphServiceClient(credentials=credentials, scopes=scopes)


def graph_service(
        graph_client: Annotated[GraphServiceClient, Depends(graph_service_client)]
):
    """
    Provision an instance of GraphService with an injected GraphServiceClient.

    This function is meant for clients of GraphService.
    """
    return GraphService(graph_client)


class GraphService:
    """
    Performs operations on Outlook calendars using the Microsoft Graph API.
    
    The associated Entra ID application must have Calendars.ReadWrite application permission.
    """
    def __init__(self, graph_service_client: GraphServiceClient):
        self.graph_service_client = graph_service_client
    
    @classmethod
    def __parse_ts(cls, iso_time: str, local_tz: datetime.tzinfo) -> str:
        """
        Convert a UTC ISO timestamp to a local time ISO timestamp.
        """
        parsed_datetime = datetime.fromisoformat(iso_time)
        parsed_datetime = parsed_datetime.replace(tzinfo=UTC)
        return parsed_datetime.astimezone(local_tz).isoformat()
    
    async def get_calendar_events_today(self):
        """
        Get all calendar events within today's working hours (8:00 AM to 5:00 PM).

        This method will return calendar events as serialized JSON. `start_time` and `end_time` are local times (as defined in `lib.configuration`).
        """
        local_tz = timezone(LOCAL_TZ)
        current_time = datetime.now(local_tz)
        start_time = current_time.replace(hour=8, minute=0, second=0)
        end_time = current_time.replace(hour=17, minute=0, second=0)
        query_params = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
		    start_date_time = start_time.isoformat(),
		    end_date_time = end_time.isoformat(),
        )
        request_configuration = RequestConfiguration(
            query_parameters = query_params,
        )
        events = await self.graph_service_client.users.by_user_id(ASSISTANT_CALENDAR_UPN).calendar.calendar_view.get(
            request_configuration = request_configuration
        )
        return json.dumps( 
                [
                    {
                        "body": event.body.content,
                        "subject": event.subject,
                        "start_time": GraphService.__parse_ts(event.start.date_time, local_tz),
                        "end_time": GraphService.__parse_ts(event.end.date_time, local_tz)
                    } for event in events.value
                ]
        )