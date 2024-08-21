from src.service import user_services, image_services, product_services
from src.database.models import Users, Images, Products
from fastapi import HTTPException, status


def exam_user(user_id: int):
    # Проверка существования профиля
    existing_user = user_services.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not exist")
    return existing_user


"""async def exam_fee(fee_id: int):
    # Проверка существования сбора
    existing_fee = product_services.get_fee_by_id(fee_id)
    if not existing_fee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fee not exist")
    return existing_fee"""

