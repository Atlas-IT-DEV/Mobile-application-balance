from src.repository import product_repository
from src.database.models import Products
from fastapi import HTTPException, status, Form
from src.utils.hashing import validate_password


async def get_all_products():
    products = await product_repository.get_all_products()
    return [Products(**product) for product in products]


async def get_product_by_id(product_id: int):
    product = await product_repository.get_product_by_id(product_id)
    return Products(**product) if product else None


async def create_product(product: Products):
    product_id = await product_repository.create_product(product)
    return await get_product_by_id(product_id)


async def update_product(product_id: int, product: Products):
    await product_repository.update_product(product_id, product)
    return {"message": "Product updated successfully"}


async def delete_product(product_id: int):
    await product_repository.delete_product(product_id)
    return {"message": "Product deleted successfully"}
