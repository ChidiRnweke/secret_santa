from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy import func
from secret_santa.models import UserAssignment
from typing import Protocol
from sqlalchemy import select, ForeignKey
from dataclasses import dataclass


class Base(AsyncAttrs, DeclarativeBase):
    pass


class SantaSessionRepository(Protocol):
    async def check_if_name_exits(self, name: str) -> bool: ...

    async def add_santa_session(self, santa_session: "SantaSessionModel") -> None: ...

    async def get_santa_session(self, name: str) -> "SantaSessionModel | None": ...

    async def get_assignment(
        self, session_name: str, gift_sender: str
    ) -> "UserAssignmentModel | None": ...

    async def remove_session(self, session_id: str) -> None: ...


@dataclass
class SantaRepository(SantaSessionRepository):
    session: AsyncSession

    async def check_if_name_exits(self, name: str) -> bool:
        expr = select(SantaSessionModel).where(SantaSessionModel.name == name)
        result = await self.session.execute(expr)
        return bool(result.scalar_one_or_none())

    async def add_santa_session(self, santa_session: "SantaSessionModel") -> None:
        self.session.add(santa_session)
        await self.session.commit()

    async def get_santa_session(self, name: str) -> "SantaSessionModel | None":
        expr = select(SantaSessionModel).where(SantaSessionModel.name == name)
        result = await self.session.execute(expr)
        return result.scalar_one_or_none()

    async def remove_session(self, session_id: str) -> None:
        expr = select(SantaSessionModel).where(SantaSessionModel.name == session_id)
        result = await self.session.execute(expr)
        session = result.scalar_one_or_none()
        if session is not None:
            await self.session.delete(session)
            await self.session.commit()

    async def get_assignment(
        self, session_name: str, gift_sender: str
    ) -> "UserAssignmentModel | None":
        expr = (
            select(UserAssignmentModel)
            .join(SantaSessionModel)
            .where(
                SantaSessionModel.name == session_name,
                func.lower(UserAssignmentModel.gift_sender) == gift_sender.lower(),
            )
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
    gift_sender: Mapped[str]
    gift_receiver: Mapped[str]
    santa_session_id: Mapped[int] = mapped_column(ForeignKey("santa_sessions.id"))

    santa_session: Mapped["SantaSessionModel"] = relationship(
        back_populates="assignments",
        primaryjoin="UserAssignmentModel.santa_session_id == SantaSessionModel.id",
        viewonly=True,
    )

    def to_domain_model(self) -> "UserAssignment":
        return UserAssignment(
            gift_receiver=self.gift_receiver, gift_sender=self.gift_sender
        )

    @classmethod
    def from_domain_model(cls, assignment: UserAssignment) -> "UserAssignmentModel":
        return cls(
            gift_receiver=assignment.gift_sender, gift_sender=assignment.gift_sender
        )
