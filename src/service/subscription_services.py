from src.repository import subscription_repository
from src.service.user_services import get_user_by_id
from src.service.fee_services import get_fee_by_id
from src.service.sub_category_services import get_sub_category_by_id
from src.service.fee_category_services import get_fee_category_by_id
from src.database.models import SubScripts
from fastapi import HTTPException, status
from typing import Dict
from src.utils.transform_field import transform_field


def get_all_subscriptions_by_fee_id(fee_id):
    subscriptions = subscription_repository.get_all_subscriptions_by_fee_id(fee_id)
    user_ids = [subscription.get("user_id") for subscription in subscriptions]
    users = []
    for user_id in user_ids:
        user = get_user_by_id(user_id)
        users.append(user)
    return users

def get_all_subscriptions(dirs: bool = False):
    subscriptions = subscription_repository.get_all_subscriptions()
    models = [SubScripts(**subscription) for subscription in subscriptions]
    list_subscriptions = []
    for subscription in subscriptions:
        # Заменяем поля
        field_names = {"user_id": get_user_by_id,
                       "fee_id": get_fee_by_id,
                       "type_sub_id": get_sub_category_by_id}
        for field, func in field_names.items():
            subscription = transform_field(field, subscription, func)
        list_subscriptions.append(subscription)
    if dirs:
        return list_subscriptions
    else:
        return models


def get_subscription_by_id(subscription_id: int, dirs: bool = False):
    subscription = subscription_repository.get_subscription_by_id(subscription_id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Subscription not found')
    model = SubScripts(**subscription) if subscription else None
    # Заменяем поля
    field_names = {"user_id": get_user_by_id,
                   "fee_id": get_fee_by_id,
                   "type_sub_id": get_sub_category_by_id}
    for field, func in field_names.items():
        subscription = transform_field(field, subscription, func)
    if dirs:
        return subscription
    else:
        return model


def get_subscription_by_user_id(user_id: int, dirs: bool = False):
    subscriptions = subscription_repository.get_subscription_by_user_id(user_id)
    if not subscriptions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Subscription not found')
    models = [SubScripts(**subscription) for subscription in subscriptions]
    list_subscriptions = []
    for subscription in subscriptions:
        # Заменяем поля
        field_names = {"user_id": get_user_by_id,
                       "fee_id": get_fee_by_id,
                       "type_sub_id": get_sub_category_by_id}
        for field, func in field_names.items():
            subscription = transform_field(field, subscription, func)
        list_subscriptions.append(subscription)
    if dirs:
        return list_subscriptions
    else:
        return models


def create_subscription(subscription: SubScripts):
    get_user_by_id(subscription.UserID)
    get_fee_by_id(subscription.FeeID)
    get_sub_category_by_id(subscription.TypeID)
    subscription_id = subscription_repository.create_subscription(subscription)
    return get_subscription_by_id(subscription_id)


def update_subscription(subscription_id: int, subscription: Dict):
    get_subscription_by_id(subscription_id)
    if subscription.get("UserID"):
        get_user_by_id(subscription.get("UserID"))
    if subscription.get("FeeID"):
        get_fee_by_id(subscription.get("FeeID"))
    if subscription.get("TypeID"):
        get_sub_category_by_id(subscription.get("TypeID"))
    subscription_repository.update_subscription(subscription_id, subscription)
    return {"message": "Subscription updated successfully"}


def delete_subscription(subscription_id: int):
    get_subscription_by_id(subscription_id)
    subscription_repository.delete_subscription(subscription_id)
    return {"message": "Subscription deleted successfully"}
