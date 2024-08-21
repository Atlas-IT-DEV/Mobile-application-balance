from pydantic import (BaseModel, Field, StrictStr, Json, condecimal,
                      StrictInt, BaseSettings, PrivateAttr, SecretBytes, StrictBytes)
from enum import Enum
from typing import Optional, List
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


class AuthJWT(BaseModel):
    private_key_path: Optional[str] = None
    public_key_path: Optional[str] = None
    _private_key_content: str = PrivateAttr()
    _public_key_content: str = PrivateAttr()
    access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire_days = REFRESH_TOKEN_EXPIRE_DAYS

    def __init__(self, **data):
        super().__init__(**data)
        self._private_key_content: Path = Path(__file__).resolve().parent.parent / "certs" / "jwt-private.pem"
        self._public_key_content: Path = Path(__file__).resolve().parent.parent / "certs" / "jwt-public.pem"

    @property
    def private_key_content(self):
        return self._private_key_content

    @property
    def public_key_content(self):
        return self._public_key_content


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    algoritm: str = "RS256"


class TokenInfo(BaseModel):
    """
    Model of token info
    """
    AccessToken: StrictBytes = Field(..., alias="access_token", example="awawfjbawhfbiawfb")
    RefreshToken: Optional[StrictBytes] = Field(None, alias="refresh_token", example="awdawdifbawifbai")
    Type: StrictStr = Field("Bearer", alias="token_type", example="Bearer")


class RoleEnum(StrictStr, Enum):
    """
    Model of role enum
    """
    user = 'user'
    admin = 'admin'


class Auth(BaseModel):
    """
    Model of auth
    """
    Phone: StrictStr = Field(..., alias="phone", example="79164928761")
    Password: StrictStr = Field(..., alias="password", example="<PASSWORD>")


class Image(BaseModel):
    """
    Model of image
    """
    ID: Optional[int] = Field(None, alias="id")
    Url: Optional[StrictStr] = Field(None, alias="url", example="https://example.com")


class User(BaseModel):
    """
    Model of user
    """
    ID: Optional[int] = Field(None, alias="id")
    FName: StrictStr = Field(..., alias="first_name", example="Рома")
    LName: StrictStr = Field(..., alias="last_name", example="Васненцев")
    Phone: StrictStr = Field(..., alias="phone", example="79164928761")
    INN: StrictStr = Field(..., alias="INN", example="94635796354")
    Password: StrictStr = Field(..., alias="password", example="jorog")
    Role: Optional[RoleEnum] = Field(RoleEnum.user, alias="role")


class FeeCategory(BaseModel):
    """
    Model of fee category
    """
    ID: Optional[int] = Field(None, alias="id")
    Name: StrictStr = Field(..., alias="name", example="Пожертвование")


class TypeSubEnum(StrictStr, Enum):
    """
    Model of type sub enum
    """
    day = 'DAY'
    month = 'MONTH'


class SubCategory(BaseModel):
    """
    Model of sub category
    """
    ID: Optional[int] = Field(None, alias="id")
    Type: TypeSubEnum = Field(..., alias="type", example="DAY")


class Fee(BaseModel):
    """
    Model of fee
    """
    ID: Optional[int] = Field(None, alias="id")
    Name: StrictStr = Field(..., alias="name", example="Сбор семье пенсионеров")
    Desc: Optional[StrictStr] = Field(None, alias="description", example="Семья состоит из 3 человек")
    FCost: condecimal(max_digits=10, decimal_places=2) = Field(..., alias="final_cost", example="100000")
    GCost: condecimal(max_digits=10, decimal_places=2) = Field(0, alias="gathered_cost", example="5000")
    CreatedAt: datetime = Field(datetime.now(), alias="created_at", example=datetime.now())
    FeeCategoryID: StrictInt = Field(..., alias="fee_category_id", example=3)
    SubCategoryID: StrictInt = Field(..., alias="sub_category_id", example=4)
    ImageID: StrictInt = Field(..., alias="image_id", example=3)


class Company(BaseModel):
    """
    Model of company
    """
    ID: Optional[int] = Field(None, alias="id")
    Name: StrictStr = Field(..., alias="name", example="Фонд Баланс")
    Desc: Optional[StrictStr] = Field(None, alias="description", example="Фонд служит для помощи нуждающимся")
    Contact: StrictStr = Field(..., alias="contact", example="@telegram")


class SubScript(BaseModel):
    """
    Model of subscriptions
    """
    ID: Optional[int] = Field(None, alias="id")
    UserID: StrictInt = Field(..., alias="user_id", example=1)
    TableID: StrictInt = Field(..., alias="fee_id", example=3)


class HistoryPay(BaseModel):
    """
    Model of history payments
    """
    ID: Optional[int] = Field(None, alias="id")
    UserID: StrictInt = Field(..., alias="user_id", example=1)
    FeeID: StrictInt = Field(..., alias="fee_id", example=3)
    Pay: condecimal(max_digits=10, decimal_places=2) = Field(..., alias="pay", example="1000")
    CreatedAt: datetime = Field(datetime.now(), alias="created_at", example=datetime.now())
