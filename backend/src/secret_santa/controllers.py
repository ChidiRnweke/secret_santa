from dataclasses import dataclass
from secret_santa.models import AssignmentOutput, NameGenerator, AssignmentInput
from secret_santa.database import (
    SantaSessionRepository,
    SantaSessionModel,
    UserAssignmentModel,
)
from logging import getLogger

logger = getLogger("app_logger")


@dataclass
class AssignmentController:
    name_generator: NameGenerator
    santa_session_repository: SantaSessionRepository

    async def assign(self, users: AssignmentInput) -> AssignmentOutput:
        assignments = users.assign()
        id = self.name_generator.generate_name()
        while await self.santa_session_repository.check_if_name_exits(id):
            id = self.name_generator.generate_name()

        assignment_models = [
            UserAssignmentModel.from_domain_model(assignment)
            for assignment in assignments
        ]
        santa_session = SantaSessionModel(name=id, assignments=assignment_models)
        await self.santa_session_repository.add_santa_session(santa_session)
        return AssignmentOutput(assignment_name=id, assignments=assignments)

    async def get_assignment(self, session_id: str, gift_sender: str) -> str | None:
        assignment = await self.santa_session_repository.get_assignment(
            session_id, gift_sender
        )
        return assignment.gift_receiver if assignment else None

    async def remove_session(self, session_id: str) -> None:
        await self.santa_session_repository.remove_session(session_id)

    async def validate_dependencies(self, test_input: AssignmentInput) -> bool:
        try:
            output = await self.assign(test_input)
            await self.remove_session(output.assignment_name)
            return True
        except Exception as e:
            logger.error(f"Health check failed, details: {str(e)}")
            return False
