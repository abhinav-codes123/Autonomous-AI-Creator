"""Agent API Endpoint handlers for init and feed."""

import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.db.session import get_db
from app.repositories.agent_repository import AgentRepository
from app.repositories.post_repository import PostRepository
from app.scheduler.autonomous_scheduler import autonomous_scheduler
from app.schemas.agent import AgentInitRequest, AgentInitResponse
from app.schemas.feed import AgentFeedResponse, PostItemSchema
from app.services.publishing.publishing_service import PublishingService

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post(
    "/init",
    response_model=AgentInitResponse,
    status_code=status.HTTP_200_OK,
    summary="Initialize Agent Persona, generate initial post, and start autonomous scheduler",
)
async def init_agent(
    payload: AgentInitRequest,
    db: AsyncSession = Depends(get_db),
) -> AgentInitResponse:
    """Initialize a new AI agent persona, generate its first post immediately, and start the background scheduler."""
    agent_repo = AgentRepository(db)
    agent = await agent_repo.create(
        name=payload.persona.name,
        domain=payload.persona.domain,
    )
    agent_id_str = str(agent.id)
    logger.info(f"Initialized agent '{agent.name}' (domain: {agent.domain}, ID: {agent_id_str})")

    # Generate initial post synchronously so GET /feed contains posts immediately upon return
    publishing_service = PublishingService(db)
    try:
        await publishing_service.run_autonomous_cycle(agent_id=agent.id)
    except Exception as e:
        logger.error(f"Error generating initial post for agent {agent_id_str}: {e}")

    # Start background scheduler for ongoing periodic generation
    autonomous_scheduler.start()

    return AgentInitResponse(agentId=agent_id_str)


@router.get(
    "/feed",
    response_model=AgentFeedResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Agent Feed (Newest First)",
)
async def get_agent_feed(
    agentId: str = Query(..., description="UUID of the initialized agent"),
    db: AsyncSession = Depends(get_db),
) -> AgentFeedResponse:
    """Retrieve posts generated autonomously for the specified agentId.
    
    IMPORTANT: This endpoint strictly reads from the database and NEVER triggers content generation.
    """
    try:
        agent_uuid = uuid.UUID(agentId)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid agentId format. Must be a valid UUID.",
        )

    # Verify agent exists
    agent_repo = AgentRepository(db)
    agent = await agent_repo.get_by_id(agent_uuid)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agentId} not found.",
        )

    # Read existing posts sorted Newest First from database
    post_repo = PostRepository(db)
    posts = await post_repo.get_posts_by_agent(agent_uuid, limit=100)

    post_schemas = [
        PostItemSchema(
            id=str(p.id),
            createdAt=p.created_at.isoformat(),
            text=p.text,
            rationale=p.rationale,
            sources=[s.url for s in p.sources],
        )
        for p in posts
    ]

    return AgentFeedResponse(posts=post_schemas)
