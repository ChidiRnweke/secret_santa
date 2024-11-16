from dataclasses import dataclass
from secret_santa.models import AssignmentOutput, NameGenerator, AssignmentInput
from secret_santa.database import (
    SantaSessionRepository,
    SantaSessionModel,
    UserAssignmentModel,
)


@dataclass
class AssignmentController:
    name_generator: NameGenerator
    santa_session_repository: SantaSessionRepository

    async def assign(self, users: AssignmentInput) -> AssignmentOutput:
        assignments = users.assign()
        id = self.name_generator.generate_name()
        while await self.santa_session_repository.check_id_exists(id):
            id = self.name_generator.generate_name()

        assignment_models = [
            UserAssignmentModel.from_domain_model(assignment)
            for assignment in assignments
        ]
        santa_session = SantaSessionModel(id=id, name=id, assignments=assignment_models)
        await self.santa_session_repository.add_santa_session(santa_session)
        return AssignmentOutput(assignment_id=id, assignments=assignments)

    async def get_assignment(self, session_id: str, buys_for: str) -> str | None:
        assignment = await self.santa_session_repository.get_assignment(
            session_id, buys_for
        )
        return assignment.buys_from if assignment else None
