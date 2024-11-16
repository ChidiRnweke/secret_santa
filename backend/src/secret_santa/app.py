from dataclasses import dataclass
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from secret_santa.models import (
    AssignmentInput,
    AssignmentOutput,
    NameGenerator,
    UserAssignment,
)
from secret_santa.database import SantaRepository
from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from controllers import AssignmentController
from config import AppConfig, validate_config


router = APIRouter()

validate_config()


def session_maker_from_connection_string(
    config: Annotated[AppConfig, Depends(AppConfig.from_config)],
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(config.connection_string)
    return async_sessionmaker(engine)


async def get_session(
    session_maker: async_sessionmaker[AsyncSession] = Depends(
        session_maker_from_connection_string
    ),
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@router.post("/assignments")
async def make_assignment(
    assign_input: AssignmentInput,
    name_generator: Annotated[NameGenerator, Depends(NameGenerator.from_config)],
    session: AsyncSession = Depends(get_session),
) -> AssignmentOutput:
    repo = SantaRepository(session)
    controller = AssignmentController(name_generator, repo)
    return await controller.assign(assign_input)


@router.get("/assignments/{assignment_id}/{buy_for}")
async def get_assignment(
    assignment_id: str,
    buy_for: str,
    session: AsyncSession = Depends(get_session),
    name_generator: NameGenerator = Depends(NameGenerator.from_config),
) -> UserAssignment:
    repo = SantaRepository(session)
    controller = AssignmentController(name_generator, repo)
    buys_from = await controller.get_assignment(assignment_id, buy_for)
    if buys_from is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return UserAssignment(buys_for=buy_for, buys_from=buys_from)


@dataclass
class HealthCheck:
    status: str = "ok"


@router.get("/health")
def health_check() -> HealthCheck:
    return HealthCheck()


def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()
