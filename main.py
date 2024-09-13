from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile, Body, Header, status, Form
from src.database.my_connector import Database
from src.service import (user_services, auth_services, fee_category_services,
                         company_services, sub_category_services, fee_services,
                         subscription_services, history_payment_services, file_services)
from typing import Dict
from fastapi.openapi.models import Tag
from src.database.models import (Users, TokenInfo, AuthJWT, FeeCategories, Companies,
                                 SubCategories, Fees, SubScripts, HistoryPays)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from src.utils.jwt_bearer import JWTBearer
from jwt import InvalidTokenError
from src.utils.custom_logging import setup_logging
from config import Config
from fastapi.staticfiles import StaticFiles

config = Config()
log = setup_logging()
app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Определяем теги
AuthTag = Tag(name="Auth", description="Registration and authorization")
ImageServiceTag = Tag(name="ImageService", description="Upload/download image for object")
UserTag = Tag(name="User", description="CRUD operations user")
FeeCategoryTag = Tag(name="FeeCategory", description="CRUD operations fee category")
SubCategoryTag = Tag(name="SubCategory", description="CRUD operations sub category")
SubscriptionTag = Tag(name="Subscription", description="CRUD operations subscription")
HistoryPaymentTag = Tag(name="HistoryPayment", description="CRUD operations history payment")
CompanyTag = Tag(name="Company", description="CRUD operations company")
FeeTag = Tag(name="Fee", description="CRUD operations fee")

# Настройка документации с тегами
app.openapi_tags = [
    AuthTag.model_dump(),
    ImageServiceTag.model_dump(),
    UserTag.model_dump(),
    FeeCategoryTag.model_dump(),
    SubCategoryTag.model_dump(),
    SubscriptionTag.model_dump(),
    HistoryPaymentTag.model_dump(),
    CompanyTag.model_dump(),
    FeeTag.model_dump()
]


@app.post("/signup/", response_model=TokenInfo, tags=["Auth"])
async def signup(user: Users = Depends(auth_services.validate_reg_user)):
    """
    Route for user registration.

    :param user: Model of user. [Users]

    :return: response model TokenInfo.
    """
    try:
        return auth_services.signup(user)
    except HTTPException as ex:
        log.exception(f"Error {ex}")
        raise ex


@app.post("/signin/", response_model=TokenInfo, tags=["Auth"])
async def signin(user: Users = Depends(auth_services.validate_auth_user)):
    """
    Route for user authorization.

    :param auth: Model of auth. [Auth]

    :return: response model TokenInfo.
    """
    try:
        return auth_services.signin(user)
    except HTTPException as ex:
        log.exception(f"Error {ex}")
        raise ex


@app.post("/auth_refresh_jwt/", response_model=TokenInfo, response_model_exclude_none=True,
          dependencies=[Depends(JWTBearer(access_level=1))], tags=["Auth"])
async def auth_refresh_jwt(user: Users = Depends(auth_services.UserGetFromToken("refresh_token_type"))):
    """
    Route for refresh jwt access token.

    :param token: valid refresh token. [Str]

    :return: response model TokenInfo.
    """
    try:
        return auth_services.auth_refresh_jwt(user)
    except HTTPException as ex:
        log.exception(f"Error {ex}")
        raise ex


@app.get("/get_current_auth_user/", response_model=Users, dependencies=[Depends(JWTBearer(access_level=1))],
         tags=["Auth"])
async def get_current_auth_user(user: Users = Depends(auth_services.UserGetFromToken("access_token_type"))):
    """
    Route for getting auth user.

    :param token: valid token. [Str]

    :return: response model User.
    """
    try:
        return user
    except HTTPException as ex:
        log.exception(f"Error {ex}")
        raise ex


