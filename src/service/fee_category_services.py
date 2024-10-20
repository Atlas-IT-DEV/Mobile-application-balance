from src.repository import fee_category_repository
from src.database.models import FeeCategories
from src.repository.fee_repository import get_all_fees
from src.utils.transform_field import transform_field
from fastapi import HTTPException, status
from src.utils.exam_services import check_for_duplicates, check_if_exists
from typing import Dict


def get_all_fee_categories():
    fee_categories = fee_category_repository.get_all_fee_categories()
    return [FeeCategories(**fee_category) for fee_category in fee_categories]


def get_fee_category_by_id(fee_category_id: int):
    fee_category = fee_category_repository.get_fee_category_by_id(fee_category_id)
    if not fee_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Fee category not found')
    return FeeCategories(**fee_category) if fee_category else None


def get_all_fee_by_category_name(category_name: str, dirs: bool = False):
    fee_categories = get_all_fee_categories()
    list_fees = []
    for fee_category in fee_categories:
        if fee_category.Name == category_name:
            fees = get_all_fees()
            for fee in fees:
                if fee.get("fee_category_id") == fee_category.ID:
                    if dirs:
                        fee = transform_field("fee_category_id", fee, get_fee_category_by_id)
                    list_fees.append(fee)
    return list_fees


def create_fee_category(fee_category: FeeCategories):
    check_if_exists(
        get_all=get_all_fee_categories,
        attr_name="Name",
        attr_value=fee_category.Name,
        exception_detail='Fee category already exist'
    )
    fee_category_id = fee_category_repository.create_fee_category(fee_category)
    return get_fee_category_by_id(fee_category_id)


def update_fee_category(fee_category_id: int, fee_category: Dict):
    check_for_duplicates(
        get_all=get_all_fee_categories,
        check_id=fee_category_id,
        attr_name="Name",
        attr_value=fee_category.get("Name"),
        exception_detail='Fee category already exist'
    )
    fee_category_repository.update_fee_category(fee_category_id, fee_category)
    return {"message": "Fee category updated successfully"}


def delete_fee_category(fee_category_id: int):
    get_fee_category_by_id(fee_category_id)
    fee_category_repository.delete_fee_category(fee_category_id)
    return {"message": "Fee category deleted successfully"}
