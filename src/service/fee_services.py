from src.repository import fee_repository
from src.database.models import Fees
from fastapi import HTTPException, status
from src.utils.exam_services import check_for_duplicates, check_if_exists
from src.service.fee_category_services import get_fee_category_by_id
from src.service.sub_category_services import get_sub_category_by_id
from src.utils.return_url_object import return_url_object


def get_all_fees(dirs: bool = False):
    fees = fee_repository.get_all_fees()
    models = [Fees(**fee) for fee in fees]
    list_fees = []
    for fee in fees:
        # Заменяем fee_category_id
        fee_category_id = fee.get("fee_category_id")
        if fee_category_id:
            fee_category = get_fee_category_by_id(fee_category_id)
            fee["fee_category"] = fee_category.model_dump(by_alias=True)
            del fee["fee_category_id"]
        list_fees.append(fee)
    if dirs:
        return list_fees
    else:
        return models


def get_fee_by_id(fee_id: int, dirs: bool = False):
    # Получаем fee из репозитория по ID
    fee = fee_repository.get_fee_by_id(fee_id)
    model = Fees(**fee) if fee else None
    # Если fee не найден, выбрасываем исключение
    if not fee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Fee not found')
    # Обрабатываем fee_category_id
    fee_category_id = fee.get("fee_category_id")
    if fee_category_id:
        fee_category = get_fee_category_by_id(fee_category_id)
        fee["fee_category"] = fee_category.model_dump(by_alias=True)
        del fee["fee_category_id"]
    if dirs:
        return fee
    else:
        return model


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


def update_fee(fee_id: int, fee: Fees):
    get_fee_by_id(fee_id)
    check_for_duplicates(
        get_all=get_all_fees,
        check_id=fee_id,
        attr_name="Name",
        attr_value=fee.Name,
        exception_detail='Fee already exist'
    )
    get_fee_category_by_id(fee.FeeCategoryID)
    fee_repository.update_fee(fee_id, fee)
    return {"message": "Fee updated successfully"}


def delete_fee(fee_id: int):
    get_fee_by_id(fee_id)
    fee_repository.delete_fee(fee_id)
    return {"message": "Fee deleted successfully"}
