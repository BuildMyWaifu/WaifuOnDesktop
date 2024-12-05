from os import getenv, getpid
from typing import TypeVar

import BMW.model
from BMW import POSSIBLE_COLLECTION_NAME
from motor.core import AgnosticClient, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

T = TypeVar("T", bound="BMW.model.Document")


class DBManager:
    mongo_client_dict: dict[int, AgnosticClient] = {}
    mongo_url: str = None
    mongo_database_name: str = None

    def __init__(self) -> None:
        self.mongo_url = getenv("MONGODB_URL")
        self.mongo_database_name = getenv("DATABASE")

    def set_loop(self, loop):
        pid = getpid()
        self.mongo_client_dict[pid] = AsyncIOMotorClient(self.mongo_url, io_loop=loop)

    def new_client(self):
        pid = getpid()
        self.mongo_client_dict[pid] = AsyncIOMotorClient(self.mongo_url)

    def get_mongodb(self) -> AgnosticDatabase:
        pid = getpid()
        if pid in self.mongo_client_dict:
            return self.mongo_client_dict[pid][self.mongo_database_name]
        else:
            self.new_client()
            return self.get_mongodb()

    async def drop_db(self):
        """VERY DANGEROUS!!! DON'T USE THIS IN PRODUCTION ENV"""
        db = self.get_mongodb()
        for collection_name in await db.list_collection_names():
            await db.drop_collection(collection_name)

    async def get_document(
        self, collection_name: POSSIBLE_COLLECTION_NAME, document_id
    ) -> T:
        collection_name2object: dict[POSSIBLE_COLLECTION_NAME, T] = {
            "User": BMW.model.User,
            "File": BMW.model.File,
            "ChatRoom": BMW.model.ChatRoom,
            "Message": BMW.model.Message,
        }
        return await collection_name2object[collection_name].find(_id=document_id)


db_manager = DBManager()
