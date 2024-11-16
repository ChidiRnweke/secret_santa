from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession

from secret_santa.models import UserAssignment
from typing import Protocol
from sqlalchemy import select, ForeignKey
from dataclasses import dataclass


class Base(AsyncAttrs, DeclarativeBase):
    pass


class SantaSessionRepository(Protocol):
    async def check_id_exists(self, id: str) -> bool: ...

    async def add_santa_session(self, santa_session: "SantaSessionModel") -> None: ...

    async def get_santa_session(self, id: str) -> "SantaSessionModel | None": ...

    async def get_assignment(
        self, session_id: str, buys_for: str
    ) -> "UserAssignmentModel | None": ...


@dataclass
class SantaRepository(SantaSessionRepository):
    session: AsyncSession

    async def check_id_exists(self, id: str) -> bool:
        expr = select(SantaSessionModel).where(SantaSessionModel.id == id)
        result = await self.session.execute(expr)
        return bool(result.scalar_one_or_none())

    async def add_santa_session(self, santa_session: "SantaSessionModel") -> None:
        self.session.add(santa_session)
        await self.session.commit()

    async def get_santa_session(self, id: str) -> "SantaSessionModel | None":
        expr = select(SantaSessionModel).where(SantaSessionModel.id == id)
        result = await self.session.execute(expr)
        return result.scalar_one_or_none()

    async def get_assignment(
        self, session_id: str, buys_for: str
    ) -> "UserAssignmentModel | None":
        expr = select(UserAssignmentModel).where(
            UserAssignmentModel.santa_session_id == session_id,
            UserAssignmentModel.buys_for == buys_for,
        )
        result = await self.session.execute(expr)
        return result.scalar_one_or_none()


class SantaSessionModel(Base):
    __tablename__ = "santa_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    assignments: Mapped[list["UserAssignmentModel"]] = relationship(
        cascade="all, delete-orphan"
    )


class UserAssignmentModel(Base):
    __tablename__ = "user_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    buys_for: Mapped[str]
    buys_from: Mapped[str]
    santa_session_id: Mapped[int] = mapped_column(ForeignKey("santa_sessions.id"))

    def to_domain_model(self) -> "UserAssignment":
        return UserAssignment(buys_for=self.buys_for, buys_from=self.buys_from)

    @classmethod
    def from_domain_model(cls, assignment: UserAssignment) -> "UserAssignmentModel":
        return cls(buys_for=assignment.buys_for, buys_from=assignment.buys_from)
