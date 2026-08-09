"""Agent Repository for database access."""

import uuid
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.agent import Agent


class AgentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, name: str, domain: str) -> Agent:
        # Deactivate any previous agents so only the newly initialized agent is active
        await self.deactivate_all()
        agent = Agent(
            id=uuid.uuid4(),
            name=name,
            domain=domain,
            is_active=True,
        )
        self.session.add(agent)
        await self.session.commit()
        await self.session.refresh(agent)
        return agent

    async def deactivate_all(self) -> None:
        """Deactivate all agents in the database."""
        stmt = update(Agent).values(is_active=False)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_id(self, agent_id: uuid.UUID) -> Agent | None:
        stmt = select(Agent).where(Agent.id == agent_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_active(self) -> Sequence[Agent]:
        """List all active agents sorted by newest created first."""
        stmt = select(Agent).where(Agent.is_active == True).order_by(Agent.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_active_agent(self) -> Agent | None:
        """Get the single currently active agent."""
        stmt = select(Agent).where(Agent.is_active == True).order_by(Agent.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_all(self) -> Sequence[Agent]:
        """List all agents sorted by newest created first."""
        stmt = select(Agent).order_by(Agent.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()
