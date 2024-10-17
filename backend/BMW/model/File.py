from starlette.datastructures import UploadFile

from .Editable import Editable
from .User import User



class File(Editable):
    collection_name: str = "File"
    filename: str = None
    data: bytes = None
    size: int = None
    contentType: str = None
    # extension: str = None

    async def check_permission(self, user: User) -> bool:
        return NotImplemented

    def safe_dict(self):
        self_dict = self.model_dump(
            exclude={"collection_name", "data"},
            by_alias=True,
            exclude_none=True,
        )
        return self_dict

    @classmethod
    async def check_create_permission(cls, user: User) -> bool:
        ...
    
    @classmethod
    async def check_search_permission(cls, user: User) -> bool:
        ...

    @classmethod
    def empty(cls) -> "File":
        return NotImplemented

    @classmethod
    async def from_file(cls, file: UploadFile) -> "File":
        return File(
            filename=file.filename,
            data=await file.read(),
            size=file.size,
            contentType=file.content_type,
        )
