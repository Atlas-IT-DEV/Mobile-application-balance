from src.database.my_connector import db
from src.database.models import SubScripts


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


def update_subscription(subscription_id: int, subscription: SubScripts):
    query = "UPDATE subscriptions SET user_id=%s, fee_id=%s, type_sub_id=%s WHERE id=%s"
    params = subscription.UserID, subscription.FeeID, subscription.TypeID, subscription_id
    db.execute_query(query, params)


def delete_subscription(subscription_id: int):
    query = "DELETE FROM subscriptions WHERE id=%s"
    db.execute_query(query, (subscription_id,))