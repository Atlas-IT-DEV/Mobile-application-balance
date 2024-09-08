from src.repository import history_payment_repository
from src.service.user_services import get_user_by_id
from src.service.fee_services import get_fee_by_id
from src.database.models import HistoryPays
from fastapi import HTTPException


def get_all_history_payments():
    history_payments = history_payment_repository.get_all_history_payments()
    return [HistoryPays(**history_payment) for history_payment in history_payments]


def get_history_payment_by_id(history_payment_id: int):
    history_payment = history_payment_repository.get_history_payment_by_id(history_payment_id)
    if not history_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'History payment not found')
    return HistoryPays(**history_payment) if history_payment else None


def get_history_payment_by_user_id(user_id: int):
    history_payments = history_payment_repository.get_history_payment_by_user_id(user_id)
    if not history_payments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'History payment not found')
    return [HistoryPays(**history_payment) for history_payment in history_payments]


def create_history_payment(history_payment: HistoryPays):
    get_user_by_id(history_payment.UserID)
    get_fee_by_id(history_payment.FeeID)
    history_payment_id = history_payment_repository.create_history_payment(history_payment)
    return get_history_payment_by_id(history_payment_id)


def update_history_payment(history_payment_id: int, history_payment: HistoryPays):
    get_history_payment_by_id(history_payment_id)
    get_user_by_id(history_payment.UserID)
    get_fee_by_id(history_payment.FeeID)
    history_payment_repository.update_history_payment(history_payment_id, history_payment)
    return {"message": "History payment updated successfully"}


def delete_history_payment(history_payment_id: int):
    get_history_payment_by_id(history_payment_id)
    history_payment_repository.delete_history_payment(history_payment_id)
    return {"message": "History payment deleted successfully"}
