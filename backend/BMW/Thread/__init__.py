from abc import abstractmethod
import threading
import asyncio

from BMW.Manager import ConnectionManager, WebsocketManager
from BMW.model import Payload
from BMW.utils import console


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs, target=self.run)
        self._stop_event = threading.Event()

    def terminate(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    @abstractmethod
    def run(self):
        return NotImplemented


class DeliveryThread(StoppableThread):

    connection_manager: ConnectionManager
    websocket_manager: WebsocketManager

    def __init__(
        self,
        connection_manager: ConnectionManager,
        websocket_manager: WebsocketManager,
        *args,
        **kwargs,
    ):
        self.connection_manager = connection_manager
        self.websocket_manager = websocket_manager
        super().__init__(*args, **kwargs)

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):
        while True:
            if self.stopped():
                return
            await asyncio.sleep(0.01)   
            for userId in self.connection_manager.user_pipe_dict.keys():
                data = self.connection_manager.read(userId=userId)
                if data:
                    websocket_list = self.websocket_manager.websocket_dict.get(
                        userId
                    )
                    if websocket_list:
                        good_websocket_list = []
                        for i, websocket in enumerate(websocket_list):
                            try:
                                await websocket.send_json(data)
                                good_websocket_list.append(websocket)
                            except Exception as e:
                                console.log(e)
                                console.log(f"{userId} connection broken?")
                        self.websocket_manager.websocket_dict[userId] = (
                            good_websocket_list
                        )

