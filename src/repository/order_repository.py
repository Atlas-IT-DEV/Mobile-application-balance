from src.database.my_connector import Database
from src.database.models import Orders
from datetime import datetime
db = Database()


async def get_all_orders():
    query = "SELECT * FROM Orders"
    return await db.fetch_all(query)


async def get_order_by_id(order_id: int):
    query = "SELECT * FROM orders WHERE id=%s"
    return await db.fetch_one(query, (order_id,))


async def get_order_by_user_id(user_id: int):
    query = "SELECT * FROM orders WHERE user_id=%s"
    return await db.fetch_all(query, (user_id,))


async def create_order(order: Orders):
    query = "INSERT INTO orders (user_id, date, total_price) VALUES (%s, %s, %s)"
    params = (order.UserID, order.Date, order.TotalPrice)
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_order(order_id: int, order: Orders):
    query = "UPDATE orders SET user_id=%s, date=%s, total_price=%s WHERE id=%s"
    params = (order.UserID, order.Date, order.TotalPrice, order_id)
    await db.execute_query(query, params)


async def delete_order(order_id: int):
    query = "DELETE FROM orders WHERE id=%s"
    await db.execute_query(query, (order_id,))







