"""Agent API Endpoint handlers for init, feed, stats, and reset."""

import uuid
from datetime import timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.db.session import get_db
from app.repositories.agent_repository import AgentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.topic_repository import TopicRepository
from app.scheduler.autonomous_scheduler import autonomous_scheduler
from app.schemas.agent import AgentInitRequest, AgentInitResponse, AgentStatsResponse
from app.schemas.feed import AgentFeedResponse, PostItemSchema

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post(
    "/init",
    response_model=AgentInitResponse,
    status_code=status.HTTP_200_OK,
    summary="Initialize Agent Persona and start autonomous scheduler",
)
async def init_agent(
    payload: AgentInitRequest,
    db: AsyncSession = Depends(get_db),
) -> AgentInitResponse:
    """Persist one agent and begin its independent scheduled publishing lifecycle."""
    agent_repo = AgentRepository(db)
    agent = await agent_repo.create(
        name=payload.persona.name,
        domain=payload.persona.domain,
    )
    agent_id_str = str(agent.id)
    logger.info(f"[INIT] Agent created: {agent_id_str} ({agent.name}, {agent.domain})")

    # Publishing is deliberately not triggered here. The first post may only be
    # created by the independently running scheduled cycle.
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
            createdAt=(
                p.created_at.replace(tzinfo=timezone.utc)
                if p.created_at.tzinfo is None
                else p.created_at.astimezone(timezone.utc)
            ).isoformat().replace("+00:00", "Z"),
            text=p.text,
            rationale=p.rationale,
            sources=[s.url for s in p.sources],
        )
        for p in posts
    ]

    return AgentFeedResponse(posts=post_schemas)


@router.get(
    "/stats",
    response_model=AgentStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Agent Discovery & Publication Statistics",
)
async def get_agent_stats(
    agentId: str = Query(..., description="UUID of the initialized agent"),
    db: AsyncSession = Depends(get_db),
) -> AgentStatsResponse:
    """Retrieve live discovery and publication statistics for the dashboard."""
    try:
        agent_uuid = uuid.UUID(agentId)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid agentId format. Must be a valid UUID.",
        )

    topic_repo = TopicRepository(db)
    post_repo = PostRepository(db)

    total_discovered = await topic_repo.count_all_topics(agent_id=agent_uuid)
    total_rejected = await topic_repo.count_rejected_topics(agent_id=agent_uuid)
    published_count = await post_repo.count_posts_by_agent(agent_uuid)

    shortlisted_count = max(0, total_discovered - total_rejected)
    selected_count = published_count

    return AgentStatsResponse(
        sourcesMonitored=8,
        topicsDiscovered=total_discovered,
        topicsRejected=total_rejected,
        published=published_count,
        shortlisted=shortlisted_count,
        selected=selected_count,
    )


@router.post(
    "/reset",
    status_code=status.HTTP_200_OK,
    summary="DEVELOPMENT ONLY: Reset agent state and stop scheduler",
)
async def reset_agent_state(
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """DEVELOPMENT ONLY: Truncate posts, topics, and agents tables to prepare for a fresh evaluation."""
    autonomous_scheduler.shutdown()
    await db.execute(text("DELETE FROM post_sources;"))
    await db.execute(text("DELETE FROM posts;"))
    await db.execute(text("DELETE FROM rejected_topics;"))
    await db.execute(text("DELETE FROM topics;"))
    await db.execute(text("DELETE FROM agents;"))
    await db.commit()
    logger.info("[DEV RESET] Successfully reset database state.")
    return {"status": "reset_complete"}
