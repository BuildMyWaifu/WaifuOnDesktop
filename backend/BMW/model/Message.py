from typing import Literal

from BMW.config import config
from fastapi import HTTPException
from pydantic import Field

from .ChatRoom import ChatRoom
from .Document import Document, FilterPayload, SortPayload
from .Editable import CreatePayload, Editable, UpdatePayload
from .User import User


class MessageFilterPayload(FilterPayload):
    chatRoomId: str | None = None

    async def validate_user_filter(self, user: User) -> dict:
        filter_payload = self.model_dump(exclude_none=True)

        if self.chatRoomId:
            chat_room = await ChatRoom.find(_id=self.chatRoomId)
            if not chat_room:
                raise ValueError("聊天室不存在")

            if not (
                (
                    user.type == "staff"
                    and user.level >= config.MESSAGE_GLOBAL_SEARCH_LEVEL
                )
                or (user.id in chat_room.members)
            ):
                raise HTTPException(403, "您沒有權限存取這個聊天室")
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


class MessageCreatePayload(CreatePayload):
    chatRoomId: str
    authorId: str
    text: str
    reply: str | None = None

    async def validate_user_create(self, user: User) -> dict:
        chat_room = await ChatRoom.find(_id=self.chatRoomId)
        if not chat_room:
            raise ValueError("聊天室不存在")

        author = await User.find(_id=self.authorId)
        if not await author.check_permission(user):
            raise HTTPException(403, "您沒有權限發送此訊息")
        if author.id not in chat_room.members:
            raise HTTPException(403, "發送者不在這個聊天室內")

        self.text = self.text.strip()
        if not self.text:
            raise ValueError("訊息不能為空")

        if self.reply:
            reply_message = await Message.find(_id=self.reply)
            if not reply_message:
                raise ValueError("回覆訊息不存在")

        return self.model_dump(exclude_none=True)


class Message(Editable):
    collection_name: str = "Message"

    role: str
    companionId: str
    content: str
    createdAt: int  # unix timestamp ms int

    _FilterPayload = MessageFilterPayload
    _SortPayload = MessageSortPayload
    _UpdatePayload = MessageUpdatePayload
    _CreatePayload = MessageCreatePayload

    @classmethod
    async def check_create_permission(cls, user: User) -> bool:
        return True

    @classmethod
    async def check_search_permission(cls, user: User) -> bool:
        return True

    async def check_permission(self, user: User) -> bool:
        return user.id == self.authorId

    async def get_dict(self, user: User) -> dict:
        chat_room = await ChatRoom.find(_id=self.chatRoomId)
        self_dict = await super().get_dict(user)
        author = await User.find(_id=self.authorId)
        if (
            user.type == "case"
            and chat_room.type == "assistance"
            and author.type == "staff"
        ):
            del self_dict["authorId"]
        return self_dict

    @classmethod
    def empty(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    async def create(self, *args, **kwargs):
        result = await super().create(*args, **kwargs)
        chatroom = await ChatRoom.find(_id=self.chatRoomId)
        await chatroom.update_to_message(self)
        return result
