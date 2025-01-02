from pydantic import BaseModel

from BMW.LLMCore import setup_trait_and_send_systemPrompt

from .Editable import Editable
from .User import User


class Pose(BaseModel):
    motion: str
    expression: str


class CompanionTrait(BaseModel):
    role: str = "companion"
    personality: str = ""
    communication_style: str = ""
    emotional_response: str = ""


class Companion(Editable):
    collection_name: str = "Companion"

    userId: str

    name: str | None = None
    description: str | None = None

    live2dModelSettingPath: str | None = None
    poseMap: dict[str, Pose] = {}

    backstory: str | None = None

    trait: CompanionTrait | None = None

    @classmethod
    async def check_create_permission(cls, user: User) -> bool:
        return True

    @classmethod
    async def check_search_permission(cls, user: User) -> bool:
        return True

    async def check_permission(self, user: User) -> bool:
        return user.id == self.userId

    @classmethod
    def empty(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    async def setup(self):
        await setup_trait_and_send_systemPrompt(self)

    async def create(self):
        await super().create()
        return self
