from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile, Body, Header, status
from src.database.my_connector import Database
from src.service import user_services, auth_services
from typing import Dict
from fastapi.openapi.models import Tag
from src.database.models import User, Auth, TokenInfo
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from src.utils.jwt_bearer import JWTBearer
from jwt import InvalidTokenError
from src.utils.custom_logging import setup_logging
from dotenv import load_dotenv
load_dotenv()
log = setup_logging()


db = Database()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Определяем теги
TestTag = Tag(name="Test", description="Route for testing")
AuthTag = Tag(name="Auth", description="Registration and authorization")
# ImageServiceTag = Tag(name="ImageService", description="Upload/download image for object")
UserTag = Tag(name="User", description="CRUD operations user")
# CategoryTag = Tag(name="Category", description="CRUD operations category")
# CharacteristicTag = Tag(name="Characteristic", description="CRUD operations characteristic")
# CompanyTag = Tag(name="Company", description="CRUD operations company")
# ImageTag = Tag(name="Image", description="CRUD operations image")
# ProductCommentTag = Tag(name="ProductComment", description="CRUD operations order comment")
# OrderProductTag = Tag(name="OrderProduct", description="CRUD operations order product")
# OrderTag = Tag(name="Order", description="CRUD operations order")
# ProductCharacteristicTag = Tag(name="ProductCharacteristic", description="CRUD operations  product characteristic")
# ProductTag = Tag(name="Product", description="CRUD operations product")

# Настройка документации с тегами
app.openapi_tags = [
    TestTag.dict(),
    AuthTag.dict(),
    # ImageServiceTag.dict(),
    UserTag.dict(),
    # CategoryTag.dict(),
    # CharacteristicTag.dict(),
    # CompanyTag.dict(),
    # ImageTag.dict(),
    # ProductCommentTag.dict(),
    # OrderProductTag.dict(),
    # OrderTag.dict(),
    # ProductCharacteristicTag.dict(),
    # ProductTag.dict()
]


@app.get("/", response_model=Dict, tags=["Test"])
async def Test():
    """
    Route for test.

    :return: response model None.
    """
    return {"Test": "Normaly Work"}


@app.get("/users/", response_model=list[User], tags=["User"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def get_all_users():
    """
    Route for get all users from basedata.

    :return: response model List[Users].
    """
    try:
        return user_services.get_all_users()
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.get("/users/id/{user_id}", response_model=User, tags=["User"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def get_user_by_id(user_id: int):
    """
    Route for get user by UserID.

    :param user_id: ID by user. [int]

    :return: response model Users.
    """
    try:
        return user_services.get_user_by_id(user_id)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.get("/users/phone/{phone}", response_model=User, tags=["User"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def get_user_by_phone(phone: str):
    """
    Route for get user by user phone.

    :param phone: Phone by user. [str]

    :return: response model Users.
    """
    try:
        return user_services.get_user_by_phone(phone)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.post("/users/", response_model=User, tags=["User"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_user(user: User):
    """
    Route for create user in basedata.

    :param user: Model user. [Users]

    :return: response model Users.
    """
    try:
        return user_services.create_user(user)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.put("/users/{user_id}", response_model=Dict, tags=["User"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_user(user_id, user: User):
    """
    Route for update user in basedata.

    :param user_id: ID by user. [int]

    :param user: Model user. [Users]

    :return: response model dict.
    """
    try:
        return user_services.update_user(user_id, user)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.delete("/users/{user_id}", response_model=Dict, tags=["User"],
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_user(user_id):
    """
    Route for delete user from basedata.

    :param user_id: ID by user. [int]

    :return: response model dict.
    """
    try:
        return user_services.delete_user(user_id)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.post("/signup/", response_model=TokenInfo, tags=["Auth"])
async def signup(user: User = Depends(auth_services.validate_reg_user)):
    """
    Route for user registration.

    :param phone: Phone number user. [Str]

    :param password: Password user. [Str]

    :return: response model User.
    """
    try:
        return auth_services.signup(user)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.post("/signin/", response_model=TokenInfo, tags=["Auth"])
async def signin(user: User = Depends(auth_services.validate_auth_user)):
    """
    Route for user authorization.

    :param user: Model User. [User]

    :return: response model User.
    """
    try:
        return auth_services.signin(user)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.post("/auth_refresh_jwt/", response_model=TokenInfo, response_model_exclude_none=True,
          dependencies=[Depends(JWTBearer(access_level=1))], tags=["Auth"])
async def auth_refresh_jwt(user: User = Depends(auth_services.UserGetFromToken("refresh_token_type"))):
    """
    Route for refresh jwt access token.

    :param token: valid refresh token. [Str]

    :return: response model TokenInfo.
    """
    try:
        return auth_services.auth_refresh_jwt(user)
    except HTTPException as ex:
        log.exception(ex)
        raise ex


@app.get("/get_current_auth_user/", response_model=User, dependencies=[Depends(JWTBearer(access_level=1))],
         tags=["Auth"])
async def get_current_auth_user(user: User = Depends(auth_services.UserGetFromToken("access_token_type"))):
    """
    Route for getting auth user.

    :param token: valid token. [Str]

    :return: response model User.
    """
    try:
        return user
    except HTTPException as ex:
        log.exception(ex)
        raise ex


if __name__ == "__main__":
    import uvicorn
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
