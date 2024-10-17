from multiprocessing import Pipe, Manager
from multiprocessing.connection import Connection
from typing import Literal
import BMW

class ConnectionManager:

    user_pipe_dict: dict[
        str, dict[Literal["send", "recv"], Connection]
    ]  # userId: {send, recv}

    def __init__(self, user_pipe_dict) -> None:
        self.user_pipe_dict = user_pipe_dict

    def send(self, userId, data):
        if userId not in self.user_pipe_dict:
            send, recv = Pipe()
            self.user_pipe_dict[userId] = {"send": send, "recv": recv}

        self.user_pipe_dict[userId]["send"].send(data)

    def read(self, userId):
        if userId not in self.user_pipe_dict:
            return None
        if self.user_pipe_dict[userId]["recv"].poll():
            return self.user_pipe_dict[userId]["recv"].recv()

    async def send_operation(self, user: 'BMW.model.User', type: Literal["update", "create"], document):
        self.send(
            userId=user.id,
            data={
                "type": "update",
                "document_id": document.id,
                "collection": document.collection_name,
                "document": await document.get_dict(user),
            },
        )

    async def update(self, user: 'BMW.model.User', document):
        await self.send_operation(user=user, type="update", document=document)



connection_manager: ConnectionManager = (
    None  # this instance with be create in __main__, to make the multiprocessing part spawn in main process
)
