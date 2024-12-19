import random
import json
from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel, field_validator


@dataclass
class NameGenerator:
    rng: random.Random
    adjectives: list[str]
    nouns: list[str]

    def generate_name(self) -> str:
        adjective = self.rng.choice(self.adjectives)
        noun = self.rng.choice(self.nouns)
        number = self.rng.randint(1, 100)
        return f"{adjective}_{noun}_{number}"

    @classmethod
    def from_config(cls, seed: int | None = None) -> "NameGenerator":
        rng = random.Random(seed)
        path = Path("data") / "santa_data.json"
        with open(path, "r") as f:
            data = json.load(f)
            adjectives = data["adjectives"]
            nouns = data["nouns"]
        return cls(rng=rng, adjectives=adjectives, nouns=nouns)


@dataclass
class UserAssignment:
    gift_sender: str
    gift_receiver: str


@dataclass
class AssignmentOutput:
    assignment_name: str
    assignments: list[UserAssignment]


class AssignmentInput(BaseModel):
    users: list[str]

    @field_validator("users")
    @classmethod
    def _check_unique_users(cls, users: list[str]) -> list[str]:
        if not users:
            raise ValueError("Users list cannot be empty")
        if len(users) != len(set(users)):
            raise ValueError("Users list must contain unique values")
        return users

    def assign(self) -> list[UserAssignment]:
        new_indices = self._random_derangement(len(self.users))
        return [
            UserAssignment(gift_sender=self.users[i], gift_receiver=self.users[j])
            for i, j in enumerate(new_indices)
        ]

    @staticmethod
    def _random_derangement(n: int) -> list[int]:
        while True:
            v = [i for i in range(n)]
            for j in range(n - 1, -1, -1):
                p = random.randint(0, j)
                if v[p] == j:
                    break
                else:
                    v[j], v[p] = v[p], v[j]
            else:
                if v[0] != 0:
                    return v
