from src.repository import history_payment_repository
from src.service.user_services import get_user_by_id
from src.service.fee_services import get_fee_by_id
from src.service.fee_services import get_fee_by_name
from src.database.models import HistoryPays
from fastapi import HTTPException, status
from typing import Dict
from src.utils.transform_field import transform_field


def get_all_history_payments(dirs: bool = False):
    history_payments = history_payment_repository.get_all_history_payments()
    models = [HistoryPays(**history_payment) for history_payment in history_payments]
    list_history_payments = []
    for history_payment in history_payments:
        # Заменяем поля
        field_names = {"user_id": get_user_by_id,
                       "fee_id": get_fee_by_id}
        for field, func in field_names.items():
            history_payment = transform_field(field, history_payment, func)
        list_history_payments.append(history_payment)
    if dirs:
        return list_history_payments
    else:
        return models


def get_history_payment_by_id(history_payment_id: int, dirs: bool = False):
    history_payment = history_payment_repository.get_history_payment_by_id(history_payment_id)
    if not history_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'History payment not found')
    model = HistoryPays(**history_payment) if history_payment else None
    # Заменяем поля
    field_names = {"user_id": get_user_by_id,
                   "fee_id": get_fee_by_id}
    for field, func in field_names.items():
        history_payment = transform_field(field, history_payment, func)
    if dirs:
        return history_payment
    else:
        return model


def get_history_payment_by_user_id(user_id: int, dirs: bool = False):
    history_payments = history_payment_repository.get_history_payment_by_user_id(user_id)
    if not history_payments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'History payment not found')
    models = [HistoryPays(**history_payment) for history_payment in history_payments]
    list_history_payments = []
    for history_payment in history_payments:
        # Заменяем поля
        field_names = {"user_id": get_user_by_id,
                       "fee_id": get_fee_by_id}
        for field, func in field_names.items():
            history_payment = transform_field(field, history_payment, func)
        list_history_payments.append(history_payment)
    if dirs:
        return list_history_payments
    else:
        return models


def get_history_payment_by_fee_name(fee_name: str):
    fee = get_fee_by_name(fee_name)
    history_payments = get_all_history_payments()
    list_history_payments_ids = []
    for history_payment in history_payments:
        if history_payment.FeeID == fee.ID:
            list_history_payments_ids.append(history_payment.ID)
    list_history_payments = []
    history_payments = get_all_history_payments(True)
    for history_payment in history_payments:
        if history_payment.get("id") in list_history_payments_ids:
            list_history_payments.append(history_payment)
    return list_history_payments


def get_history_payment_by_fee_name_and_user_id(fee_name: str, user_id: int):
    fee = get_fee_by_name(fee_name)
    user = get_user_by_id(user_id)
    history_payments = get_all_history_payments()
    list_history_payments_ids = []
    for history_payment in history_payments:
        if history_payment.FeeID == fee.ID and history_payment.UserID == user.ID:
            list_history_payments_ids.append(history_payment.ID)
    list_history_payments = []
    history_payments = get_all_history_payments(True)
    for history_payment in history_payments:
        if history_payment.get("id") in list_history_payments_ids:
            list_history_payments.append(history_payment)
    return list_history_payments


def create_history_payment(history_payment: HistoryPays):
    get_user_by_id(history_payment.UserID)
    get_fee_by_id(history_payment.FeeID)
    history_payment_id = history_payment_repository.create_history_payment(history_payment)
    return get_history_payment_by_id(history_payment_id)


def update_history_payment(history_payment_id: int, history_payment: Dict):
    get_history_payment_by_id(history_payment_id)
    if history_payment.get("UserID"):
        get_user_by_id(history_payment.get("UserID"))
    if history_payment.get("FeeID"):
        get_fee_by_id(history_payment.get("FeeID"))
    history_payment_repository.update_history_payment(history_payment_id, history_payment)
    return {"message": "History payment updated successfully"}


def delete_history_payment(history_payment_id: int):
    get_history_payment_by_id(history_payment_id)
    history_payment_repository.delete_history_payment(history_payment_id)
    return {"message": "History payment deleted successfully"}
