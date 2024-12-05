import asyncio
import threading
from abc import abstractmethod

from BMW.Manager import ConnectionManager, WebsocketManager
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

            user_ids = list(self.connection_manager.user_pipe_dict.keys())
            tasks = [self.handle_user(user_id) for user_id in user_ids]
            await asyncio.gather(*tasks)

    async def handle_user(self, user_id: str):
        """
        Handle data delivery for a single user, including all associated websockets.
        """

        mailbox = {}
        other_data = []
        while True:
            data = self.connection_manager.read(userId=user_id)
            if not data:
                break

            data_type = data.get("type")
            data_document_id = data.get("document_id")
            if data_type and data_document_id:
                mailbox[f"{data_type}_{data_document_id}"] = data
            else:
                other_data.append(data)

        payloads = list(mailbox.values()) + other_data

        if payloads:
            for data in payloads:
                websocket_list = self.websocket_manager.websocket_dict.get(user_id)
                if websocket_list:
                    # Create a task pool to send data concurrently to multiple websockets
                    results = await asyncio.gather(
                        *[
                            self.send_data(websocket, data)
                            for websocket in websocket_list
                        ],
                        return_exceptions=True,
                    )
                    # Update the websocket list by filtering out broken connections
                    self.websocket_manager.websocket_dict[user_id] = [
                        websocket
                        for websocket, result in zip(websocket_list, results)
                        if not isinstance(result, Exception)
                    ]

    async def send_data(self, websocket, data):
        """
        Attempt to send data to a websocket. Exceptions are logged but not raised.
        """
        try:
            await websocket.send_json(data)
        except Exception as e:
            console.log(e)
            console.log(f"Websocket connection broken for {websocket}.")
            raise e
