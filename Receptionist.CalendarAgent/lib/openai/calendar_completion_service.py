import json
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
    
    async def handle_completion_request(self, request: str):
        messages = [
            {
                "role": "user",
                "content": request
            }
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_calendar_events",
                    "description": "Find calendar events matching a given search term.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "Event search term. This could be the user's name, for example.",
                            }
                        },
                        "required": ["search_term"],
                    },
                },
            }
        ]
        response = self.azure_openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "search_calendar_events": self.graph_service.search_calendar_events
            }  # only one function in this example, but you can have multiple
            messages.append(response_message)  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = await function_to_call(
                    search_term = function_args.get("search_term")
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = self.azure_openai_client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=messages,
            )  # get a new response from the model where it can see the function response
            return second_response.choices[0].message.content
        return "I'm sorry, but I was unable to locate any matching calendar events."