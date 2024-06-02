import json
from foundationallm.models.orchestration import CompletionRequestBase
from lib.configuration import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME
from lib.graph.graph_service import GraphService, graph_service
from typing import Annotated
from fastapi import Depends
from openai import AzureOpenAI


def azure_openai_client():
    return AzureOpenAI(
        azure_endpoint = AZURE_OPENAI_ENDPOINT,
        api_key = AZURE_OPENAI_KEY,
        api_version = AZURE_OPENAI_API_VERSION
    )

class CalendarCompletionService:
    def __init__(
        self,
        azure_openai_client: Annotated[AzureOpenAI, Depends(azure_openai_client)],
        graph_service: Annotated[GraphService, Depends(graph_service)]
    ):
        self.azure_openai_client = azure_openai_client
        self.graph_service = graph_service
    
    async def handle_completion_request(self, request: CompletionRequestBase) -> str:
        messages = [
            *[
                {
                    "role": message.sender.lower(),
                    "content": message.text
                } for message in request.message_history
            ],
            {
                "role": "user",
                "content": request.user_prompt
            }
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "does_calendar_event_exist",
                    "description": "Check if an appointment exists for the given user and time.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the user for the appointment.",
                            },
                            "time": {
                                "type": "string",
                                "description": "The time of the appointment. There should be NO date information and do NOT include the time of day (AM/PM). For example, '2:00' and '11:00' are VALID, while '2:00 on May 23rd', '2:00 PM today', and '11:00 PM' are INVALID.",
                            }
                        },
                        "required": ["name"],
                    },
                },
            }
        ]
        response = self.azure_openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            tool_call = tool_calls[0]
            function_args = json.loads(tool_call.function.arguments)
            if function_args.get("name") is None:
                return "Please provide your name."
            print(f'Name: {function_args["name"]}')
            print(f'Time: {function_args.get("time", "")}')
            appointment_exists = await self.graph_service.does_calendar_event_exist(
                name = function_args["name"],
                time = function_args.get("time", "")
            )
            if appointment_exists:
                return "Yes, we have an appointment scheduled for you. Please have a seat."
            return "Sorry, but we couldn't find an appointment matching that name and time."
        return "I'm sorry, but I'm unable to handle your request."