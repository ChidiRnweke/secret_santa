from contextlib import asynccontextmanager
from dataclasses import dataclass
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from secret_santa.models import (
    AssignmentInput,
    AssignmentOutput,
    NameGenerator,
    UserAssignment,
)
from secret_santa.database import SantaRepository
from typing import AsyncGenerator, Literal
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from secret_santa.controllers import AssignmentController
from secret_santa.config import AppConfig, RuntimeMode
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from secret_santa.telemetry import configure_telemetry
from logging import getLogger

router = APIRouter()
logger = getLogger("app_logger")


_session_store: dict[Literal["session_maker"], async_sessionmaker[AsyncSession]] = {}
_name_generator: dict[Literal["name_generator"], NameGenerator] = {}
_app_config: dict[Literal["app_config"], AppConfig] = {}


def get_name_generator() -> NameGenerator:
    return _name_generator["name_generator"]


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    return _session_store["session_maker"]


def get_app_config() -> AppConfig:
    return _app_config["app_config"]


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@router.post("/assignments")
async def make_assignment(
    assign_input: AssignmentInput,
    session: AsyncSession = Depends(get_session),
) -> AssignmentOutput:
    name_generator = get_name_generator()
    repo = SantaRepository(session)
    controller = AssignmentController(name_generator, repo)
    return await controller.assign(assign_input)


@router.get("/assignments/{assignment_id}/{gift_sender}")
async def get_assignment(
    assignment_id: str,
    gift_sender: str,
    session: AsyncSession = Depends(get_session),
) -> UserAssignment:
    repo = SantaRepository(session)
    name_generator = get_name_generator()
    controller = AssignmentController(name_generator, repo)
    assignment = await controller.get_assignment(assignment_id, gift_sender)
    if assignment is None:
        logger.info(f"Assignment not found for {gift_sender}")
        raise HTTPException(status_code=404, detail="Assignment not found")
    return UserAssignment(
        gift_sender=assignment.gift_sender,
        gift_receiver=assignment.gift_receiver,
        times_viewed=assignment.times_viewed,
    )


@dataclass
class HealthCheck:
    status: str = "ok"


@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)) -> HealthCheck:
    name_generator = get_name_generator()
    repo = SantaRepository(session)

    controller = AssignmentController(name_generator, repo)
    test_input = AssignmentInput(users=["test1", "test2"])
    success = await controller.validate_dependencies(test_input)
    if success:
        return HealthCheck()
    else:
        raise HTTPException(status_code=500, detail="Health check failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = AppConfig.from_config()
    _app_config["app_config"] = config
    engine = create_async_engine(config.connection_string)
    _session_store["session_maker"] = async_sessionmaker(engine)
    _name_generator["name_generator"] = NameGenerator.from_config()
    yield


def create_app():
    app = FastAPI(lifespan=lifespan, root_path="/api")
    app.include_router(router)

    config = AppConfig.from_config()
    if config.mode == RuntimeMode.PROD:
        configure_telemetry(config)
        FastAPIInstrumentor.instrument_app(app)
    logger.info("App configured")
    return app


app = create_app()


@app.exception_handler(Exception)
async def exception_callback(request: Request, exc: Exception):
    logger.error(str(exc))
    return JSONResponse(status_code=500, content={"message": "Internal server error"})
