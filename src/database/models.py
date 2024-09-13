from pydantic import (BaseModel, Field, StrictStr, Json, condecimal,
                      StrictInt, PrivateAttr, SecretBytes, StrictBytes, StrictBool, root_validator)
from pydantic_settings import BaseSettings
from enum import Enum
from typing import Optional, List, ClassVar
from datetime import datetime
import os
from pathlib import Path
from config import Config

config = Config()

ACCESS_TOKEN_EXPIRE_MINUTES = int(config.__getattr__("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(config.__getattr__("REFRESH_TOKEN_EXPIRE_DAYS"))


class AuthJWT(BaseModel):
    private_key_path: Optional[str] = None
    public_key_path: Optional[str] = None
    _private_key_content: str = PrivateAttr()
    _public_key_content: str = PrivateAttr()
    access_token_expire_minutes: ClassVar[int] = ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire_days: ClassVar[int] = REFRESH_TOKEN_EXPIRE_DAYS

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
    Model of information about token
    """
    AccessToken: StrictStr = Field(...,
                                   alias="access_token")
    RefreshToken: Optional[StrictStr] = Field(None,
                                              alias="refresh_token")
    Type: StrictStr = Field("Bearer",
                            alias="token_type")


class RoleEnum(StrictStr, Enum):
    """
    Model of role enum
    """
    user = 'USER'
    admin = 'ADMIN'


class Auth(BaseModel):
    """
    Model of auth
    """
    Phone: StrictStr = Field(...,
                             alias="phone",
                             examples=["79164928761"])
    Password: StrictStr = Field(...,
                                alias="password",
                                examples=["<PASSWORD>"])


class Users(BaseModel):
    """
    Model of user
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    FName: StrictStr = Field(...,
                             alias="first_name",
                             examples=["Рома"])
    LName: StrictStr = Field(...,
                             alias="last_name",
                             examples=["Васненцев"])
    Phone: StrictStr = Field(...,
                             alias="phone",
                             examples=["79164928761"])
    INN: StrictStr = Field(...,
                           alias="INN",
                           examples=["94635796354"])
    Password: StrictStr = Field(...,
                                alias="password",
                                examples=["<PASSWORD>"])
    DateReg: Optional[datetime] = Field(datetime.now(),
                                        alias="created_at",
                                        examples=[f"{datetime.now()}"])
    Role: Optional[RoleEnum] = Field(RoleEnum.user,
                                     alias="role",
                                     examples=["USER"])


class FeeCategories(BaseModel):
    """
    Model of fee category
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    Name: StrictStr = Field(...,
                            alias="name",
                            examples=["Пожертвование"])


class SubCategories(BaseModel):
    """
    Model of sub category
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    Type: StrictStr = Field(...,
                            alias="type",
                            examples=["DAY"])


class Fees(BaseModel):
    """
    Model of fee
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    Name: StrictStr = Field(...,
                            alias="name",
                            examples=["Сбор семье пенсионеров"])
    Desc: Optional[StrictStr] = Field(None,
                                      alias="description",
                                      examples=["Семья состоит из 3 человек"])
    FCost: condecimal(max_digits=10, decimal_places=2) = Field(...,
                                                               alias="final_cost",
                                                               examples=["100000"])
    GCost: condecimal(max_digits=10, decimal_places=2) = Field(0,
                                                               alias="gathered_cost",
                                                               examples=["5000"])
    CreatedAt: Optional[datetime] = Field(datetime.now(),
                                          alias="created_at",
                                          examples=[f"{datetime.now()}"])
    FeeCategoryID: StrictInt = Field(...,
                                     alias="fee_category_id",
                                     examples=[3])
    ImageUrl: Optional[StrictStr] = Field(None,
                                          alias="image_url",
                                          examples=["http://example.png"])


class Companies(BaseModel):
    """
    Model of company
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    Name: StrictStr = Field(...,
                            alias="name",
                            examples=["Фонд Баланс"])
    Desc: Optional[StrictStr] = Field(None,
                                      alias="description",
                                      examples=["Фонд служит для помощи нуждающимся"])
    Contact: StrictStr = Field(...,
                               alias="contact",
                               examples=["@telegram"])


class SubScripts(BaseModel):
    """
    Model of subscriptions
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    UserID: StrictInt = Field(...,
                              alias="user_id",
                              examples=[1])
    FeeID: StrictInt = Field(...,
                             alias="fee_id",
                             examples=[3])
    TypeID: StrictInt = Field(...,
                              alias="type_sub_id",
                              examples=[5])


class HistoryPays(BaseModel):
    """
    Model of history payments
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    UserID: StrictInt = Field(...,
                              alias="user_id",
                              examples=[1])
    FeeID: StrictInt = Field(...,
                             alias="fee_id",
                             examples=[3])
    Pay: condecimal(max_digits=10, decimal_places=2) = Field(...,
                                                             alias="pay",
                                                             examples=[1000])
    CreatedAt: Optional[datetime] = Field(datetime.now(),
                                          alias="created_at",
                                          examples=[f"{datetime.now()}"])

# TODO FAILED test_main.py::test_update_entity[subscription-subscriptions-update_data6]
#  - pymysql.err.DataError: (1366, "Incorrect integer value: 'annotation=NoneType required=True
#  alias='fee_id' alias_pri ->
#  Где-то при инициализации модели может быть опечатка, в этом случае была лишняя запятая
