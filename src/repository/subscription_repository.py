from src.database.my_connector import db
from src.database.models import SubScripts
from typing import Dict


def get_all_subscriptions():
    query = "SELECT * FROM subscriptions"
    return db.fetch_all(query)


def get_subscription_by_id(subscription_id: int):
    query = "SELECT * FROM subscriptions WHERE id=%s"
    return db.fetch_one(query, (subscription_id,))


def get_subscription_by_user_id(user_id: int):
    query = "SELECT * FROM subscriptions WHERE user_id=%s"
    return db.fetch_all(query, (user_id,))


def create_subscription(subscription: SubScripts):
    query = "INSERT INTO subscriptions (user_id, fee_id, type_sub_id) VALUES (%s, %s, %s)"
    params = subscription.UserID, subscription.FeeID, subscription.TypeID
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_subscription(subscription_id: int, subscription: Dict):
    fields_to_update = [f"{key}=%s" for key in subscription.keys()]
    params = list(subscription.values())
    query = f"UPDATE subscriptions SET {', '.join(fields_to_update)} WHERE id=%s"
    params.append(subscription_id)
    db.execute_query(query, tuple(params))


def delete_subscription(subscription_id: int):
    query = "DELETE FROM subscriptions WHERE id=%s"
    db.execute_query(query, (subscription_id,))