@app.post("/image_upload/fee", response_model=Fees, tags=["ImageService"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def image_upload_fee(file: UploadFile = File(...), fee_id: int = Form(...)):
    """
   Route for uploading multiple images for a fee.

   :return: response model product [Fees].
   """
    try:
        return await file_services.upload_images(
            entity_type="fee",
            file=file,
            entity_id=fee_id,
            get_entity_by_id=fee_services.get_fee_by_id,
            update_entity=fee_services.update_fee)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/image_delete/fee", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def image_delete_fee(fee_id: int):
    """
   Route for delete fee into basedata.

   :return: response model Dict.
   """
    try:
        return file_services.delete_images(entity_type="fee",
                                           entity_id=fee_id,
                                           get_entity_by_id=fee_services.get_fee_by_id,
                                           update_entity=fee_services.update_fee)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/users/", response_model=list[Users], tags=["User"])
async def get_all_users():
    """
    Route for get all users from basedata.

    :return: response model List[Users].
    """
    try:
        return user_services.get_all_users()
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/users/user_id/{user_id}", response_model=Users, tags=["User"])
async def get_user_by_id(user_id: int):
    """
    Route for get user by UserID.

    :param user_id: ID by user. [int]

    :return: response model Users.
    """
    try:
        return user_services.get_user_by_id(user_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/users/phone/{phone}", response_model=Users, tags=["User"])
async def get_user_by_phone(phone: str):
    """
    Route for get user by user phone.

    :param phone: phone by user. [int]

    :return: response model Users.
    """
    try:
        return user_services.get_user_by_phone(phone)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.post("/users/", response_model=Users, tags=["User"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_user(user: Users):
    """
    Route for create user in basedata.

    :param user: Model user. [Users]

    :return: response model Users.
    """
    try:
        return user_services.create_user(user)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.put("/users/{user_id}", response_model=Dict, tags=["User"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_user(user_id, user: Users):
    """
    Route for update user in basedata.

    :param user_id: ID by user. [int]

    :param user: Model user. [Users]

    :return: response model dict.
    """
    try:
        return user_services.update_user(user_id, user)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/users/{user_id}", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_user(user_id):
    """
    Route for delete user in basedata.

    :param user_id: ID by user. [int]

    :return: response model dict.
    """
    try:
        return user_services.delete_user(user_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/fees/", response_model=list[Fees], tags=["Fee"])
async def get_all_fees():
    """
    Route for getting all fees from basedata.

    :return: response model List[Fees].
    """
    try:
        return fee_services.get_all_fees(dirs=False)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/fees/full", response_model=list[Dict], tags=["Fee"])
async def get_all_fees():
    """
    Route for getting all fees from basedata.

    :return: response model List[Fees].
    """
    try:
        return fee_services.get_all_fees(dirs=True)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/fees/fee_id/{fee_id}", response_model=Fees, tags=["Fee"])
async def get_fee_by_id(fee_id: int):
    """
    Route for getting fee by FeeID.

    :param fee_id: ID of the fee. [int]

    :return: response model Fees.
    """
    try:
        return fee_services.get_fee_by_id(fee_id, dirs=False)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/fees/full/fee_id/{fee_id}", response_model=Fees, tags=["Fee"])
async def get_fee_by_id(fee_id: int):
    """
    Route for getting fee by FeeID.

    :param fee_id: ID of the fee. [int]

    :return: response model Fees.
    """
    try:
        return fee_services.get_fee_by_id(fee_id, dirs=True)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.post("/fees/", response_model=Fees, tags=["Fee"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_fee(fee: Fees):
    """
    Route for creating a fee in basedata.

    :param fee: Model fee. [Fees]

    :return: response model Fees.
    """
    try:
        return fee_services.create_fee(fee)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.put("/fees/{fee_id}", response_model=Dict, tags=["Fee"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_fee(fee_id: int, fee: Fees):
    """
    Route for updating a fee in basedata.

    :param fee_id: ID of the fee. [int]

    :param fee: Model fee. [Fees]

    :return: response model dict.
    """
    try:
        return fee_services.update_fee(fee_id, fee)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/fees/{fee_id}", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_fee(fee_id: int):
    """
    Route for deleting a fee from basedata.

    :param fee_id: ID of the fee. [int]

    :return: response model dict.
    """
    try:
        return fee_services.delete_fee(fee_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/fee_categories/", response_model=list[FeeCategories], tags=["FeeCategory"])
async def get_all_fee_categories():
    """
    Route for get all fee categories from basedata.

    :return: response model List[FeeCategories].
    """
    try:
        return fee_category_services.get_all_fee_categories()
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/fee_categories/fee_category_id/{fee_category_id}", response_model=FeeCategories, tags=["FeeCategory"])
async def get_fee_category_by_id(fee_category_id: int):
    """
    Route for get category by FeeCategoryID.

    :param fee_category_id: ID by fee category. [int]

    :return: response model FeeCategories.
    """
    try:
        return fee_category_services.get_fee_category_by_id(fee_category_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.post("/fee_categories/", response_model=FeeCategories, tags=["FeeCategory"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_fee_category(fee_category: FeeCategories):
    """
    Route for create fee_category in basedata.

    :param fee_category: Model fee category. [Category]

    :return: response model FeeCategories.
    """
    try:
        return fee_category_services.create_fee_category(fee_category)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.put("/fee_categories/{fee_category_id}", response_model=Dict, tags=["FeeCategory"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_fee_category(fee_category_id, fee_category: FeeCategories):
    """
    Route for update fee_category in basedata.

    :param fee_category_id: ID by fee category. [int]

    :param fee_category: Model fee_category. [Categories]

    :return: response model dict.
    """
    try:
        return fee_category_services.update_fee_category(fee_category_id, fee_category)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/fee_categories/{fee_category_id}", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_fee_category(fee_category_id):
    """
    Route for delete fee_category from basedata.

    :param fee_category_id: ID by FeeCategory. [int]

    :return: response model dict.
    """
    try:
        return fee_category_services.delete_fee_category(fee_category_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/sub_categories/", response_model=list[SubCategories], tags=["SubCategory"])
async def get_all_sub_categories():
    """
    Route for get all sub categories from basedata.

    :return: response model List[SubCategories].
    """
    try:
        return sub_category_services.get_all_sub_categories()
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/sub_categories/sub_category_id/{sub_category_id}", response_model=SubCategories, tags=["SubCategory"])
async def get_sub_category_by_id(sub_category_id: int):
    """
    Route for get category by SubCategoryID.

    :param sub_category_id: ID by sub category. [int]

    :return: response model SubCategories.
    """
    try:
        return sub_category_services.get_sub_category_by_id(sub_category_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.post("/sub_categories/", response_model=SubCategories, tags=["SubCategory"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_sub_category(sub_category: SubCategories):
    """
    Route for create sub_category in basedata.

    :param sub_category: Model sub category. [Category]

    :return: response model SubCategories.
    """
    try:
        return sub_category_services.create_sub_category(sub_category)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.put("/sub_categories/{sub_category_id}", response_model=Dict, tags=["SubCategory"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_sub_category(sub_category_id, sub_category: SubCategories):
    """
    Route for update sub_category in basedata.

    :param sub_category_id: ID by sub category. [int]

    :param sub_category: Model sub_category. [SubCategories]

    :return: response model dict.
    """
    try:
        return sub_category_services.update_sub_category(sub_category_id, sub_category)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/sub_categories/{sub_category_id}", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_sub_category(sub_category_id):
    """
    Route for delete sub_category from basedata.

    :param sub_category_id: ID by SubCategory. [int]

    :return: response model dict.
    """
    try:
        return sub_category_services.delete_sub_category(sub_category_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/companies/", response_model=list[Companies], tags=["Company"])
async def get_all_companies():
    """
    Route for get all companies from basedata.

    :return: response model List[Companies].
    """
    try:
        return company_services.get_all_companies()
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/companies/company_id/{company_id}", response_model=Companies, tags=["Company"])
async def get_company_by_id(company_id: int):
    """
    Route for get company by CompanyID.

    :param company_id: ID by company. [int]

    :return: response model Companies.
    """
    try:
        return company_services.get_company_by_id(company_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.post("/companies/", response_model=Companies, tags=["Company"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_company(company: Companies):
    """
    Route for create company in basedata.

    :param company: Model company. [Companies]

    :return: response model Companies.
    """
    try:
        return company_services.create_company(company)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.put("/companies/{company_id}", response_model=Dict, tags=["Company"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_company(company_id, company: Companies):
    """
    Route for update company in basedata.

    :param company_id: ID by company. [int]

    :param company: Model company. [Companies]

    :return: response model dict.
    """
    try:
        return company_services.update_company(company_id, company)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/companies/{company_id}", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_company(company_id):
    """
    Route for delete company from basedata.

    :param company_id: ID by Company. [int]

    :return: response model dict.
    """
    try:
        return company_services.delete_company(company_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/subscriptions/", response_model=list[SubScripts], tags=["Subscription"])
async def get_all_subscriptions():
    """
    Route for getting all subscriptions from basedata.

    :return: response model List[SubScripts].
    """
    try:
        return subscription_services.get_all_subscriptions()
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/subscriptions/subscription_id/{subscription_id}", response_model=SubScripts,
         tags=["Subscription"])
async def get_subscription_by_id(subscription_id: int):
    """
    Route for getting subscription by SubScriptID.

    :param subscription_id: ID of the subscription. [int]

    :return: response model SubScripts.
    """
    try:
        return subscription_services.get_subscription_by_id(subscription_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/subscriptions/user_id/{user_id}", response_model=SubScripts,
         tags=["Subscription"])
async def get_subscription_by_user_id(user_id: int):
    """
    Route for getting subscription by SubScriptID.

    :param user_id: ID of the user. [int]

    :return: response model SubScripts.
    """
    try:
        return subscription_services.get_subscription_by_user_id(user_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.post("/subscriptions/", response_model=SubScripts, tags=["Subscription"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_subscription(subscription: SubScripts):
    """
    Route for creating an subscription in basedata.

    :param subscription: Model subscription. [SubScripts]

    :return: response model SubScripts.
    """
    try:
        return subscription_services.create_subscription(subscription)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.put("/subscriptions/{subscription_id}", response_model=Dict, tags=["Subscription"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_subscription(subscription_id: int, subscription: SubScripts):
    """
    Route for updating an subscription in basedata.

    :param subscription_id: ID of the subscription. [int]

    :param subscription: Model subscription. [Subscription]

    :return: response model dict.
    """
    try:
        return subscription_services.update_subscription(subscription_id, subscription)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/subscriptions/{subscription_id}", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_subscription(subscription_id: int):
    """
    Route for deleting an subscription from basedata.

    :param subscription_id: ID of the subscription. [int]

    :return: response model dict.
    """
    try:
        return subscription_services.delete_subscription(subscription_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/history_payments/", response_model=list[HistoryPays], tags=["HistoryPayment"])
async def get_all_history_payments():
    """
    Route for getting all history_payments from basedata.

    :return: response model List[HistoryPays].
    """
    try:
        return history_payment_services.get_all_history_payments()
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/history_payments/history_payment_id/{history_payment_id}", response_model=HistoryPays,
         tags=["HistoryPayment"])
async def get_history_payment_by_id(history_payment_id: int):
    """
    Route for getting history_payment by HistoryPayID.

    :param history_payment_id: ID of the history payment. [int]

    :return: response model HistoryPays.
    """
    try:
        return history_payment_services.get_history_payment_by_id(history_payment_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.get("/history_payments/user_id/{user_id}", response_model=HistoryPays,
         tags=["HistoryPayment"])
async def get_history_payment_by_user_id(user_id: int):
    """
    Route for getting history_payment by HistoryPayID.

    :param history_payment_id: ID of the history payment. [int]

    :return: response model HistoryPays.
    """
    try:
        return history_payment_services.get_history_payment_by_user_id(user_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.post("/history_payments/", response_model=HistoryPays, tags=["HistoryPayment"],
          dependencies=[Depends(JWTBearer(access_level=1))])
async def create_history_payment(history_payment: HistoryPays):
    """
    Route for creating an history_payment in basedata.

    :param history_payment: Model history_payment. [HistoryPays]

    :return: response model HistoryPays.
    """
    try:
        return history_payment_services.create_history_payment(history_payment)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.put("/history_payments/{history_payment_id}", response_model=Dict, tags=["HistoryPayment"],
         dependencies=[Depends(JWTBearer(access_level=1))])
async def update_history_payment(history_payment_id: int, history_payment: HistoryPays):
    """
    Route for updating an history_payment in basedata.

    :param history_payment_id: ID of the history payment. [int]

    :param history_payment: Model history payment. [HistoryPays]

    :return: response model dict.
    """
    try:
        return history_payment_services.update_history_payment(history_payment_id, history_payment)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


@app.delete("/history_payments/{history_payment_id}", response_model=Dict, tags=None,
            dependencies=[Depends(JWTBearer(access_level=1))])
async def delete_history_payment(history_payment_id: int):
    """
    Route for deleting an history payment from basedata.

    :param history_payment_id: ID of the history payment. [int]

    :return: response model dict.
    """
    try:
        return history_payment_services.delete_history_payment(history_payment_id)
    except HTTPException as ex:
        log.exception(f"Error", exc_info=ex)
        raise ex


# @app.get("/product_comments/", response_model=list[ProductComments], tags=["ProductComment"])
# async def get_all_product_comments():
#     """
#     Route for getting all product comments from basedata.
#
#     :return: response model List[ProductComments].
#     """
#     try:
#         return product_comment_services.get_all_product_comments()
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/product_comments/product_comment_id/{product_comment_id}", response_model=ProductComments,
#          tags=["ProductComment"])
# async def get_product_comment_by_id(product_comment_id: int):
#     """
#     Route for getting product comment by ProductCommentID.
#
#     :param product_comment_id: ID of the product comment. [int]
#
#     :return: response model ProductComments.
#     """
#     try:
#         return product_comment_services.get_product_comment_by_id(product_comment_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.post("/product_comments/", response_model=ProductComments, tags=["ProductComment"],
#           dependencies=[Depends(JWTBearer(access_level=1))])
# async def create_product_comment(product_comment: ProductComments):
#     """
#     Route for creating an order comment in basedata.
#
#     :param product_comment: Model Product comment. [ProductComments]
#
#     :return: response model ProductComments.
#     """
#     try:
#         return product_comment_services.create_product_comment(product_comment)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.put("/product_comments/{product_comment_id}", response_model=Dict, tags=["ProductComment"],
#          dependencies=[Depends(JWTBearer(access_level=1))])
# async def update_product_comment(product_comment_id: int, product_comment: ProductComments):
#     """
#     Route for updating an order comment in basedata.
#
#     :param product_comment_id: ID of the product comment. [int]
#
#     :param product_comment: Model order product. [ProductComments]
#
#     :return: response model dict.
#     """
#     try:
#         return product_comment_services.update_product_comment(product_comment_id, product_comment)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.delete("/product_comments/{product_comment_id}", response_model=Dict, tags=None,
#             dependencies=[Depends(JWTBearer(access_level=1))])
# async def delete_product_comment(product_comment_id: int):
#     """
#     Route for deleting an product comment from basedata.
#
#     :param product_comment_id: ID of the product comment. [int]
#
#     :return: response model product comment. [ProductComments]
#     """
#     try:
#         return product_comment_services.delete_product_comment(product_comment_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/company_comments/", response_model=list[CompanyComments], tags=["CompanyComment"])
# async def get_all_company_comments():
#     """
#     Route for getting all company comments from basedata.
#
#     :return: response model List[CompanyComments].
#     """
#     try:
#         return company_comment_services.get_all_company_comments()
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/company_comments/company_comment_id/{company_comment_id}", response_model=CompanyComments,
#          tags=["CompanyComment"])
# async def get_company_comment_by_id(company_comment_id: int):
#     """
#     Route for getting company comment by CompanyCommentID.
#
#     :param company_comment_id: ID of the company comment. [int]
#
#     :return: response model CompanyComments.
#     """
#     try:
#         return company_comment_services.get_company_comment_by_id(company_comment_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.post("/company_comments/", response_model=CompanyComments, tags=["CompanyComment"],
#           dependencies=[Depends(JWTBearer(access_level=1))])
# async def create_company_comment(company_comment: CompanyComments):
#     """
#     Route for creating an company comment in basedata.
#
#     :param company_comment: Model Company comment. [CompanyComments]
#
#     :return: response model CompanyComments.
#     """
#     try:
#         return company_comment_services.create_company_comment(company_comment)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.put("/company_comments/{company_comment_id}", response_model=Dict, tags=["CompanyComment"],
#          dependencies=[Depends(JWTBearer(access_level=1))])
# async def update_company_comment(company_comment_id: int, company_comment: CompanyComments):
#     """
#     Route for updating an company comment in basedata.
#
#     :param company_comment_id: ID of the company comment. [int]
#
#     :param company_comment: Model company product. [CompanyComments]
#
#     :return: response model dict.
#     """
#     try:
#         return company_comment_services.update_company_comment(company_comment_id, company_comment)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.delete("/company_comments/{company_comment_id}", response_model=Dict, tags=None,
#             dependencies=[Depends(JWTBearer(access_level=1))])
# async def delete_company_comment(company_comment_id: int):
#     """
#     Route for deleting an company comment from basedata.
#
#     :param company_comment_id: ID of the company comment. [int]
#
#     :return: response model company comment. [CompanyComments]
#     """
#     try:
#         return company_comment_services.delete_company_comment(company_comment_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/product_characteristics/", response_model=list[ProductCharacteristics], tags=["ProductCharacteristic"])
# async def get_all_product_characteristics():
#     """
#     Route for getting all product characteristic from basedata.
#
#     :return: response model List[ProductCharacteristics].
#     """
#     try:
#         return product_characteristic_services.get_all_product_characteristics()
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/product_characteristics/product_characteristic_id/{product_characteristic_id}",
#          response_model=ProductCharacteristics,
#          tags=["ProductCharacteristic"])
# async def get_product_characteristic_by_id(product_characteristic_id: int):
#     """
#     Route for getting product characteristic by ProductСharacteristicID.
#
#     :param product_characteristic_id: ID of the product characteristic. [int]
#
#     :return: response model ProductСharacteristics.
#     """
#     try:
#         return product_characteristic_services.get_product_characteristic_by_id(product_characteristic_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.post("/product_characteristics/", response_model=ProductCharacteristics, tags=["ProductCharacteristic"],
#           dependencies=[Depends(JWTBearer(access_level=1))])
# async def create_product_characteristic(product_characteristic: ProductCharacteristics):
#     """
#     Route for creating an product characteristic in basedata.
#
#     :param order_comment: Model product characteristic. [ProductСharacteristics]
#
#     :return: response model ProductСharacteristics.
#     """
#     try:
#         return product_characteristic_services.create_product_characteristic(product_characteristic)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.put("/product_characteristics/{product_characteristic_id}", response_model=Dict, tags=["ProductCharacteristic"],
#          dependencies=[Depends(JWTBearer(access_level=1))])
# async def update_product_characteristic(product_characteristic_id: int, product_characteristic: ProductCharacteristics):
#     """
#     Route for updating an product characteristic in basedata.
#
#     :param product_characteristic_id: ID of the product characteristic. [int]
#
#     :param product_characteristic: Model product characteristic. [ProductСharacteristics]
#
#     :return: response model dict.
#     """
#     try:
#         return product_characteristic_services.update_product_characteristic(product_characteristic_id,
#                                                                              product_characteristic)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.delete("/product_characteristics/{product_characteristic_id}", response_model=Dict, tags=None,
#             dependencies=[Depends(JWTBearer(access_level=1))])
# async def delete_product_characteristic(product_characteristic_id: int):
#     """
#     Route for deleting an product characteristic from basedata.
#
#     :param product characteristic_id: ID of the product characteristic. [int]
#
#     :return: response model dict.
#     """
#     try:
#         return product_characteristic_services.delete_product_characteristic(product_characteristic_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/receipts/", response_model=list[Receipts], tags=["Receipt"])
# async def get_all_receipts():
#     """
#     Route for get all receipts from basedata.
#
#     :return: response model List[Receipts].
#     """
#     try:
#         return receipt_services.get_all_receipts()
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/receipts/receipt_id/{receipt_id}", response_model=Receipts, tags=["Receipt"])
# async def get_receipt_by_id(receipt_id: int):
#     """
#     Route for get receipt by ReceiptID.
#
#     :param receipt_id: ID by receipt. [int]
#
#     :return: response model Receipts.
#     """
#     try:
#         return receipt_services.get_receipt_by_id(receipt_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.post("/receipts/", response_model=Receipts, tags=["Receipt"],
#           dependencies=[Depends(JWTBearer(access_level=1))])
# async def create_receipt(receipt: Receipts):
#     """
#     Route for create receipt in basedata.
#
#     :param receipt: Model receipt. [Receipts]
#
#     :return: response model Receipts.
#     """
#     try:
#         return receipt_services.create_receipt(receipt)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.put("/receipts/{receipt_id}", response_model=Dict, tags=["Receipt"],
#          dependencies=[Depends(JWTBearer(access_level=1))])
# async def update_receipt(receipt_id, receipt: Receipts):
#     """
#     Route for update receipt in basedata.
#
#     :param receipt_id: ID by receipt. [int]
#
#     :param receipt: Model receipt. [Receipts]
#
#     :return: response model dict.
#     """
#     try:
#         return receipt_services.update_receipt(receipt_id, receipt)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.delete("/receipts/{receipt_id}", response_model=Dict, tags=None,
#             dependencies=[Depends(JWTBearer(access_level=1))])
# async def delete_receipt(receipt_id):
#     """
#     Route for delete receipt in basedata.
#
#     :param receipt_id: ID by receipt. [int]
#
#     :return: response model dict.
#     """
#     try:
#         return receipt_services.delete_receipt(receipt_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/write_offs/", response_model=list[WriteOffs], tags=["WriteOff"])
# async def get_all_write_offs():
#     """
#     Route for get all write_offs from basedata.
#
#     :return: response model List[WriteOff].
#     """
#     try:
#         return write_off_services.get_all_write_offs()
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/write_offs/write_off_id/{write_off_id}", response_model=WriteOffs, tags=["WriteOff"])
# async def get_write_off_by_id(write_off_id: int):
#     """
#     Route for get write_off by WriteOffID.
#
#     :param write_off_id: ID by write off. [int]
#
#     :return: response model write offs. [WriteOff]
#     """
#     try:
#         return write_off_services.get_write_off_by_id(write_off_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.post("/write_offs/", response_model=WriteOffs, tags=["WriteOff"],
#           dependencies=[Depends(JWTBearer(access_level=1))])
# async def create_write_off(write_off: WriteOffs):
#     """
#     Route for create write off in basedata.
#
#     :param write_off: Model write off. [WriteOff]
#
#     :return: response model write offs. [WriteOff]
#     """
#     try:
#         return write_off_services.create_write_off(write_off)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.put("/write_offs/{write_off_id}", response_model=Dict, tags=["WriteOff"],
#          dependencies=[Depends(JWTBearer(access_level=1))])
# async def update_write_off(write_off_id, write_off: WriteOffs):
#     """
#     Route for update write off in basedata.
#
#     :param write_off_id: ID by write off. [int]
#
#     :param write_off: Model write_off. [WriteOff]
#
#     :return: response model dict.
#     """
#     try:
#         return write_off_services.update_write_off(write_off_id, write_off)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.delete("/write_offs/{write_off_id}", response_model=Dict, tags=None,
#             dependencies=[Depends(JWTBearer(access_level=1))])
# async def delete_write_off(write_off_id):
#     """
#     Route for delete write_off in basedata.
#
#     :param write_off_id: ID by write_off. [int]
#
#     :return: response model dict.
#     """
#     try:
#         return write_off_services.delete_write_off(write_off_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/question_answers/", response_model=list[QuestionAnswers], tags=["QuestionAnswer"])
# async def get_all_question_answers():
#     """
#     Route for get all question_answers from basedata.
#
#     :return: response model List[QuestionAnswers].
#     """
#     try:
#         return question_answer_services.get_all_question_answers()
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.get("/question_answers/question_answer_id/{question_answer_id}", response_model=QuestionAnswers,
#          tags=["QuestionAnswer"])
# async def get_question_answer_by_id(question_answer_id: int):
#     """
#     Route for get question_answer by QuestionAnswerID.
#
#     :param question_answer_id: ID by question answer. [int]
#
#     :return: response model question answers. [QuestionAnswer]
#     """
#     try:
#         return question_answer_services.get_question_answer_by_id(question_answer_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.post("/question_answers/", response_model=QuestionAnswers, tags=["QuestionAnswer"],
#           dependencies=[Depends(JWTBearer(access_level=1))])
# async def create_question_answer(question_answer: QuestionAnswers):
#     """
#     Route for create question_answer in basedata.
#
#     :param question_answer: Model question answer. [QuestionAnswers]
#
#     :return: response model question answers. [QuestionAnswers]
#     """
#     try:
#         return question_answer_services.create_question_answer(question_answer)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.put("/question_answers/{question_answer_id}", response_model=Dict, tags=["QuestionAnswer"],
#          dependencies=[Depends(JWTBearer(access_level=1))])
# async def update_question_answer(question_answer_id, question_answer: QuestionAnswers):
#     """
#     Route for update write off in basedata.
#
#     :param write_off_id: ID by write off. [int]
#
#     :param write_off: Model write_off. [QuestionAnswers]
#
#     :return: response model dict.
#     """
#     try:
#         return question_answer_services.update_question_answer(question_answer_id, question_answer)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex
#
#
# @app.delete("/question_answers/{question_answer_id}", response_model=Dict, tags=None,
#             dependencies=[Depends(JWTBearer(access_level=1))])
# async def delete_question_answer(question_answer_id):
#     """
#     Route for delete question_answer in basedata.
#
#     :param question_answer_id: ID by question_answer. [int]
#
#     :return: response model dict.
#     """
#     try:
#         return question_answer_services.delete_question_answer(question_answer_id)
#     except HTTPException as ex:
#         log.exception(f"Error", exc_info=ex)
#         raise ex


def run_server():
    import logging
    import uvicorn
    import yaml
    uvicorn_log_config = 'logging.yaml'
    with open(uvicorn_log_config, 'r') as f:
        uvicorn_config = yaml.safe_load(f.read())
        logging.config.dictConfig(uvicorn_config)
    uvicorn.run("main:app", host=config.__getattr__("HOST"), port=int(config.__getattr__("SERVER_PORT")),
                reload=True, log_config=uvicorn_log_config)


if __name__ == "__main__":
    # Создание датабазы и таблиц, если они не существуют
    log.info("Start create/update database")
    from create_sql import CreateSQL

    create_sql = CreateSQL()
    create_sql.read_sql()

    # Запуск сервера и бота
    log.info("Start run server")
    run_server()
