"""Main API router incorporating endpoints."""

from fastapi import APIRouter
from app.api.endpoints import agent

api_router = APIRouter()
api_router.include_router(agent.router)
