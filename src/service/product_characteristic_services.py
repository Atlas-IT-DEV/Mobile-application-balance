from src.repository import product_characteristic_repository
from src.database.models import ProductCharacteristics
from fastapi import HTTPException, status
from datetime import datetime


async def get_all_product_characteristics():
    product_characteristics = await product_characteristic_repository.get_all_product_characteristics()
    return [ProductCharacteristics(**product_characteristic) for product_characteristic in product_characteristics]


async def get_product_characteristic_by_id(product_characteristic_id: int):
    product_characteristic = await product_characteristic_repository.get_product_characteristic_by_id(product_characteristic_id)
    return ProductCharacteristics(**product_characteristic) if product_characteristic else None


async def get_product_characteristic_by_user_id(user_id: int):
    product_characteristics = await product_characteristic_repository.get_product_characteristic_by_user_id(user_id)
    return [ProductCharacteristics(**product_characteristic) for product_characteristic in product_characteristics]


async def create_product_characteristic(product_characteristic: ProductCharacteristics):
    product_characteristic_id = await product_characteristic_repository.create_product_characteristic(product_characteristic)
    return await get_product_characteristic_by_id(product_characteristic_id)


async def update_product_characteristic(product_characteristic_id: int, product_characteristic: ProductCharacteristics):
    await product_characteristic_repository.update_product_characteristic(product_characteristic_id, product_characteristic)
    return {"message": "Product characteristic updated successfully"}


async def delete_product_characteristic(product_characteristic_id: int):
    await product_characteristic_repository.delete_product_characteristic(product_characteristic_id)
    return {"message": "Product characteristic deleted successfully"}
