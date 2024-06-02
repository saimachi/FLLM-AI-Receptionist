"""
FastAPI configuration for the receptionist orchestrator.
"""
from api.routes import orchestration
from fastapi import FastAPI


app = FastAPI(
    title="Receptionist Agent Custom Orchestrator",
    summary="Custom agent orchestrator for Receptionist tasks, such as finding calendar events.",
    description="This API is a wrapper around the functionality exposed by the MSGraph & OpenAI SDKs.",
    version="1.0.0",
    contact={
        "name": "Sai Machiraju",
        "email": "sai@saimachi.dev",
        "url": "https://saimachi.dev/"
    }
)

app.include_router(orchestration.router)