from src.repository import order_product_repository
from src.database.models import OrderProducts
from fastapi import HTTPException


async def get_all_orders_products():
    orders_products = await order_product_repository.get_all_orders_products()
    return [OrderProducts(**order_product) for order_product in orders_products]


async def get_order_product_by_id(order_product_id: int):
    order_product = await order_product_repository.get_order_product_by_id(order_product_id)
    return OrderProducts(**order_product) if order_product else None


async def get_order_product_by_order_id(order_id: int):
    orders = await order_product_repository.get_order_product_by_order_id(order_id)
    return [OrderProducts(**orders) for orders in orders]


async def create_order_product(order_product: OrderProducts):
    order_product_id = await order_product_repository.create_order_product(order_product)
    return await get_order_product_by_id(order_product_id)


async def update_order_product(order_product_id: int, order_product: OrderProducts):
    await order_product_repository.update_order_product(order_product_id, order_product)
    return {"message": "Order product updated successfully"}


async def delete_order_product(order_product_id: int):
    await order_product_repository.delete_order_product(order_product_id)
    return {"message": "Order product deleted successfully"}
