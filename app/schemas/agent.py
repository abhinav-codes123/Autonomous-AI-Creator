"""Pydantic schemas for Agent Init API."""

from pydantic import BaseModel, ConfigDict, Field


class PersonaInput(BaseModel):
    name: str = Field(..., description="Name of the AI Persona")
    domain: str = Field(..., description="Domain of expertise for the persona")


class AgentInitRequest(BaseModel):
    persona: PersonaInput


class AgentInitResponse(BaseModel):
    agentId: str

    model_config = ConfigDict(populate_by_name=True)
