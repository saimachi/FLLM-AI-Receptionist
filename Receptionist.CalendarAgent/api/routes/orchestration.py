from lib.graph.graph_service import InjectedGraphService
from fastapi import APIRouter
from foundationallm.models.orchestration import CompletionResponse


# Initialize API routing
router = APIRouter(
    prefix='/orchestration',
    tags=['orchestration'],
    responses={404: {'description':'Not found'}}
)

@router.get('/completion')
async def get_completion(
    graph_service: InjectedGraphService
) -> CompletionResponse:
    calendar_events = await graph_service.get_calendar_events()
    return CompletionResponse(
        user_prompt='What are the appointments for today?',
        completion='\n'.join(calendar_events)
    )
