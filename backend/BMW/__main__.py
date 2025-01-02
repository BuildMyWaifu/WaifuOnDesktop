import traceback
from contextlib import asynccontextmanager
from multiprocessing import Manager
from typing import Annotated
from pathlib import Path
import zipfile
import os
import BMW.Manager
import BMW.model
import git
import secrets

from BMW import POSSIBLE_COLLECTION_NAME_LOWERCASE

BMW.Manager.connection_manager = BMW.Manager.ConnectionManager(Manager().dict())

# from BMW.config import config
from BMW.Manager import connection_manager, websocket_manager
from BMW.model import ChatRoom, Document, File, Message, Payload, User, Companion
from BMW.Process import BackgroundProcess
from BMW.Thread import DeliveryThread
from BMW.utils import console, checkIfPathSafe, getFullPath
from BMW.LLMCore import generateResponseMessage
from fastapi import (
    Cookie,
    Depends,
    UploadFile,
    FastAPI,
    HTTPException,
    Request,
    Response,
    WebSocket,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.websockets import WebSocketDisconnect

# from starlette.requests import Request


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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


async def get_current_user(token: str = Depends(oauth2_scheme),) -> User:
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
        return Payload.success("登入成功", user.token)
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
    # TODO: 建立預設伴侶

    await user.update_token()
    await user.set_password(payload.password)
    return Payload.success("註冊成功", user.token)


class MessageCreatePayload(BaseModel):
    companionId: str
    content: str


@app.post("/message")
async def create_message(
    payload: MessageCreatePayload,
    user: User = Depends(get_current_user),
):
    companion = await Companion.find(_id=payload.companionId)
    if not companion:
        raise HTTPException(404, "找不到這個伴侶")
    if companion.userId != user.id:
        raise HTTPException(403, "您沒有權限發送訊息")

    await Message.empty(
        role='user',
        companionId=payload.companionId,
        content=payload.content,
        ).create()
    message = await generateResponseMessage(companion)
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
):
    companions = await Companion.find_any(userId=user.id)
    return Payload.success(
        "成功獲取伴侶列表", [await companion.get_dict(user) for companion in companions]
    )


@app.get("/companion/{companion_id}")
async def get_companion(
    companion_id: str,
    user: User = Depends(get_current_user),
):
    companion = await Companion.find(_id=companion_id)
    if not companion:
        raise HTTPException(404, "找不到這個伴侶")
    if companion.userId != user.id:
        raise HTTPException(403, "您沒有權限查看這個伴侶")
    return Payload.success("成功獲取伴侶資料", await companion.get_dict(user))


class CompanionEditPayload(BaseModel):
    name: str | None = None
    description: str | None = None
    live2dModelSettingPath: str | None = None
    poseMap: dict[str, dict[str, str]] | None = None
    backstory: str | None = None


@app.patch("/companion/{companion_id}")
async def patch_companion(
    companion_id: str,
    payload: CompanionEditPayload,
    user: User = Depends(get_current_user),
):
    companion = await Companion.find(_id=companion_id)
    if not companion:
        raise HTTPException(404, "找不到這個伴侶")
    if companion.userId != user.id:
        raise HTTPException(403, "您沒有權限編輯這個伴侶")
    
    if payload.live2dModelSettingPath and not checkIfPathSafe(payload.live2dModelSettingPath):
        raise HTTPException(500, "不合法的Live2dModel路徑")
    raw_update_payload = payload.model_dump(exclude_unset=True)
    update_payload = {}
    for key, value in raw_update_payload.items():
        if value is not None and value != getattr(companion, key):
            update_payload[key] = value
    
    if payload.backstory:
        update_payload['trait'] = None
    await companion.update(**update_payload)
    return Payload.success("成功編輯伴侶", await companion.get_dict(user))


class CompanionCreatePayload(BaseModel):
    name: str
    description: str 
    live2dModelSettingPath: str 
    poseMap: dict[str, dict[str, str]] = {}
    backstory: str

@app.post("/companion")
async def create_companion(
    payload: CompanionCreatePayload,
    user: User = Depends(get_current_user),
):
    if not checkIfPathSafe(payload.live2dModelSettingPath):
        raise HTTPException(500, "不合法的Live2dModel路徑")
    companion = Companion.empty(**payload.model_dump(), userId=user.id)
    await companion.create()
    return Payload.success("成功創建伴侶", await companion.get_dict(user))

@app.delete("/companion/{companion_id}")
async def delete_companion(
    companion_id: str,
    user: User = Depends(get_current_user),
):
    companion = await Companion.find(_id=companion_id)
    if not companion:
        raise HTTPException(404, "找不到這個伴侶")
    if companion.userId != user.id:
        raise HTTPException(403, "您沒有權限刪除這個伴侶")
    await companion.update(deleted=True)
    return Payload.success("成功刪除伴侶")


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


"""
/assets/live2dModel/public/mao
                          /miku
                          ...
                   /<userId>
                   



"""

@app.post("/assets/live2dModel/upload")
async def upload_live2d_model(file: UploadFile, user: User = Depends(get_current_user)):
    # 定義解壓縮目標目錄
    target_directory = Path(
        f"./assets/live2dModel/{user.id}/{secrets.token_urlsafe(8)}"
    )

    # 確保目標目錄存在
    target_directory.mkdir(parents=True, exist_ok=True)

    # 確定檔案是否為 zip 檔
    if not file.filename.endswith(".zip"):
        return Payload.error("僅接受 .zip 格式的檔案")

    # 儲存上傳的 zip 檔
    zip_path = target_directory / file.filename
    with open(zip_path, "wb") as f:
        f.write(await file.read())

    # 解壓縮 zip 檔
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_directory)
        # 解壓縮成功後刪除原始 zip 檔案
        zip_path.unlink()
    except zipfile.BadZipFile:
        return Payload.error("無法解壓縮，檔案可能已損壞")

    # 尋找符合條件的檔案
    model_json_path = None
    for root, _, files in os.walk(target_directory):
        for file_name in files:
            if file_name.endswith(".model3.json"):
                model_json_path = str(Path(root) / file_name)
                break
        if model_json_path:
            break

    if model_json_path:
        return Payload.success("成功上傳並找到符合條件的文件", "/api/"+model_json_path)
    else:
        return Payload.error("未找到符合條件的 .model3.json 文件")


@app.get("/assets/{file_path:path}")
async def read_assets(file_path: str):
    # 定義根目錄

    if not checkIfPathSafe(file_path):
        raise HTTPException(403, "不合法的路徑")
    
    full_path = getFullPath(file_path)
    # 檢查文件是否存在
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail="文件不存在")

    # 返回文件回應
    return FileResponse(full_path)


@app.get("/version")
async def get_version():
    repo = git.Repo(search_parent_directories=True)
    return Payload.success("成功獲得後端版本", repo.git.describe())


@app.api_route("/{full_path:path}")
async def handle_404_route(full_path: str, request: Request):
    console.log(full_path)
    raise HTTPException(404, f"未知的路徑或資源 {request.method} {request.url}")
