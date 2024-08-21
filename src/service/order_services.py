from src.repository import order_repository
from src.service import user_services, product_services, order_product_services, exam_services
from src.database.models import Orders, OrderProducts, Products, ProductsDict
from fastapi import HTTPException, status
from datetime import datetime


async def get_all_orders():
    orders = await order_repository.get_all_orders()
    return [Orders(**order) for order in orders]


async def get_order_by_id(order_id: int):
    order = await order_repository.get_order_by_id(order_id)
    return Orders(**order) if order else None


async def get_order_by_user_id(user_id: int):
    orders = await order_repository.get_order_by_user_id(user_id)
    return [Orders(**order) for order in orders]


async def create_order(order: Orders):
    order_id = await order_repository.create_order(order)
    return await get_order_by_id(order_id)


async def update_order(order_id: int, order: Orders):
    await order_repository.update_order(order_id, order)
    return {"message": "Order updated successfully"}


async def delete_order(order_id: int):
    await order_repository.delete_order(order_id)
    return {"message": "Order deleted successfully"}


async def place_an_order(user_id: int, products: list[ProductsDict]):
    user = await exam_services.exam_user(user_id)
    # Создаем заказ
    order = await create_order(Orders(user_id=user.ID, date=datetime.now(), total_price=1))
    # Добавляем товары в заказ
    list_added_product = []
    for product in products:
        product_id = product.ProductID
        quantity = product.Quantity
        current_order_products = await order_product_services.create_order_product(OrderProducts(order_id=order.ID,
                                                                                                 product_id=product_id,
                                                                                                 quantity=quantity))
        list_added_product.append(current_order_products.ID)
    list_order_products = []
    # Собираем заказы и рассчитываем итоговую стоимость заказа
    for add in list_added_product:
        list_order_products.append(await order_product_services.get_order_product_by_id(add))
    total_price = 0
    for order_product in list_order_products:
        product = await product_services.get_product_by_id(order_product.ProductID)
        total_price += product.Price * order_product.Quantity
    await update_order(order_id=order.ID, order=Orders(user_id=user.ID,
                                                       date=datetime.now(),
                                                       total_price=total_price))
    return list_order_products


async def get_hystory_orders_by_user_id(user_id: int):
    user = await exam_services.exam_user(user_id)
    # Получаем всю историю заказов пользователя
    list_hystory = []
    orders = await get_order_by_user_id(user.ID)
    for order in orders:
        if not order:
            continue
        list_hystory.append(await order_product_services.get_order_product_by_order_id(order.ID))
    return list_hystory
