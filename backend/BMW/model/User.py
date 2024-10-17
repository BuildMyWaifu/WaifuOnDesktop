from abc import ABCMeta
from secrets import token_urlsafe

from pydantic import BaseModel, ConfigDict
import bcrypt

from fastapi import HTTPException

from BMW.utils import console
from BMW.config import config

from .Editable import Editable, basic_permission_check, UpdatePayload
from .ABC import IUser


class UserUpdatePayload(UpdatePayload):
    model_config = ConfigDict(extra="allow")

    async def validate_user_update(self, user: "User", document: "User") -> dict:
        update_dict = self.model_dump()
        update_dict = document.clean_update_dict(update_dict)
        return update_dict


class Profile(BaseModel):
    name: str | None = None
    email: str | None = None


class User(Editable, IUser):
    collection_name: str = "User"

    profile: Profile = Profile()
    passwordHash: bytes | None = None
    token: str | None = None

    _UpdatePayload = UserUpdatePayload

    @classmethod
    async def check_create_permission(cls, user: "User") -> bool: ...

    @classmethod
    async def check_search_permission(cls, user: "User") -> bool: ...

    @classmethod
    def empty(cls, *args, **kwargs) -> "User":
        return User(*args, **kwargs)

    async def check_valid(self, update_dict: dict):
        new_self = await super().check_valid(update_dict)
        if new_self.profile.email:
            all_users_with_same_email = await User.find_any(
                **{"profile.email": new_self.profile.email}
            )
            if all_users_with_same_email:
                for u in all_users_with_same_email:
                    if u.id != new_self.id:
                        console.log(u)
                        raise ValueError(
                            f"無法使用 {new_self.profile.email}，已經被其他人使用了"
                        )
        return new_self

    def safe_dict(self):
        self_dict = self.model_dump(
            exclude={"collection_name", "token", "passwordHash"},
            by_alias=True,
            exclude_none=True,
        )
        return self_dict

    async def update_token(self) -> str:
        new_token = token_urlsafe(128)
        await self.update(token=new_token)
        return new_token

    async def set_password(self, password: str):
        await self.update(
            passwordHash=bcrypt.hashpw(bytes(password, "utf8"), bcrypt.gensalt(8)),
        )

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(bytes(password, "utf8"), self.passwordHash)

    @basic_permission_check
    async def check_permission(self, user: "User"):
        if user.id == self.id:
            return True
