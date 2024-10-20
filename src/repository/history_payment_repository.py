from src.database.my_connector import db
from src.database.models import HistoryPays
from typing import Dict


def get_all_history_payments():
    query = "SELECT * FROM history_payments"
    return db.fetch_all(query)


def get_history_payment_by_id(history_payment_id: int):
    query = "SELECT * FROM history_payments WHERE id=%s"
    return db.fetch_one(query, (history_payment_id,))


def get_history_payment_by_user_id(user_id: int):
    query = "SELECT * FROM history_payments WHERE user_id=%s"
    return db.fetch_all(query, (user_id,))


def create_history_payment(history_payment: HistoryPays):
    query = "INSERT INTO history_payments (user_id, fee_id, pay, created_at) VALUES (%s, %s, %s, %s)"
    params = history_payment.UserID, history_payment.FeeID, history_payment.Pay, history_payment.CreatedAt
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_history_payment(history_payment_id: int, history_payment: Dict):
    fields_to_update = [f"{key}=%s" for key in history_payment.keys()]
    params = list(history_payment.values())
    query = f"UPDATE history_payments SET {', '.join(fields_to_update)} WHERE id=%s"
    params.append(history_payment_id)
    db.execute_query(query, tuple(params))


def delete_history_payment(history_payment_id: int):
    query = "DELETE FROM history_payments WHERE id=%s"
    db.execute_query(query, (history_payment_id,))
