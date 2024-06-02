import json
from foundationallm.models.orchestration import CompletionRequestBase
from lib.configuration import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME
from lib.graph.graph_service import GraphService, graph_service
from lib.openai.tools_catalog import TOOLS, METHOD_SIGNATURES
from typing import Annotated
from fastapi import Depends
from openai import AzureOpenAI


def azure_openai_client():
    """
    Obtain an instance of the AzureOpenAI client from the OpenAI SDK for dependency injection.
    """
    return AzureOpenAI(
        azure_endpoint = AZURE_OPENAI_ENDPOINT,
        api_key = AZURE_OPENAI_KEY,
        api_version = AZURE_OPENAI_API_VERSION
    )


class CalendarCompletionService:
    """
    Injectable service that implements the CalendarScheduler agent.
    """
    def __init__(
        self,
        azure_openai_client: Annotated[AzureOpenAI, Depends(azure_openai_client)],
        graph_service: Annotated[GraphService, Depends(graph_service)]
    ):
        self.azure_openai_client = azure_openai_client
        self.graph_service = graph_service
        self._tool_callbacks = {
            "get_calendar_events_today": self.graph_service.get_calendar_events_today
        }
    
    async def handle_completion_request(self, request: CompletionRequestBase) -> str:
        """
        Respond to a FoundationaLLM completion request by calling Azure OpenAI and the pertinent tools.
        """
        # Assemble messages using FLLM prompt history
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

        # Source: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling
        # Step 1: Call model
        response = self.azure_openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self._tool_callbacks[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_parameter_names = METHOD_SIGNATURES[function_name]
                function_call_args = {}
                for parameter_name in function_parameter_names:
                    function_call_args[parameter_name] = function_args.get(parameter_name, "")
                print(f"[INFO] Calling {function_name} with arguments {function_call_args}")
                function_response = await function_to_call(**function_call_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            
            # Step 4: send the info for each function call and function response to the model
            second_response = self.azure_openai_client.chat.completions.create(
                model = AZURE_OPENAI_DEPLOYMENT_NAME,
                messages = messages,
            )
            return second_response.choices[0].message.content
        
        # No tool calls - not a calendar-related task
        return "I'm sorry, but I'm unable to help with that task."