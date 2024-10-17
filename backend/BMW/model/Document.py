import uuid
from typing import Type, TypeVar, List, Literal
from abc import ABCMeta, abstractmethod, abstractclassmethod

from pydantic import BaseModel, Field
from fastapi import HTTPException

from BMW.utils import EDIT_BLACKLIST, console
import BMW.Manager

from .ABC import IUser

T = TypeVar("T", bound="Document")


class FilterPayload(BaseModel):
    ...

    @abstractmethod
    async def validate_user_filter(self, user: IUser) -> dict:
        return NotImplemented


class SortPayload(BaseModel):
    ...

    @abstractmethod
    async def validate_user_sort(self, user: IUser) -> dict:
        return NotImplemented


class Document(BaseModel, metaclass=ABCMeta):
    id: str = Field(alias="_id", default="")
    collection_name: str
    deleted: Literal[True, None] = None
    _FilterPayload: FilterPayload
    _SortPayload: SortPayload

    @classmethod
    async def validate_search(
        cls, user: IUser, sort: dict, filter: dict
    ) -> tuple[dict, dict]:
        """檢查使用者對此類別的搜索參數是否合法

        Args:
            user (IUser): _description_
            sort (dict): _description_
            filter (dict): _description_

        Raises:
            HTTPException: _description_

        Returns:
            filter: dict, sort: dict
        """
        console.log(filter)
        console.log(sort)
        filter_payload_obj = cls._FilterPayload.model_validate(filter)
        sort_payload_obj = cls._SortPayload.model_validate(sort)
        filter_payload = await filter_payload_obj.validate_user_filter(user)
        sort_payload = await sort_payload_obj.validate_user_sort(user)
        # if filter_payload and sort_payload:
        return filter_payload, sort_payload

        # console.log(filter_payload)
        # console.log(sort_payload)
        # raise HTTPException(500, "不合法的搜索")

    @abstractclassmethod
    async def check_search_permission(cls, user: IUser):
        """檢查使用者是否對此物件擁有搜索權限

        Args:
            user (User): 要檢驗的使用者

        Returns:
            bool: 是否擁有搜索權限
        """
        return NotImplemented

    @abstractmethod
    async def check_permission(self, user: "IUser") -> bool:
        """檢查使用者是否對此物件擁有完全存取權

        Args:
            user (User): 要檢驗的使用者

        Returns:
            bool: 是否擁有完全存取權
        """
        return NotImplemented

    @abstractclassmethod
    def empty(cls: T, *args, **kwargs) -> T:
        """建立對應類別的範例物件

        Args:
            cls (T): 呼叫的類別

        Returns:
            T: 呼叫的類別
        """
        return NotImplemented

    def mongo_dict(self) -> dict:
        self_dict = self.model_dump(
            exclude={"collection_name"},
            by_alias=True,
            # exclude_none=True,
        )
        return self_dict

    def safe_dict(self) -> dict:
        return self.mongo_dict()

    def public_dict(self) -> dict:
        return self.safe_dict()

    async def get_dict(self, user: "IUser") -> dict:
        if await self.check_permission(user):
            return self.safe_dict()
        else:
            return self.public_dict()

    async def create(self) -> str:
        self_dict = self.mongo_dict()
        if self_dict["_id"] == "":
            new_id = str(uuid.uuid4())
            self.id = new_id
            self_dict["_id"] = new_id
        await BMW.Manager.db_manager.get_mongodb()[self.collection_name].insert_one(
            self_dict
        )
        return self_dict["_id"]

    @classmethod
    async def find(cls: Type[T], **kwargs) -> T | None:
        collection_name = cls.model_fields["collection_name"].default
        kwargs["deleted"] = kwargs.get(
            "deleted", None
        )  # 不顯示被刪除的文件，預設為 None，代表不顯示被刪除的文件。設置為 True 代表僅顯示被刪除的文件
        document = await BMW.Manager.db_manager.get_mongodb()[collection_name].find_one(
            kwargs
        )
        if document:
            return cls.model_validate(document)

    @classmethod
    async def find_any(
        cls: Type[T],
        skip=0,
        limit=0,
        sort=[("timestamp", -1),],
        **kwargs
    ) -> List[T]:
        collection_name = cls.model_fields["collection_name"].default
        kwargs["deleted"] = kwargs.get(
            "deleted", None
        )  # 不顯示被刪除的文件，預設為 None，代表不顯示被刪除的文件。設置為 True 代表僅顯示被刪除的文件
        return [
            cls.model_validate(document)
            async for document in BMW.Manager.db_manager.get_mongodb()[
                collection_name
            ].find(filter=kwargs, skip=skip, limit=limit, sort=sort)
        ]

    async def update(self, **kwargs):
        new_document = await self.check_valid(update_dict=kwargs)
        for key, value in kwargs.items():
            setattr(self, key, getattr(new_document, key))
        new_document_dict = new_document.mongo_dict()
        update_payload = {key: new_document_dict.get(key) for key in kwargs.keys()}
        return BMW.Manager.db_manager.get_mongodb()[self.collection_name].update_one(
            {"_id": self.id}, {"$set": update_payload}
        )

    async def validate_delete(self, user: IUser):
        raise HTTPException(403, "沒有權限刪除")
    
    async def permanent_delete(self):
        return BMW.Manager.db_manager.get_mongodb()[self.collection_name].delete_one(
            {"_id": self.id}
        )

    async def check_valid(self, update_dict: dict):
        origin_dict = self.mongo_dict()
        origin_dict.update(update_dict)
        # try:
        return self.model_validate(origin_dict)
        # except ValidationError as e:
        #     raise HTTPException(
        #         500, f"格式錯誤 {', '.join([error.get('msg', '') for error in e.errors()])}"
        #     )

    def clean_update_dict(self, update_dict: dict) -> dict:
        data_copy = update_dict.copy()
        for key in update_dict:
            if key not in self.mongo_dict():
                del data_copy[key]
            elif data_copy[key] == self.mongo_dict()[key]:
                del data_copy[key]

        for key in EDIT_BLACKLIST:
            if key in data_copy:
                del data_copy[key]
        return data_copy

    @classmethod
    def clean_filter_dict(cls, filter_dict: dict) -> dict:
        data_copy = filter_dict.copy()
        for key in EDIT_BLACKLIST:
            if key in filter_dict:
                del data_copy[key]
        return data_copy

    @classmethod
    async def count(cls: Type[T], **kwargs) -> int:
        collection_name = cls.model_fields["collection_name"].default
        return BMW.Manager.db_manager.get_mongodb()[collection_name].count_documents(
            {}, **kwargs
        )

    # @classmethod
    # async def delete_many(cls: Type[T], filter: dict, limit: int = None):
    #     collection_name = cls.model_fields["collection_name"].default
    #     if limit is not None:
    #         # If a limit is provided, delete documents one by one until the limit is reached
    #         count = 0
    #         async for doc in BMW.Manager.db_manager.get_mongodb()[collection_name].find(
    #             filter
    #         ):
    #             if count < limit:
    #                 await BMW.Manager.db_manager.get_mongodb()[
    #                     collection_name
    #                 ].delete_one({"_id": doc["_id"]})
    #                 count += 1
    #             else:
    #                 break
    #         return count
    #     else:
    #         # If no limit is provided, delete all documents that match the filter
    #         return BMW.Manager.db_manager.get_mongodb()[collection_name].delete_many(
    #             filter
    #         )
