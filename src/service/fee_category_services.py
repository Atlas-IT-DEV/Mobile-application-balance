from src.repository import fee_category_repository
from src.database.models import FeeCategories
from fastapi import HTTPException, status
from src.utils.exam_services import check_for_duplicates, check_if_exists


def get_all_fee_categories():
    fee_categories = fee_category_repository.get_all_fee_categories()
    return [FeeCategories(**fee_category) for fee_category in fee_categories]


def get_fee_category_by_id(fee_category_id: int):
    fee_category = fee_category_repository.get_fee_category_by_id(fee_category_id)
    if not fee_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Fee category not found')
    return FeeCategories(**fee_category) if fee_category else None


def create_fee_category(fee_category: FeeCategories):
    check_if_exists(
        get_all=get_all_fee_categories,
        attr_name="Name",
        attr_value=fee_category.Name,
        exception_detail='Fee category already exist'
    )
    fee_category_id = fee_category_repository.create_fee_category(fee_category)
    return get_fee_category_by_id(fee_category_id)


def update_fee_category(fee_category_id: int, fee_category: FeeCategories):
    check_for_duplicates(
        get_all=get_all_fee_categories,
        check_id=fee_category_id,
        attr_name="Name",
        attr_value=fee_category.Name,
        exception_detail='Fee category already exist'
    )
    fee_category_repository.update_fee_category(fee_category_id, fee_category)
    return {"message": "Fee category updated successfully"}


def delete_fee_category(fee_category_id: int):
    get_fee_category_by_id(fee_category_id)
    fee_category_repository.delete_fee_category(fee_category_id)
    return {"message": "Fee category deleted successfully"}
