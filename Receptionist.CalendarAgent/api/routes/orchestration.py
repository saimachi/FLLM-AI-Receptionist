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

@router.post('/completion')
async def get_completion(
    request: Request,
    openai_service: Annotated[CalendarCompletionService, Depends(CalendarCompletionService)]
) -> CompletionResponse:
    body = await request.json()
    completion_request = CompletionRequestBase(**body)
    return CompletionResponse(
        user_prompt=completion_request.user_prompt,
        completion=await openai_service.handle_completion_request(completion_request)
    )
