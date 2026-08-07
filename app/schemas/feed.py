"""Pydantic schemas for Agent Feed API."""

from pydantic import BaseModel, ConfigDict


class PostItemSchema(BaseModel):
    id: str
    createdAt: str
    text: str
    rationale: str
    sources: list[str]

    model_config = ConfigDict(populate_by_name=True)


class AgentFeedResponse(BaseModel):
    posts: list[PostItemSchema]
