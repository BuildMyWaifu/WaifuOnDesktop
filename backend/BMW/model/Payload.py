from typing import Literal, Union

from pydantic import BaseModel


class Payload(BaseModel):
    status: Literal["success", "info", "warning", "error"]
    message: str = ""
    data: Union[dict, list, None, str] = None

    @classmethod
    def success(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="success", message=message, data=data)

    @classmethod
    def info(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="info", message=message, data=data)

    @classmethod
    def warning(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="warning", message=message, data=data)

    @classmethod
    def error(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="error", message=message, data=data)

