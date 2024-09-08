from src.repository import subscription_repository
from src.service.user_services import get_user_by_id
from src.service.fee_services import get_fee_by_id
from src.service.sub_category_services import get_sub_category_by_id
from src.database.models import SubScripts
from fastapi import HTTPException


def get_all_subscriptions():
    subscriptions = subscription_repository.get_all_subscriptions()
    return [SubScripts(**subscription) for subscription in subscriptions]


def get_subscription_by_id(subscription_id: int):
    subscription = subscription_repository.get_subscription_by_id(subscription_id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Subscription not found')
    return SubScripts(**subscription) if subscription else None


def get_subscription_by_user_id(user_id: int):
    subscriptions = subscription_repository.get_subscription_by_user_id(user_id)
    if not subscriptions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Subscription not found')
    return [SubScripts(**subscription) for subscription in subscriptions]


def create_subscription(subscription: SubScripts):
    get_user_by_id(subscription.UserID)
    get_fee_by_id(subscription.FeeID)
    get_sub_category_by_id(subscription.TypeID)
    subscription_id = subscription_repository.create_subscription(subscription)
    return get_subscription_by_id(subscription_id)


def update_subscription(subscription_id: int, subscription: SubScripts):
    get_subscription_by_id(subscription_id)
    get_user_by_id(subscription.UserID)
    get_fee_by_id(subscription.FeeID)
    get_sub_category_by_id(subscription.TypeID)
    subscription_repository.update_subscription(subscription_id, subscription)
    return {"message": "Subscription updated successfully"}


def delete_subscription(subscription_id: int):
    get_subscription_by_id(subscription_id)
    subscription_repository.delete_subscription(subscription_id)
    return {"message": "Subscription deleted successfully"}
