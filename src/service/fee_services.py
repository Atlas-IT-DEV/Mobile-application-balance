from src.repository import fee_repository
from src.database.models import Fees
from fastapi import HTTPException, status
from src.utils.exam_services import check_for_duplicates, check_if_exists
from src.service.fee_category_services import get_fee_category_by_id
from src.service.sub_category_services import get_sub_category_by_id
from src.utils.return_url_object import return_url_object
from typing import Dict
from src.utils.transform_field import transform_field


def get_all_fees(category_id: int = None, dirs: bool = False, limit: int = None, offset: int = None):
    fees = fee_repository.get_all_fees(category_id, limit, offset)
    models = [Fees(**fee) for fee in fees]
    list_fees = []
    for fee in fees:
        # Заменяем поля
        field_names = {"fee_category_id": get_fee_category_by_id}
        for field, func in field_names.items():
            fee = transform_field(field, fee, func)
        list_fees.append(fee)
    if dirs:
        return list_fees
    else:
        return models


def get_fee_by_id(fee_id: int, dirs: bool = False):
    fee = fee_repository.get_fee_by_id(fee_id)
    model = Fees(**fee) if fee else None
    # Заменяем поля
    field_names = {"fee_category_id": get_fee_category_by_id}
    for field, func in field_names.items():
        fee = transform_field(field, fee, func)
    if dirs:
        return fee
    else:
        return model


def get_fee_by_name(fee_name: str, dirs: bool = False):
    fee = fee_repository.get_fee_by_name(fee_name)
    return get_fee_by_id(fee.get("id"), dirs)


def create_fee(fee: Fees):
    check_if_exists(
        get_all=get_all_fees,
        attr_name="Name",
        attr_value=fee.Name,
        exception_detail='Fee already exist'
    )
    get_fee_category_by_id(fee.FeeCategoryID)
    fee_id = fee_repository.create_fee(fee)
    return get_fee_by_id(fee_id)


def update_fee(fee_id: int, fee: Dict):
    get_fee_by_id(fee_id)
    check_for_duplicates(
        get_all=get_all_fees,
        check_id=fee_id,
        attr_name="name",
        attr_value=fee.get("name"),
        exception_detail='Fee already exist'
    )
    if fee.get("FeeCategoryID"):
        get_fee_category_by_id(fee.get("FeeCategoryID"))
    fee_repository.update_fee(fee_id, fee)
    return {"message": "Fee updated successfully"}


def delete_fee(fee_id: int):
    get_fee_by_id(fee_id)
    fee_repository.delete_fee(fee_id)
    return {"message": "Fee deleted successfully"}
