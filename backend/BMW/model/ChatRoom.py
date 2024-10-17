from typing import Literal

from pydantic import Field
from fastapi import HTTPException
import os

from .ABC import IUser
import BMW.model  # import the module to prevent circular import
from BMW.utils import has_duplicates, unix_timestamp_ms, console
from BMW.config import config
import BMW.Manager

from .Document import FilterPayload, SortPayload
from .Editable import Editable, UpdatePayload, CreatePayload
from .User import User


class ChatRoomFilterPayload(FilterPayload):
    type: Literal["private", "assistance"] | None = None
    member: str | None = None

    async def validate_user_filter(self, user: User) -> dict:
        if not self.member and not user.level >= config.MESSAGE_GLOBAL_SEARCH_LEVEL:
            raise HTTPException(403, "權限不足，無法查詢所有聊天室")

        member = await User.find(_id=self.member)
        if member:
            if not await member.check_permission(user):
                raise HTTPException(403, "權限不足，無法查詢該使用者的聊天室")
        else:
            raise ValueError("無此使用者")

        filter_payload = self.model_dump(exclude_none=True, by_alias=True)
        filter_payload["members"] = filter_payload["member"]
        del filter_payload["member"]
        return filter_payload


class ChatRoomSortPayload(SortPayload):
    lastUpdateTimestamp: Literal[1, -1] = -1

    async def validate_user_sort(self, user: User) -> dict:
        return self.model_dump(by_alias=True)


class ChatRoomUpdatePayload(UpdatePayload):
    members: list[str]

    async def validate_user_update(self, user: User, document: "ChatRoom") -> dict:
        if document.type == "private":
            raise ValueError("私人聊天室無法變更成員")

        if has_duplicates(self.members):
            raise ValueError("聊天室成員不能重複")

        for oldMemberId in document.members:
            if oldMemberId not in self.members:
                # remove oldMemberId from chatroom
                oldMember = await User.find(_id=oldMemberId)
                if not await oldMember.check_permission(user):
                    raise HTTPException(403, f"權限不足，無法替{oldMember}退出聊天室")

        for newMemberId in self.members:
            if newMemberId not in document.members:
                newMember = await User.find(_id=newMemberId)
                if not await newMember.check_permission(user):
                    raise HTTPException(403, f"權限不足，無法替{newMember}加入聊天室")

        return self.model_dump()


class ChatRoomCreatePayload(CreatePayload):
    type: Literal["private", "assistance"]
    members: list[str] = []

    async def validate_user_create(self, user: User) -> dict:

        if user.type == "case" and self.type == "assistance":
            chatroom = await ChatRoom.find(member=user.id, type="assistance")
            if chatroom:
                return ValueError("您已經在一個照護聊天室內了")

            staff = await user.get_staff()
            self.members = [staff.id, user.id]
            return self.model_dump()

        if has_duplicates(self.members):
            raise ValueError("聊天室成員不能重複")

        if self.members == []:
            raise ValueError("成員列表不得為空")

        members = await User.find_any(**{"_id": {"$in": self.members}})
        case_list = []
        for member in members:
            if member.type == "case":
                case_list.append(member)
            if not member.enable:
                raise ValueError(f"未啟用的{member}無法加入聊天室")
            if not await member.check_permission(user):
                raise HTTPException(403, f"權限不足，無法替{member}加入聊天室")

            if self.type == "assistance" and member.type == "carer":
                raise ValueError("照顧者不能加入照護聊天室")

        if self.type == "private":
            if user.id not in self.members:
                raise HTTPException(403, "無法幫別人建立私人聊天室")
            if len(self.members) != 2:
                raise ValueError("私人聊天室只能有兩位成員")
            chatroom = await ChatRoom.find(
                type="private", members={"$size": 2, "$all": self.members}
            )
            if chatroom:
                raise ValueError("已有現有的私人聊天室")
        else:
            assert self.type == "assistance"
            if len(case_list) != 1:
                raise ValueError("照護聊天室內僅能有一個個案")
            chatroom = await ChatRoom.find(type="assistance", members=case_list[0].id)
            if chatroom:
                raise ValueError("此個案已有一個照護聊天室")

        return self.model_dump()


class ChatRoom(Editable):
    collection_name: str = "ChatRoom"
    members: list[str] = []
    type: Literal["private", "assistance"]
    lastUpdateTimestamp: int  # unix timestamp in ms

    _FilterPayload = ChatRoomFilterPayload
    _SortPayload = ChatRoomSortPayload
    _UpdatePayload = ChatRoomUpdatePayload
    _CreatePayload = ChatRoomCreatePayload

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
        return cls(*args, **kwargs, lastUpdateTimestamp=unix_timestamp_ms())

    async def update_to_message(self, message: "BMW.model.Message"):
        for memberId in self.members:
            member = await User.find(_id=memberId)
            await BMW.Manager.connection_manager.update(member, document=message)
            
        await self.update(lastUpdateTimestamp=unix_timestamp_ms())

    async def update(
        self,  *args, **kwargs
    ):
        old_members = self.members
        result = await super().update( *args, **kwargs)
        for memberId in list(set(self.members + old_members)):
            member = await User.find(_id=memberId)
            await BMW.Manager.connection_manager.update(member, self)
        return result
