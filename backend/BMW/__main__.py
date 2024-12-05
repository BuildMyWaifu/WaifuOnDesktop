import io
import traceback
from contextlib import asynccontextmanager
from multiprocessing import Manager
from typing import Annotated

import BMW.Manager
import BMW.model
import git
from BMW import POSSIBLE_COLLECTION_NAME_LOWERCASE

# from BMW.config import config
from BMW.Manager import connection_manager, websocket_manager
from BMW.model import ChatRoom, Document, File, Message, Payload, User
from BMW.model.Message import MessageCreatePayload
from BMW.Process import BackgroundProcess
from BMW.Thread import DeliveryThread
from BMW.utils import console
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    UploadFile,
    WebSocket,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.websockets import WebSocketDisconnect

# from starlette.requests import Request


BMW.Manager.connection_manager = BMW.Manager.ConnectionManager(Manager().dict())


lower_collection_name2object: dict[POSSIBLE_COLLECTION_NAME_LOWERCASE, Document] = {
    "user": User,
    "file": File,
    "chatroom": ChatRoom,
    "message": Message,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    process_list = [
        BackgroundProcess(connection_manager),
    ]

    thread_list = [
        DeliveryThread(
            connection_manager=connection_manager, websocket_manager=websocket_manager
        )
    ]

    for p in process_list:
        p.start()
    for t in thread_list:
        t.start()
    yield
    for p in process_list:
        p.terminate()
    for t in thread_list:
        t.terminate()


class RewritePathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Rewrite the path
        if request.url.path.startswith("/api"):
            modified_path = request.url.path[len("/api") :]
            request.scope["path"] = modified_path
        response = await call_next(request)
        return response


app = FastAPI(lifespan=lifespan)
app.add_middleware(RewritePathMiddleware)


@app.exception_handler(RequestValidationError)
async def not_found_exception_handler(request, exc: RequestValidationError):
    console.log(exc.errors())
    return JSONResponse(
        content=Payload.error(
            f"不合法的請求參數 {' '.join([e.get('msg') if e.get('msg') else ''  + ' Input: '+ e.get('input') if e.get('input') else '' for e in exc.errors()])}"
        ).model_dump(),
        status_code=422,
    )


@app.exception_handler(405)
async def wrong_method_exception_handler(request, exc):
    return JSONResponse(
        content=Payload.error(
            f"不合法的方法 {request.method} {request.url}"
        ).model_dump(),
        status_code=405,
    )


@app.exception_handler(HTTPException)
async def custom_exception_handler(request, exc):
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        return JSONResponse(
            content=Payload.error(str(exc.detail)).model_dump(), status_code=status_code
        )
    return JSONResponse(
        content=Payload.error("未知的錯誤").model_dump(), status_code=status_code
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    console.log("".join(traceback.format_exception(exc)))
    return JSONResponse(
        content=Payload.error(f"{exc}").model_dump(),
        status_code=500,
    )


async def get_current_user(
    token: Annotated[str | None, Cookie()] = None,
) -> User:
    if token:
        user = await User.find(token=token)
        if user:
            return user
        else:
            raise HTTPException(status_code=401, detail="登入已過期，請重新登入")
    raise HTTPException(status_code=401, detail="授權失效，請重新登入")


@app.get("/test")
async def test_endpoint():
    return Payload.success("測試成功")


@app.get("/me")
async def get_user_me(user: User = Depends(get_current_user)):
    return Payload.success("成功獲取帳號資料", user.safe_dict())


class UserLoginPayload(BaseModel):
    email: str
    password: str


@app.post("/login")
async def login(payload: UserLoginPayload, response: Response, request: Request):
    user = await User.find(**{"profile.email": payload.email})
    if not user:
        raise HTTPException(404, "找不到這個使用者")
    if user.check_password(payload.password):
        response.set_cookie(key="token", value=user.token)

        return Payload.success("登入成功", user.safe_dict())
    else:
        raise HTTPException(500, "密碼錯誤")


class UserSignUpPayload(BaseModel):
    name: str
    email: str
    password: str


@app.post("/signup")
async def registration(payload: UserSignUpPayload, response: Response):
    if await User.find(**{"profile.email": payload.email}):
        raise HTTPException(500, "這個信箱已被使用")

    user = User.empty()
    user.profile.name = payload.name
    user.profile.email = payload.email
    await user.create()

    await user.update_token()
    await user.set_password(payload.password)
    response.set_cookie(key="token", value=user.token)
    return Payload.success("註冊成功", user.safe_dict())


@app.post("/message")
async def create_message(
    payload: MessageCreatePayload,
    user: User = Depends(get_current_user),
):
    message = Message.empty(**payload.model_dump())
    await message.create()
    return Payload.success("成功發送訊息", await message.get_dict(user))


@app.get("/message/{companion_id}")
async def list_message(
    companion_id: str,
    before: int | None = None,
    after: int | None = None,
    limit: int = 50,
    offset: int = 0,
    user: User = Depends(get_current_user),
):
    messages = await Message.find_any(
        companionId=companion_id, limit=limit, offset=offset
    )
    return Payload.success(
        "成功獲取訊息列表", [await message.get_dict(user) for message in messages]
    )


@app.get("/companion")
async def list_companion(
    user: User = Depends(get_current_user),
): ...


@app.get("/companion/{companion_id}")
async def get_companion(
    companion_id: str,
    user: User = Depends(get_current_user),
): ...


@app.patch("/companion/{companion_id}")
async def patch_companion(
    companion_id: str,
    user: User = Depends(get_current_user),
): ...


@app.delete("/companion/{companion_id}")
async def delete_companion(
    companion_id: str,
    user: User = Depends(get_current_user),
): ...


@app.get("/user/{user_id}")
async def get_user_by_id(user_id: str, user: User = Depends(get_current_user)):
    target_user = await User.find(_id=user_id)
    if not target_user:
        raise HTTPException(404, "找不到此使用者")

    return Payload.success("成功獲取使用者資料", await target_user.get_dict(user))


class UserSetPasswordPayload(BaseModel):
    password: str


@app.post("/user/{user_id}/password")
async def user_password_set(
    data: UserSetPasswordPayload, user_id: str, user: User = Depends(get_current_user)
):
    target_user = await User.find(_id=user_id)
    if await target_user.check_permission(user):
        await target_user.set_password(data.password)
        await target_user.update_token()
        return Payload.success("成功編輯使用者密碼")
    raise HTTPException(403, "您沒有權限重設這個使用者的密碼")


@app.get("/user/{user_id}/token/reset")
async def user_token_reset(user_id: str, user: User = Depends(get_current_user)):
    target_user = await User.find(_id=user_id)
    if await target_user.check_permission(user):
        await target_user.update_token()
        return Payload.success("成功重設使用者 token")
    raise HTTPException(403, "您沒有權限重設這個使用者的 token")


@app.post("/file")
async def create_upload_file(file: UploadFile, user: User = Depends(get_current_user)):
    # console.log(upload_file)
    if user.level < 0:
        raise HTTPException(403, "您沒有權限上傳檔案")
    file_document = await File.from_file(file)
    file_id = await file_document.create()
    return Payload.success("成功上傳檔案", file_id)


@app.get("/file/{file_id}")
async def get_file_info_by_id(file_id: str, user: User = Depends(get_current_user)):
    if user.level < 0:
        raise HTTPException(403, "您沒有權限取得檔案資訊")
    file = await File.find(_id=file_id)
    return Payload.success("成功獲得檔案資訊", file.safe_dict())


@app.get("/file/{file_id}/download")
async def download_file_by_id(file_id: str, user: User = Depends(get_current_user)):
    if user.level < 0:
        raise HTTPException(403, "您沒有權限下載檔案")

    file = await File.find(_id=file_id)
    file_stream = io.BytesIO(file.data)

    response = StreamingResponse(file_stream)

    try:
        response.headers["Content-Disposition"] = (
            f"attachment; filename={file.filename}"
        )
    except UnicodeEncodeError:
        response.headers["Content-Disposition"] = (
            f"attachment; filename={file_id}.{file.filename.split('.')[-1]}"
        )

    return response


@app.get("/version")
async def get_version():
    repo = git.Repo(search_parent_directories=True)
    return Payload.success("成功獲得後端版本", repo.git.describe())


@app.websocket("/api/ws")
async def websocket_endpoint(
    websocket: WebSocket, user: User = Depends(get_current_user)
):
    # read message from connection_manager, and send to websocket
    # read from websocket, send to connecion_manager

    await websocket.accept()
    await websocket.send_json(
        {"type": "snackbar", "data": Payload.success("連線成功").model_dump()}
    )

    websocket_manager.regist(userId=user.id, websocket=websocket)
    try:
        while True:
            await websocket.receive_json()
            # should not recv anything from client

    except WebSocketDisconnect:
        websocket_manager.unregist(userId=user.id)


# class SearchPayload(BaseModel):
#     filter: dict = {}
#     sort: dict = {}


# @app.post("/{collection_name}/search")
# async def search_document(
#     collection_name: POSSIBLE_COLLECTION_NAME_LOWERCASE,
#     payload: SearchPayload,
#     user: User = Depends(get_current_user),
#     offset: int = 0,
#     limit: int = 50,
# ):
#     Object = lower_collection_name2object[collection_name]
#     if not await Object.check_search_permission(user):
#         raise HTTPException(403, "無搜索此類別的權限")
#     filter_payload, sort_payload = await Object.validate_search(
#         user=user, sort=payload.sort, filter=payload.filter
#     )
#     console.log(filter_payload)
#     console.log(sort_payload)

#     return Payload.success(
#         "成功加載資料",
#         [
#             await document.get_dict(user)
#             for document in await Object.find_any(
#                 skip=offset,
#                 limit=limit,
#                 sort=list(sort_payload.items()),
#                 **filter_payload,
#             )
#         ],
#     )


# @app.get("/{collection_name}/{document_id}")
# async def get_document(
#     collection_name: POSSIBLE_COLLECTION_NAME_LOWERCASE,
#     document_id: str,
#     user: User = Depends(get_current_user),
# ):
#     Object = lower_collection_name2object[collection_name]
#     document = await Object.find(_id=document_id)
#     if not document:
#         raise HTTPException(404, "找不到此文件")

#     output_dict = await document.get_dict(user)
#     if output_dict:
#         return Payload.success("成功存取資料", output_dict)
#     else:
#         raise HTTPException(403, "無存取此文件的權限")


# @app.post("/{collection_name}")
# async def create_document(
#     collection_name: POSSIBLE_COLLECTION_NAME_LOWERCASE,
#     dict_payload: dict,
#     user: User = Depends(get_current_user),
# ):
#     console.log(dict_payload)
#     Object = lower_collection_name2object[collection_name]
#     if not issubclass(Object, Editable):
#         raise HTTPException(500, "該類型不支援創建")
#     if not await Object.check_create_permission(user):
#         raise HTTPException(403, "無建立此類型文件的權限")

#     create_payload = await Object.validate_create(user=user, create=dict_payload)

#     document = Object.empty(**create_payload)
#     await document.create()
#     return Payload.success("成功創建文件", await document.get_dict(user))


# # @app.patch("/{collection_name}/{document_id}")
# # async def update_document(
# #     collection_name: POSSIBLE_COLLECTION_NAME_LOWERCASE,
# #     document_id: str,
# #     dict_payload: dict,
# #     user: User = Depends(get_current_user),
# # ):
# #     Object = lower_collection_name2object[collection_name]
# #     document = await Object.find(_id=document_id)

# #     if not document:
# #         raise HTTPException(404, "找不到此文件")

# #     if not isinstance(document, Editable):
# #         raise HTTPException(500, "該類型不支援編輯")

# #     if not await document.check_permission(user):
# #         raise HTTPException(403, "無存取此文件的權限")

# #     update_payload = await document.validate_update(user=user, update=dict_payload)

# #     await document.update(**update_payload, )
# #     return Payload.success("成功更新文件", await document.get_dict(user))


# @app.delete("/{collection_name}/{document_id}")
# async def delete_document(
#     collection_name: POSSIBLE_COLLECTION_NAME_LOWERCASE,
#     document_id: str,
#     user: User = Depends(get_current_user),
# ):
#     Object = lower_collection_name2object[collection_name]
#     document = await Object.find(_id=document_id)

#     if not document:
#         raise HTTPException(404, "找不到此文件")

#     if not isinstance(document, Editable):
#         raise HTTPException(500, "該類型不支援刪除")

#     await document.validate_delete(user)

#     await document.update(deleted=True)
#     return Payload.success("成功刪除文件")


@app.api_route("/{full_path:path}")
async def handle_404_route(full_path: str, request: Request):
    console.log(full_path)
    raise HTTPException(404, f"未知的路徑或資源 {request.method} {request.url}")
