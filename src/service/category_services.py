from src.repository import category_repository
from src.database.models import Categories
from fastapi import HTTPException, status


async def get_all_categories():
    categories = await category_repository.get_all_categories()
    return [Categories(**category) for category in categories]


async def get_category_by_id(category_id: int):
    category = await category_repository.get_category_by_id(category_id)
    return Categories(**category) if category else None


async def create_category(category: Categories):
    category_id = await category_repository.create_category(category)
    return await get_category_by_id(category_id)


async def update_category(category_id: int, category: Categories):
    await category_repository.update_category(category_id, category)
    return {"message": "Category updated successfully"}


async def delete_category(category_id: int):
    await category_repository.delete_category(category_id)
    return {"message": "Category deleted successfully"}
