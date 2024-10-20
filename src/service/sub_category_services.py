from src.repository import sub_category_repository
from src.database.models import SubCategories
from fastapi import HTTPException, status
from src.utils.exam_services import check_for_duplicates, check_if_exists
from typing import Dict


def get_all_sub_categories():
    sub_categories = sub_category_repository.get_all_sub_categories()
    return [SubCategories(**sub_category) for sub_category in sub_categories]


def get_sub_category_by_id(sub_category_id: int):
    sub_category = sub_category_repository.get_sub_category_by_id(sub_category_id)
    if not sub_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sub category not found')
    return SubCategories(**sub_category) if sub_category else None


def create_sub_category(sub_category: SubCategories):
    check_if_exists(
        get_all=get_all_sub_categories,
        attr_name="Type",
        attr_value=sub_category.Type,
        exception_detail='Sub category already exist'
    )
    sub_category_id = sub_category_repository.create_sub_category(sub_category)
    return get_sub_category_by_id(sub_category_id)


def update_sub_category(sub_category_id: int, sub_category: Dict):
    check_for_duplicates(
        get_all=get_all_sub_categories,
        check_id=sub_category_id,
        attr_name="Type",
        attr_value=sub_category.get("Type"),
        exception_detail='Sub category already exist'
    )
    sub_category_repository.update_sub_category(sub_category_id, sub_category)
    return {"message": "Sub category updated successfully"}


def delete_sub_category(sub_category_id: int):
    get_sub_category_by_id(sub_category_id)
    sub_category_repository.delete_sub_category(sub_category_id)
    return {"message": "Sub category deleted successfully"}
