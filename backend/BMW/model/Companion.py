from pydantic import BaseModel

from .Editable import Editable
from .User import User


class CompanionProfile(BaseModel):
    name: str | None = None
    description: str | None = None


class CompanionPrompt(BaseModel):
    character: str | None = None
    backstory: str | None = None


class Companion(Editable):
    collection_name: str = "Companion"

    profile: CompanionProfile = CompanionProfile()
    prompt: CompanionPrompt = CompanionPrompt()
    userId: str

    @classmethod
    async def check_create_permission(cls, user: User) -> bool:
        return True

    @classmethod
    async def check_search_permission(cls, user: User) -> bool:
        return True

    async def check_permission(self, user: User) -> bool:
        return user.id == self.authorId

    @classmethod
    def empty(cls, *args, **kwargs):
        return cls(*args, **kwargs)
