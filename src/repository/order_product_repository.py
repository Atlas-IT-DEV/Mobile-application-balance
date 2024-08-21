from src.database.my_connector import Database
from src.database.models import OrderProducts
db = Database()


async def get_all_orders_products():
    query = "SELECT * FROM Order_Products"
    return await db.fetch_all(query)


async def get_order_product_by_id(order_product_id: int):
    query = "SELECT * FROM order_products WHERE id=%s"
    return await db.fetch_one(query, (order_product_id,))


async def get_order_product_by_order_id(order_id: int):
    query = "SELECT * FROM order_products WHERE order_id=%s"
    return await db.fetch_all(query, (order_id,))


async def create_order_product(order_product: OrderProducts):
    query = "INSERT INTO order_products (order_id, product_id, quantity) VALUES (%s, %s, %s)"
    params = (order_product.OrderID, order_product.ProductID, order_product.Quantity)
    cursor = await db.execute_query(query, params)
    return cursor.lastrowid


async def update_order_product(order_product_id: int, order_product: OrderProducts):
    query = "UPDATE order_products SET order_id=%s, product_id=%s, quantity=%s WHERE id=%s"
    params = (order_product.OrderID, order_product.ProductID, order_product.Quantity, order_product_id)
    await db.execute_query(query, params)


async def delete_order_product(order_product_id: int):
    query = "DELETE FROM order_products WHERE id=%s"
    await db.execute_query(query, (order_product_id,))
