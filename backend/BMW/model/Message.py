from typing import Literal

from fastapi import HTTPException
from pydantic import Field, BaseModel

from BMW.config import config
from BMW.utils import unix_timestamp_ms

from .Companion import Companion, Pose
from .Document import Document, FilterPayload, SortPayload
from .Editable import CreatePayload, Editable, UpdatePayload
from .User import User


class MessageFilterPayload(FilterPayload):
    companionId: str | None = None

    async def validate_user_filter(self, user: User) -> dict:
        filter_payload = self.model_dump(exclude_none=True)

        if self.companionId:
            companion = await Companion.find(_id=self.companionId)
            if not companion:
                raise ValueError("聊天室不存在")
            # TODO: fix here
            
        else:
            if not (
                user.type == "staff"
                and user.level >= config.MESSAGE_GLOBAL_SEARCH_LEVEL
            ):
                raise HTTPException(403, "您沒有權限搜索全部訊息")

        return filter_payload


class MessageSortPayload(SortPayload):
    createTimestamp: Literal[1, -1] = Field(alias="timestamp", default=-1)

    async def validate_user_sort(self, user: User) -> dict:
        return self.model_dump(by_alias=True)


class MessageUpdatePayload(UpdatePayload):
    async def validate_user_update(self, user: User, document: Document) -> dict:
        raise HTTPException("無法編輯訊息")


class Message(Editable):
    collection_name: str = "Message"

    role: str
    companionId: str
    content: str
    createdAt: int  # unix timestamp ms int
    pose: Pose | None = None


    @classmethod
    async def check_create_permission(cls, user: User) -> bool:
        return True

    @classmethod
    async def check_search_permission(cls, user: User) -> bool:
        return True

    async def check_permission(self, user: User) -> bool:
        return True

    @classmethod
    def empty(cls, *args, **kwargs):
        return cls(*args, **kwargs, createdAt=unix_timestamp_ms())
