
from fastapi import WebSocket
class WebsocketManager:
    
    websocket_dict: dict[str, list[WebSocket]] = {}  # userId: WebSocket[]
    
    def __init__(self) -> None:
        pass
    
    
    def regist(self, userId, websocket: WebSocket):
        if (self.websocket_dict.get(userId) == None) :
            self.websocket_dict[userId] = []
        self.websocket_dict[userId].append(websocket)
    
    def unregist(self, userId):
        ...
    
    
websocket_manager = WebsocketManager()