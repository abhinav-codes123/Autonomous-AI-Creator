"""Agent Repository for database access."""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.agent import Agent


class AgentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, name: str, domain: str) -> Agent:
        agent = Agent(
            id=uuid.uuid4(),
            name=name,
            domain=domain,
        )
        self.session.add(agent)
        await self.session.commit()
        await self.session.refresh(agent)
        return agent

    async def get_by_id(self, agent_id: uuid.UUID) -> Agent | None:
        stmt = select(Agent).where(Agent.id == agent_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> Sequence[Agent]:
        stmt = select(Agent)
        result = await self.session.execute(stmt)
        return result.scalars().all()
