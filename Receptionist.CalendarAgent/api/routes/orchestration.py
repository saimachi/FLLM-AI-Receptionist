from typing import Annotated
from fastapi import APIRouter, Depends, Request
from foundationallm.models.orchestration import CompletionRequestBase, CompletionResponse
from lib.openai.calendar_completion_service import CalendarCompletionService


# Initialize API routing
router = APIRouter(
    prefix='/orchestration',
    tags=['orchestration'],
    responses={404: {'description':'Not found'}}
)

@router.get('/completion')
async def get_completion(
    # request: Request,
    openai_service: Annotated[CalendarCompletionService, Depends(CalendarCompletionService)]
) -> CompletionResponse:
    # completion_request = CompletionRequestBase(**request)
    completion_request = CompletionRequestBase(user_prompt="I am here for a workout appointment. Could you please check if I have an appointment scheduled?")
    return CompletionResponse(
        user_prompt=completion_request.user_prompt,
        completion=await openai_service.handle_completion_request(completion_request.user_prompt)
    )
