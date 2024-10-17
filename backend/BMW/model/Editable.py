from typing import TypeVar
from abc import ABCMeta, abstractmethod, abstractclassmethod

from pydantic import BaseModel
from fastapi import HTTPException

from BMW.utils import unix_timestamp_ms, console
from BMW.config import config

from .Document import Document
from .ABC import IUser

T = TypeVar("T", bound="Editable")


def basic_permission_check(func):
    async def wrapper(cls, user: IUser, *args, **kwargs):
        if user.type != "carer" and not user.enable:
            return False
        if user.type == "staff":
            if user.level < config.NONE_PERMISSION_LEVEL:
                return False
            if user.level > config.ALL_PERMISSION_LEVEL:
                return True
        return await func(cls, user, *args, **kwargs)

    return wrapper


class WhoAndWhen(BaseModel):
    userId: str | None = None
    timestamp: int | None = None


class CreatePayload(BaseModel):
    ...

    @abstractmethod
    async def validate_user_create(self, user: IUser) -> dict:
        return NotImplemented


class UpdatePayload(BaseModel):
    ...

    @abstractmethod
    async def validate_user_update(self, user: IUser, document: Document) -> dict:
        return NotImplemented


class Editable(Document, metaclass=ABCMeta):
    _CreatePayload: CreatePayload
    _UpdatePayload: UpdatePayload

    @classmethod
    async def validate_create(cls, user: IUser, create: dict):
        """檢查使用者對此類別的創建參數是否合法

        Args:
            user (IUser): _description_
            create (dict): _description_

        Raises:
            HTTPException: HTTPException(500, "不合法的創建")

        Returns:
            dict: _description_
        """
        create_payload = cls._CreatePayload.model_validate(create)
        create_payload_dict = await create_payload.validate_user_create(user)
        if create_payload_dict:
            return create_payload_dict
        raise HTTPException(500, "不合法的創建")

    async def validate_update(self, user: IUser, update: dict):
        """檢查使用者對此類別的編輯參數是否合法

        Args:
            user (IUser): _description_
            update (dict): _description_

        Raises:
            HTTPException: HTTPException(500, "不合法的更新")

        Returns:
            dict: _description_
        """
        update_payload = self._UpdatePayload.model_validate(update)
        update_payload_dict = await update_payload.validate_user_update(user, self)
        if update_payload_dict:
            return update_payload_dict
        raise HTTPException(500, "不合法的更新")

    @classmethod
    @abstractmethod
    async def check_create_permission(cls, user: IUser):
        """檢查使用者是否對此類別擁有創建權限

        Args:
            user (User): 要檢驗的使用者

        Returns:
            bool: 是否擁有創建權限
        """
        return NotImplemented

  
